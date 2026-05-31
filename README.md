# Product CRUD API

A RESTful Product Management API built with FastAPI, MySQL, SQLAlchemy, Pydantic, JWT Authentication, Order Management, and Flutterwave Payment Integration.

Repository: https://github.com/ZindumKage/E-Commerece_Backend

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
- Create orders
- View orders
- Make payments

## Order Management

- Create Orders
- View User Orders
- View Single Order
- Multi-Product Orders
- Automatic Total Price Calculation
- Order Status Management
- Stock Quantity Validation
- Stock Quantity Reduction

## Payment Integration

- Flutterwave Payment Integration
- Payment Initialization
- Payment Verification
- Webhook Verification
- Transaction Reference Tracking
- Duplicate Payment Prevention
- Automatic Order Status Updates
- Sandbox Payment Testing

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
- Structured Logging
- Error Handling
- Service Layer Architecture
- Controller Layer Architecture

---

# Tech Stack

- Python
- FastAPI
- MySQL
- SQLAlchemy
- Pydantic
- Alembic
- Redis
- JWT Authentication
- bcrypt
- Flutterwave
- ngrok
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
│   ├── controllers/
│   │   ├── order.py
│   │   └── payment.py
│   │
│   ├── services/
│   │   ├── order.py
│   │   ├── payment.py
│   │   └── flutterwave.py
│   │
│   ├── helper/
│   │   └── time_helper.py
│   │
│   ├── core/
│   │   └── logger.py
│   │
│   ├── models/
│   │   ├── product.py
│   │   ├── user.py
│   │   ├── refresh_token.py
│   │   ├── order.py
│   │   └── order_item.py
│   │
│   ├── schemas/
│   │   ├── product.py
│   │   ├── user.py
│   │   └── order.py
│   │
│   ├── crud/
│   │   └── product.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── payment.py
│   │   └── webhook.py
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

FLUTTERWAVE_SECRET_KEY=your_flutterwave_secret_key
FLUTTERWAVE_PUBLIC_KEY=your_flutterwave_public_key
FLUTTERWAVE_BASE_URL=https://api.flutterwave.com/v3

FLUTTERWAVE_SECRET_HASH=your_webhook_secret_hash
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

# Order Lifecycle

```txt
Pending → Paid / Failed
```

### Workflow

1. User creates order
2. System calculates total price
3. Payment is initialized
4. Flutterwave checkout page opens
5. User completes payment
6. Flutterwave triggers webhook
7. Backend verifies payment
8. Order status updates automatically

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

## Order Validation

- Product must exist
- Quantity must be greater than 0
- Product stock must be available
- Total price is calculated automatically

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

## Order Endpoints

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/orders/` | Authenticated User | Create Order |
| GET | `/orders/my-orders` | Authenticated User | Get User Orders |
| GET | `/orders/{order_id}` | Authenticated User | Get Single Order |

---

## Payment Endpoints

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/payments/initialize/{order_id}` | Authenticated User | Initialize Payment |
| GET | `/payments/verify/{tx_ref}` | Public | Verify Payment |
| POST | `/webhooks/flutterwave` | Flutterwave | Flutterwave Webhook |

---

# Flutterwave Setup

Create a Flutterwave account.

Get your test API keys from the Flutterwave dashboard.

---

# Webhook Setup

Expose your local server using ngrok:

```bash
ngrok http 8000
```

Example:

```txt
https://abcd1234.ngrok-free.app
```

Set Flutterwave webhook URL:

```txt
https://abcd1234.ngrok-free.app/webhooks/flutterwave
```

---

# Payment Verification Flow

Flutterwave redirects after payment:

```txt
/payment-success?status=successful&tx_ref=xxx&transaction_id=xxx
```

Backend verification endpoint:

```http
GET /payments/verify/{tx_ref}?transaction_id=123456
```

Verification checks:

- Payment status
- Transaction reference validation
- Amount validation
- Duplicate payment prevention

---

# Logging & Error Handling

The backend includes:

- Structured logging
- HTTP exception handling
- Database validation
- Authentication validation
- Payment validation
- Webhook validation
- Stock validation
- Duplicate payment protection

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

# Example Order Request

## Create Order

### Request

```http
POST /orders/
```

### Headers

```http
Authorization: Bearer <access_token>
```

### Request Body

```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 1
    },
    {
      "product_id": 2,
      "quantity": 2
    }
  ]
}
```

### Response

```json
{
  "id": 5,
  "user_id": 1,
  "total_price": 3250000,
  "status": "pending"
}
```

---

# Example Payment Initialization

## Request

```http
POST /payments/initialize/5
```

## Response

```json
{
  "payment_link": "https://checkout.flutterwave.com/...",
  "tx_ref": "uuid-reference"
}
```

---

# Example Payment Verification

## Request

```http
GET /payments/verify/{tx_ref}?transaction_id=123456
```

## Response

```json
{
  "message": "Payment verified successfully",
  "order_id": 5,
  "payment_status": "paid"
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