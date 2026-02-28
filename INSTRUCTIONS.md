# Quick Start Guide

## 1. Start the System (Recommended)
The easiest way to run the full system with MySQL and MongoDB is using Docker.

1. Open a terminal in this folder: `Day_26/cloud_inventory_system`
2. Run the following command:
   ```bash
   docker-compose up --build -d
   ```
   *(This downloads MySQL and MongoDB images and builds your Python app)*

3. Verify it's running:
   - Open browser: [http://localhost:5000](http://localhost:5000)

## 2. Populate Data (Seeding)
Once the server is running, populate it with sample users, products, and orders logic.

1. Ensure you have Python installed locally, or exec into the container.
2. Local run (if you have `requests` installed):
   ```bash
   pip install requests
   python seed.py
   ```
3. OR run inside Docker container:
   ```bash
   docker-compose exec web python seed.py
   ```

## 3. Verify Data Storage

### Check MySQL (Relational Data)
- **Tool**: MySQL Workbench
- **Connection**: 
  - Host: `localhost`
  - Port: `3307` (Changed to avoid conflict with local MySQL)
  - User: `root`
  - Password: `password`
- **Tables to check**:
  - `users`: See created users.
  - `products`: Catalog items.
  - `orders`: Transaction records.
  - `inventory`: Stock levels.

### Check MongoDB (NoSQL Logs)
- **Tool**: MongoDB Compass
- **Connection**: `mongodb://localhost:27018`
- **Database**: `inventory_logs`
- **Collection**: `logs`
  - See the JSON documents tracking every API action (Create User, Create Order, etc).
