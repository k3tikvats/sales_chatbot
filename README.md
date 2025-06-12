# E-commerce Sales Chatbot

A comprehensive e-commerce sales chatbot built with React frontend and Flask backend, featuring intelligent product search, user authentication, and seamless shopping experience.

## Project Overview

This project implements a full-stack e-commerce chatbot solution that enables customers to search, explore, and purchase products through natural language interactions. The system includes a responsive web interface, secure authentication, session management, and a RESTful API backend with a mock product database.

## Technology Stack

### Frontend

- **React 18** - Modern JavaScript framework for building user interfaces
- **TypeScript** - Type-safe JavaScript for better code quality
- **Tailwind CSS** - Utility-first CSS framework for responsive design
- **Axios** - HTTP client for API communication
- **React Router** - Client-side routing
- **React Context API** - State management for authentication and chat

### Backend

- **Python 3.9+** - Programming language
- **Flask** - Lightweight web framework
- **Flask-SQLAlchemy** - ORM for database operations
- **Flask-JWT-Extended** - JWT authentication
- **Flask-CORS** - Cross-origin resource sharing
- **SQLite** - Database for development (easily switchable to PostgreSQL/MySQL)
- **Marshmallow** - Serialization/deserialization

### Additional Tools

- **Google Gemini AI** - For intelligent chatbot responses and natural language processing
- **Faker** - For generating mock data
- **pytest** - Testing framework

## Features

### User Interface

- ✅ Responsive design (desktop, tablet, mobile)
- ✅ Modern, intuitive chatbot interface
- ✅ User authentication and registration
- ✅ Session management with timestamps
- ✅ Chat history storage and retrieval
- ✅ Conversation reset functionality
- ✅ Product visualization and filtering
- ✅ Real-time typing indicators

### Backend

- ✅ RESTful API architecture
- ✅ 100+ mock product entries
- ✅ Advanced search and filtering
- ✅ User session management
- ✅ Chat history persistence
- ✅ Product recommendation engine
- ✅ Order processing simulation

### Security

- ✅ JWT-based authentication
- ✅ Password hashing
- ✅ CORS configuration
- ✅ Input validation and sanitization

## Project Structure

```
e-commerce_sales_chatbot/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── migrations/
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── contexts/
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── services/
│   │   └── types/
│   ├── package.json
│   └── tailwind.config.js
├── docs/
├── tests/
└── README.md
```

## 🚀 Quick Start

### Automated Setup (Recommended)

**Windows:**

```bash
# Run the setup script
setup.bat

# Start the application
start-app.bat
```

**Linux/Mac:**

```bash
# Make scripts executable and run setup
chmod +x setup.sh
./setup.sh

# Start backend and frontend manually (see below)
```

### Manual Start

**Start Backend:**

```bash
# Windows
start-backend.bat

# Linux/Mac
cd backend
source venv/bin/activate
python run.py
```

**Start Frontend:**

```bash
# Windows
start-frontend.bat

# Linux/Mac
cd frontend
npm start
```

### Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5000
- **API Documentation:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

### Test Accounts

- **Admin:** admin@example.com / password123
- **User:** user@example.com / password123

## Setup Instructions

### Prerequisites

- Node.js 16+ and npm
- Python 3.9+
- Git

### Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create and activate virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Initialize database:

```bash
python run.py init-db
```

5. Run the Flask server:

```bash
python run.py
```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user

### Products

- `GET /api/products` - Get all products with filtering
- `GET /api/products/{id}` - Get specific product
- `GET /api/products/search` - Search products
- `GET /api/products/categories` - Get product categories

### Chat

- `POST /api/chat/message` - Send chat message
- `GET /api/chat/history` - Get chat history
- `DELETE /api/chat/reset` - Reset chat session

### Orders

- `POST /api/orders` - Create new order
- `GET /api/orders` - Get user orders
- `GET /api/orders/{id}` - Get specific order

## Architecture Decisions

### Framework Choices

**Flask vs Django**:

- Chose Flask for its lightweight nature and flexibility
- Better suited for API-focused applications
- Easier to integrate with different frontend frameworks

**React vs Vue/Angular**:

- React's component-based architecture aligns well with chatbot UI
- Large ecosystem and community support
- TypeScript integration for better development experience

**SQLite vs PostgreSQL**:

- SQLite for development simplicity
- Easy migration path to PostgreSQL for production

### Design Patterns

1. **Repository Pattern**: Separates data access logic from business logic
2. **Service Layer**: Encapsulates business logic
3. **Factory Pattern**: For creating different types of chat responses
4. **Observer Pattern**: For real-time updates in chat interface

## Mock Data

The database is populated with 100+ products across categories:

- Electronics (smartphones, laptops, headphones)
- Books (fiction, non-fiction, textbooks)
- Clothing (men's, women's, accessories)
- Home & Garden (furniture, appliances, decor)

Each product includes:

- Name, description, price
- Category and subcategory
- Stock quantity
- Images and ratings
- Specifications

## Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Challenges and Solutions

### 1. Natural Language Processing

**Challenge**: Understanding user intent from natural language queries
**Solution**: Implemented keyword extraction and intent classification system with fallback to GPT integration

### 2. Real-time Chat Experience

**Challenge**: Creating smooth, responsive chat interactions
**Solution**: Implemented optimistic UI updates and proper error handling with retry mechanisms

### 3. Product Search Optimization

**Challenge**: Efficient product search across multiple attributes
**Solution**: Implemented full-text search with ranking and fuzzy matching

### 4. Session Management

**Challenge**: Maintaining chat context across sessions
**Solution**: JWT tokens with proper expiration and refresh token mechanism

## Future Enhancements

1. **AI Integration**: OpenAI GPT for more sophisticated natural language understanding
2. **Real-time Features**: WebSocket integration for live chat support
3. **Analytics**: User behavior tracking and recommendation improvements
4. **Mobile App**: React Native mobile application
5. **Multi-language**: Internationalization support
6. **Voice Interface**: Speech-to-text integration

## Performance Considerations

- Database indexing for fast product searches
- Pagination for large result sets
- Caching frequently accessed data
- Image optimization and CDN integration
- Code splitting for faster frontend loading

## Security Measures

- Password hashing with bcrypt
- JWT token validation
- SQL injection prevention
- XSS protection
- Rate limiting on API endpoints
- Input validation and sanitization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please contact the development team.
