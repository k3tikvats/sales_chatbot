#!/bin/bash

# E-commerce Chatbot Setup Script
# This script sets up the complete development environment

echo "🚀 Setting up E-commerce Sales Chatbot..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_status "Starting setup process..."

# Setup Backend
print_status "Setting up backend..."
cd backend

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate || venv\Scripts\activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Create environment file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file from template..."
    cp .env.example .env
    print_warning "Please update .env file with your actual configuration values"
fi

# Initialize database
print_status "Initializing database..."
python init_db.py

cd ..

# Setup Frontend
print_status "Setting up frontend..."
cd frontend

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 16+ and try again."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm and try again."
    exit 1
fi

# Install dependencies
print_status "Installing Node.js dependencies..."
npm install

# Create environment file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file from template..."
    cp .env.example .env
fi

cd ..

print_success "Setup completed successfully! 🎉"
echo ""
echo "📋 Next Steps:"
echo "1. Update backend/.env with your configuration (database, API keys, etc.)"
echo "2. Update frontend/.env if needed"
echo "3. Start the backend server: cd backend && source venv/bin/activate && python run.py"
echo "4. Start the frontend server: cd frontend && npm start"
echo ""
echo "🌐 Application URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:5000"
echo ""
echo "👤 Test Accounts:"
echo "   Admin: admin@example.com / password123"
echo "   User: user@example.com / password123"
