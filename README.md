# Product CRUD API

A RESTful Product Management API built with FastAPI, MySQL, SQLAlchemy, and Pydantic.

Repository: [E-Commerece_Backend](https://github.com/ZindumKage/E-Commerece_Backend?utm_source=chatgpt.com)

---

# Features

## Product Management

- Create Product
- Get All Products
- Get Single Product
- Update Product
- Delete Product

## Authentication & Authorization

- User Signup
- User Login
- User Logout
- JWT Authentication
- Access Token Generation
- Refresh Token Rotation
- Email Verification
- Password Reset via Email
- Redis Token Blacklisting
- Role-Based Access Control (RBAC)

## Roles

### Admin
- Create products
- Update products
- Delete products
- View products

### User
- View products only

## Security Features

- Secure password hashing with bcrypt
- JWT access tokens
- Refresh token rotation
- Refresh token revocation
- Redis blacklist support
- Hashed token storage
- Email verification tokens
- Password reset token expiration
- Protected routes
- Admin-only endpoints

## Additional Features

- MySQL Database Integration
- Input Validation
- Swagger Documentation
- SQLAlchemy ORM
- Alembic Database Migrations
- Environment Variable Support

---

# Tech Stack

- Python
- [FastAPI](chatgpt://generic-entity?number=0)
- [MySQL](chatgpt://generic-entity?number=1)
- [SQLAlchemy](chatgpt://generic-entity?number=2)
- [Pydantic](chatgpt://generic-entity?number=3)
- [Alembic](chatgpt://generic-entity?number=4)
- [Redis](chatgpt://generic-entity?number=5)
- JWT Authentication
- bcrypt
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
│   ├── auth/
│   │   ├── dependencies.py
│   │   ├── hashing.py
│   │   ├── jwt_handler.py
│   │   └── token_hash.py
│   │
│   ├── helper/
│   │   └── time_helper.py
│   │
│   ├── models/
│   │   ├── product.py
│   │   ├── user.py
│   │   └── refresh_token.py
│   │
│   ├── schemas/
│   │   ├── product.py
│   │   └── user.py
│   │
│   ├── crud/
│   │   └── product.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   └── product.py
│   │
│   └── utils/
│       └── mail.py
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

SECRET_KEY=your_secret_key
ALGORITHM=HS256

MAIL_USERNAME=your_mailtrap_username
MAIL_PASSWORD=your_mailtrap_password
MAIL_FROM=test@example.com
MAIL_SERVER=sandbox.smtp.mailtrap.io
MAIL_PORT=2525

REDIS_HOST=localhost
REDIS_PORT=6379

BASE_URL=http://127.0.0.1:8000
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

# Run Redis

```bash
redis-server
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

# Authentication Flow

## 1. Signup

Users create an account using:

```http
POST /auth/signup
```

A verification email is sent after signup.

---

## 2. Verify Email

Users verify email using:

```http
GET /auth/verify/{token}
```

Only verified users can log in.

---

## 3. Login

Users log in using:

```http
POST /auth/login
```

### Login Response

```json
{
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token",
  "token_type": "bearer"
}
```

---

## 4. Access Protected Routes

Protected endpoints require:

```http
Authorization: Bearer <access_token>
```

---

## 5. Refresh Token

Refresh expired access tokens using:

```http
POST /auth/refresh
```

Refresh token rotation is implemented.

---

## 6. Logout

Logout endpoint:

```http
POST /auth/logout
```

Refresh tokens are revoked and blacklisted.

---

## 7. Forgot Password

Request password reset:

```http
POST /auth/forgot-password
```

---

## 8. Reset Password

Reset password using:

```http
POST /auth/reset-password/{token}
```

---

# Validation Rules

## Product Validation

- Product name is required
- Price must be greater than 0
- Stock quantity cannot be negative

## Authentication Validation

- Email must be unique
- Passwords are securely hashed
- Verification tokens expire after 24 hours
- Reset tokens expire after 1 hour
- Refresh tokens expire after 3 days

---

# Route Protection

## Authenticated Routes

Only authenticated users can access protected endpoints.

Example:

```python
Depends(get_current_user)
```

---

## Admin Routes

Only admins can modify products.

Example:

```python
Depends(require_admin)
```

---

# API Endpoints

## Authentication Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/signup` | Register User |
| POST | `/auth/login` | Login User |
| POST | `/auth/logout` | Logout User |
| POST | `/auth/refresh` | Refresh Access Token |
| GET | `/auth/verify/{token}` | Verify Email |
| POST | `/auth/forgot-password` | Request Password Reset |
| POST | `/auth/reset-password/{token}` | Reset Password |

---

## Product Endpoints

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/products/` | Admin | Create Product |
| GET | `/products/` | User/Admin | Get All Products |
| GET | `/products/{id}` | User/Admin | Get Single Product |
| PUT | `/products/{id}` | Admin | Update Product |
| DELETE | `/products/{id}` | Admin | Delete Product |

---

# Example Request

## Create Product

### Request

```http
POST /products/
```

### Headers

```http
Authorization: Bearer <access_token>
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