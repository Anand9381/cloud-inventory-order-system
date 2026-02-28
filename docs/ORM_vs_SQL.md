# Raw SQL vs ORM Query Comparison

This document highlights the differences between performing raw SQL queries and using an Object-Relational Memory (ORM) library like SQLAlchemy, as demonstrated in our codebase.

## 1. Fetching All Users

### Raw SQL (Example):
```sql
SELECT * FROM users;
```

### SQLAlchemy ORM (Current Implementation):
```python
users = User.query.all()
```
*   **Advantage**: Abstraction over database dialect. No need to write specific syntax for MySQL vs PostgreSQL.

## 2. Filtering (Fetch User by ID)

### Raw SQL (Example):
```sql
SELECT * FROM users WHERE id = 1;
```

### SQLAlchemy ORM:
```python
user = User.query.get(1)
# OR
user = User.query.filter_by(id=1).first()
```
*   **Advantage**: Automatically handles parameter binding, preventing SQL injection.

## 3. Inserting Data with Relationships (Creating an Order)

### Raw SQL (Example):
```sql
START TRANSACTION;
INSERT INTO orders (user_id, status, total_amount) VALUES (1, 'Pending', 100.0);
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (LAST_INSERT_ID(), 1, 2, 50.0);
COMMIT;
```

### SQLAlchemy ORM:
```python
order = Order(user_id=1, status='Pending', total_amount=100.0)
item = OrderItem(order=order, product_id=1, quantity=2, price_at_purchase=50.0) 
db.session.add(order) 
# OrderItem is automatically linked via relationship during commit
db.session.commit()
```
*   **Advantage**: Seamlessly manages complex object graphs and transaction boundaries without manual `BEGIN`/`COMMIT`.

## 4. Updates (Changing Order Status)

### Raw SQL (Example):
```sql
UPDATE orders SET status = 'Completed' WHERE id = 1;
```

### SQLAlchemy ORM:
```python
order = Order.query.get(1)
order.status = 'Completed'
db.session.commit()
```
*   **Advantage**: Modifying Python object attributes directly feels more natural and integrates with code logic.

## 5. Pagination

### Raw SQL (Example):
```sql
SELECT * FROM products LIMIT 10 OFFSET 20;
```

### SQLAlchemy ORM:
```python
products = Product.query.paginate(page=3, per_page=10, error_out=False)
```
*   **Advantage**: Built-in helper methods simplify pagination logic significantly.
