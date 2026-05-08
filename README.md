# Product CRUD API

A RESTful Product Management API built with FastAPI, MySQL, SQLAlchemy, and Pydantic.

Repository: [E-Commerece_Backend](https://github.com/ZindumKage/E-Commerece_Backend?utm_source=chatgpt.com)

---

# Features

- Create Product
- Get All Products
- Get Single Product
- Update Product
- Delete Product
- MySQL Database Integration
- Input Validation
- Swagger Documentation
- SQLAlchemy ORM
- Environment Variable Support

---

# Tech Stack

- Python
- FastAPI
- MySQL
- SQLAlchemy
- Pydantic
- Alembic
- Uvicorn

---

# Project Structure

```txt
E-Commerece_Backend/
│
├── app/
│   ├── main.py
│   ├── database.py
│   │
│   ├── models/
│   │   └── product.py
│   │
│   ├── schemas/
│   │   └── product.py
│   │
│   ├── crud/
│   │   └── product.py
│   │
│   └── routes/
│       └── product.py
│
├── alembic/
├── requirements.txt
├── .env
├── README.md
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/ZindumKage/E-Commerece_Backend.git

cd E-Commerece_Backend
```

---

## 2. Create Virtual Environment

### Mac/Linux

```bash
python -m venv venv

source venv/bin/activate
```

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/ecommerce_db
```

---

# MySQL Database Setup

Login to MySQL:

```bash
mysql -u root -p
```

Create database:

```sql
CREATE DATABASE ecommerce_db;
```

---

# Run Database Migrations

```bash
alembic upgrade head
```

---

# Run the Application

```bash
uvicorn app.main:app --reload
```

Application runs on:

```txt
http://127.0.0.1:8000
```

---

# Swagger Documentation

Swagger UI:

```txt
http://127.0.0.1:8000/docs
```

ReDoc:

```txt
http://127.0.0.1:8000/redoc
```

---

# Validation Rules

- Product name is required
- Price must be greater than 0
- Stock quantity cannot be negative

---

# API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/products/` | Create Product |
| GET | `/products/` | Get All Products |
| GET | `/products/{id}` | Get Single Product |
| PUT | `/products/{id}` | Update Product |
| DELETE | `/products/{id}` | Delete Product |

---

# Example Request

## Create Product

### Request

```http
POST /products/
```

### Request Body

```json
{
  "name": "iPhone 15",
  "price": 1200,
  "description": "Apple smartphone",
  "stock_quantity": 10
}
```

### Response

```json
{
  "id": 1,
  "name": "iPhone 15",
  "price": 1200,
  "description": "Apple smartphone",
  "stock_quantity": 10
}
```

---

# Swagger Testing

After starting the server, open:

```txt
http://127.0.0.1:8000/docs
```

You can directly test all API endpoints from the Swagger UI.

---


# Author

Stanley Chidindu