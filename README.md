# Cloud-Native Inventory & Order Management System

A robust, containerized full-stack application for managing inventory, orders, and users.
This system leverages both **SQL (MySQL)** for structured transactional data and **NoSQL (MongoDB)** for flexible logging and activity tracking.

## Features
- **User Management**: Create, Read, Update, Delete users.
- **Product & Inventory**: Manage product catalog and stock levels.
- **Order Processing**: Create orders with complex item structures.
- **Activity Logging**: All significant actions are logged to MongoDB for audit trails.
- **Dual-Database Architecture**: Demonstrates hybrid data storage (SQL + NoSQL).
- **Containerization**: Fully dockerized environment using Docker Compose.
- **CI/CD**: GitHub Actions workflow for automated testing and building.

## Tech Stack
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Backend**: Python (Flask)
- **Databases**: 
  - MySQL (Transactional Data)
  - MongoDB (Logs & Activity Stream)
- **Infrastructure**: Docker, Docker Compose

## Setup
### Local Development
1. Install dependencies: `pip install -r requirements.txt`
2. Configure `.env` file with database credentials.
3. Run the application: `python src/app.py`

### Docker (Cloud-Native)
1. Run: `docker-compose up --build`
2. Access at `http://localhost:5000`

## API Endpoints
- `/api/users`
- `/api/products`
- `/api/orders`
- `/api/logs`

## Professional Note
This project implementation successfully integrates relational (MySQL) and non-relational (MongoDB) databases to handle different aspects of data management efficiently. You can verify data persistence by checking the tables in MySQL Workbench and collections in MongoDB Compass/Shell.
