# API Documentation

## E-commerce Sales Chatbot API

Base URL: `http://localhost:5000/api`

### Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Authentication Endpoints

### POST /auth/register

Register a new user account.

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

**Response:**

```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### POST /auth/login

Authenticate user and get access token.

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### GET /auth/profile

Get current user profile (requires authentication).

**Response:**

```json
{
  "success": true,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

## Product Endpoints

### GET /products

Get list of products with optional filtering and pagination.

**Query Parameters:**

- `page` (int): Page number (default: 1)
- `per_page` (int): Items per page (default: 20, max: 100)
- `category_id` (int): Filter by category ID
- `search` (string): Search in product name and description
- `min_price` (float): Minimum price filter
- `max_price` (float): Maximum price filter
- `sort` (string): Sort by field (name, price, created_at)
- `order` (string): Sort order (asc, desc)

**Response:**

```json
{
  "success": true,
  "products": [
    {
      "id": 1,
      "name": "iPhone 14 Pro",
      "description": "Latest Apple smartphone with advanced features",
      "price": 999.99,
      "stock_quantity": 50,
      "image_url": "https://example.com/iphone14pro.jpg",
      "category": {
        "id": 1,
        "name": "Electronics",
        "description": "Electronic devices and gadgets"
      },
      "specifications": {
        "color": "Space Black",
        "storage": "256GB",
        "camera": "48MP Pro camera system"
      },
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "pages": 8
  }
}
```

### GET /products/{id}

Get detailed information about a specific product.

**Response:**

```json
{
  "success": true,
  "product": {
    "id": 1,
    "name": "iPhone 14 Pro",
    "description": "Latest Apple smartphone with advanced features",
    "price": 999.99,
    "stock_quantity": 50,
    "image_url": "https://example.com/iphone14pro.jpg",
    "category": {
      "id": 1,
      "name": "Electronics",
      "description": "Electronic devices and gadgets"
    },
    "specifications": {
      "color": "Space Black",
      "storage": "256GB",
      "camera": "48MP Pro camera system",
      "display": "6.1-inch Super Retina XDR",
      "chip": "A16 Bionic"
    },
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

### GET /products/categories

Get list of all product categories.

**Response:**

```json
{
  "success": true,
  "categories": [
    {
      "id": 1,
      "name": "Electronics",
      "description": "Electronic devices and gadgets",
      "product_count": 45
    },
    {
      "id": 2,
      "name": "Clothing",
      "description": "Fashion and apparel",
      "product_count": 78
    }
  ]
}
```

## Chat Endpoints

### GET /chat/sessions

Get user's chat sessions (requires authentication).

**Response:**

```json
{
  "success": true,
  "sessions": [
    {
      "id": "session_123",
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:30:00Z",
      "message_count": 15,
      "last_message_preview": "Thank you for helping me find the perfect laptop!"
    }
  ]
}
```

### POST /chat/sessions

Create a new chat session (requires authentication).

**Response:**

```json
{
  "success": true,
  "session": {
    "id": "session_456",
    "created_at": "2024-01-01T11:00:00Z"
  }
}
```

### GET /chat/sessions/{session_id}/messages

Get messages from a specific chat session (requires authentication).

**Response:**

```json
{
  "success": true,
  "messages": [
    {
      "id": 1,
      "content": "Hi! I'm looking for a new laptop for work.",
      "sender": "user",
      "timestamp": "2024-01-01T10:00:00Z"
    },
    {
      "id": 2,
      "content": "I'd be happy to help you find the perfect laptop! What's your budget and main use case?",
      "sender": "assistant",
      "timestamp": "2024-01-01T10:00:30Z"
    }
  ],
  "session_id": "session_123"
}
```

### POST /chat/sessions/{session_id}/messages

Send a message in a chat session (requires authentication).

**Request Body:**

```json
{
  "content": "I need a laptop under $1000 for programming and design work."
}
```

**Response:**

```json
{
  "success": true,
  "user_message": {
    "id": 3,
    "content": "I need a laptop under $1000 for programming and design work.",
    "sender": "user",
    "timestamp": "2024-01-01T10:05:00Z"
  },
  "assistant_response": {
    "id": 4,
    "content": "Based on your requirements, I recommend checking out these laptops...",
    "sender": "assistant",
    "timestamp": "2024-01-01T10:05:15Z",
    "suggested_products": [
      {
        "id": 25,
        "name": "Dell XPS 13",
        "price": 899.99,
        "image_url": "https://example.com/dell-xps13.jpg"
      }
    ]
  }
}
```

## Order Endpoints

### GET /orders

Get user's order history (requires authentication).

**Query Parameters:**

- `page` (int): Page number (default: 1)
- `per_page` (int): Items per page (default: 20)
- `status` (string): Filter by order status

**Response:**

```json
{
  "success": true,
  "orders": [
    {
      "id": 1,
      "total_amount": 1299.98,
      "status": "completed",
      "created_at": "2024-01-01T00:00:00Z",
      "items": [
        {
          "id": 1,
          "product": {
            "id": 1,
            "name": "iPhone 14 Pro",
            "image_url": "https://example.com/iphone14pro.jpg"
          },
          "quantity": 1,
          "price": 999.99
        }
      ]
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 5,
    "pages": 1
  }
}
```

### POST /orders

Create a new order (requires authentication).

**Request Body:**

```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 3,
      "quantity": 1
    }
  ]
}
```

**Response:**

```json
{
  "success": true,
  "message": "Order created successfully",
  "order": {
    "id": 2,
    "total_amount": 2299.97,
    "status": "pending",
    "created_at": "2024-01-01T12:00:00Z",
    "items": [
      {
        "id": 1,
        "product": {
          "id": 1,
          "name": "iPhone 14 Pro"
        },
        "quantity": 2,
        "price": 999.99
      }
    ]
  }
}
```

### GET /orders/{id}

Get detailed information about a specific order (requires authentication).

**Response:**

```json
{
  "success": true,
  "order": {
    "id": 1,
    "total_amount": 1299.98,
    "status": "completed",
    "created_at": "2024-01-01T00:00:00Z",
    "items": [
      {
        "id": 1,
        "product": {
          "id": 1,
          "name": "iPhone 14 Pro",
          "description": "Latest Apple smartphone",
          "image_url": "https://example.com/iphone14pro.jpg"
        },
        "quantity": 1,
        "price": 999.99
      }
    ]
  }
}
```

## Error Responses

All endpoints return errors in the following format:

```json
{
  "success": false,
  "message": "Error description",
  "error": "ERROR_CODE"
}
```

### Common Error Codes

- `VALIDATION_ERROR`: Invalid request data
- `AUTHENTICATION_REQUIRED`: Missing or invalid authentication token
- `AUTHORIZATION_FAILED`: Insufficient permissions
- `RESOURCE_NOT_FOUND`: Requested resource doesn't exist
- `INTERNAL_SERVER_ERROR`: Server-side error

### HTTP Status Codes

- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Unprocessable Entity
- `500`: Internal Server Error
