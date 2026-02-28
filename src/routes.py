from flask import Blueprint, request, jsonify, render_template
from src.extensions import db
from src.models import User, Product, Inventory, Order, OrderItem
from src.mongo_service import log_activity, get_logs, get_log_count
from sqlalchemy.exc import IntegrityError

api = Blueprint('api', __name__)
main = Blueprint('main', __name__)

# --- Frontend Routes ---
@main.route('/')
def index():
    stats = {
        'products': Product.query.count(),
        'orders': Order.query.count(),
        'users': User.query.count(),
        'logs': get_log_count() # Fetch from MongoDB
    }
    return render_template('index.html', stats=stats)

@main.route('/products')
def products_page():
    products = Product.query.all()
    return render_template('products.html', products=products)

@main.route('/orders')
def orders_page():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

@main.route('/users')
def users_page():
    users = User.query.all()
    return render_template('users.html', users=users)

@main.route('/logs')
def logs_page():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', 50, type=int)
    
    logs = get_logs(limit=limit, start_date=start_date, end_date=end_date)
    return render_template('logs.html', logs=logs)


# --- API Routes ---

# User CRUD
@api.route('/users', methods=['POST'])
def create_user():
    data = request.json
    try:
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        log_activity(new_user.id, 'CREATE_USER', f"Created user {new_user.username}")
        return jsonify(new_user.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'User already exists'}), 400

@api.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'users': [u.to_dict() for u in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@api.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    elif request.method == 'PUT':
        data = request.json
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        try:
            db.session.commit()
            log_activity(user.id, 'UPDATE_USER', f"Updated user {user.username}")
            return jsonify(user.to_dict())
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Username or Email already exists'}), 400

    elif request.method == 'DELETE':
        try:
            db.session.delete(user)
            db.session.commit()
            log_activity('ADMIN', 'DELETE_USER', f"Deleted user {user.username} (ID: {user_id})")
            return jsonify({'message': 'User deleted'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


# Product CRUD
@api.route('/products', methods=['POST'])
def create_product():
    data = request.json
    # Create Product
    new_product = Product(
        name=data['name'], 
        description=data.get('description', ''),
        price=data['price'],
        sku=data['sku']
    )
    db.session.add(new_product)
    db.session.flush() # Get ID before commit

    # Create Inventory entry
    initial_stock = data.get('stock', 0)
    inventory = Inventory(product_id=new_product.id, quantity=initial_stock)
    db.session.add(inventory)
    
    db.session.commit()
    log_activity('ADMIN', 'CREATE_PRODUCT', f"Created product {new_product.name}")
    return jsonify(new_product.to_dict()), 201

@api.route('/products', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'products': [p.to_dict() for p in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@api.route('/products/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'GET':
        return jsonify(product.to_dict())

    elif request.method == 'PUT':
        data = request.json
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.sku = data.get('sku', product.sku)

        # Update Stock via Inventory if provided
        if 'stock' in data:
            if not product.inventory:
                inventory = Inventory(product_id=product.id, quantity=data['stock'])
                db.session.add(inventory)
            else:
                product.inventory.quantity = data['stock']
        
        try:
            db.session.commit()
            log_activity('ADMIN', 'UPDATE_PRODUCT', f"Updated product {product.name}")
            return jsonify(product.to_dict())
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'SKU already exists'}), 400

    elif request.method == 'DELETE':
        try:
            db.session.delete(product)
            db.session.commit()
            log_activity('ADMIN', 'DELETE_PRODUCT', f"Deleted product {product.name} (ID: {product_id})")
            return jsonify({'message': 'Product deleted'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


# Order Creation (Complex)
@api.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    user_id = data.get('user_id')
    items_data = data.get('items', [])

    if not user_id or not items_data:
        return jsonify({'error': 'Missing user_id or items'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Start Transaction
    try:
        new_order = Order(user_id=user_id, status='Pending')
        db.session.add(new_order)
        db.session.flush()
        
        total_amount = 0
        
        for item in items_data:
            product_id = item['product_id']
            qty = item['quantity']
            
            product = Product.query.get(product_id)
            if not product:
                raise ValueError(f"Product {product_id} not found")
            
            # Check Stock
            if product.inventory.quantity < qty:
                raise ValueError(f"Insufficient stock for {product.name}")
            
            # Deduct Stock
            product.inventory.quantity -= qty
            
            # Create Order Item
            order_item = OrderItem(
                order_id=new_order.id, 
                product_id=product_id, 
                quantity=qty, 
                price_at_purchase=product.price
            )
            db.session.add(order_item)
            total_amount += product.price * qty

        new_order.total_amount = total_amount
        new_order.status = 'Completed' # Simple flow
        db.session.commit()
        
        log_activity(user_id, 'CREATE_ORDER', f"Order {new_order.id} created. Total: {total_amount}")
        
        return jsonify(new_order.to_dict()), 201

    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

@api.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_order(order_id):
    order = Order.query.get_or_404(order_id)

    if request.method == 'GET':
        return jsonify(order.to_dict())

    elif request.method == 'PUT':
        # Primarily for updating status.
        # Ideally, changing items would require recalculating totals, stock, etc.
        # For this assignment, we'll focus on status updates.
        data = request.json
        status = data.get('status')
        if status:
            if status not in ['Pending', 'Completed', 'Cancelled']:
                return jsonify({'error': 'Invalid status'}), 400
            order.status = status
            
        db.session.commit()
        log_activity(order.user_id, 'UPDATE_ORDER', f"Updated order {order.id} status to {status}")
        return jsonify(order.to_dict())

    elif request.method == 'DELETE':
        try:
            # Note: Deleting an order might not return stock. 
            # In a real system, you'd likely restore stock if not shipped.
            # Here we just delete for CRUD completeness.
            db.session.delete(order)
            db.session.commit()
            log_activity('ADMIN', 'DELETE_ORDER', f"Deleted order {order.id}")
            return jsonify({'message': 'Order deleted'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

@api.route('/orders', methods=['GET'])
def get_orders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = Order.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'orders': [o.to_dict() for o in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@api.route('/logs', methods=['GET'])
def get_logs_api():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', 50, type=int)
    
    logs = get_logs(limit=limit, start_date=start_date, end_date=end_date)
    return jsonify(logs)

