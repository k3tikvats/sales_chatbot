#!/usr/bin/env python3
"""
Database initialization script for E-commerce Chatbot
Run this script to set up the database and populate it with sample data.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app import create_app, db
from app.utils.sample_data import populate_sample_data


def init_database():
    """Initialize the database with tables and sample data."""
    print("🚀 Initializing E-commerce Chatbot Database...")
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Drop all tables (for clean setup)
            print("📦 Dropping existing tables...")
            db.drop_all()
            
            # Create all tables
            print("🔨 Creating database tables...")
            db.create_all()
            
            # Populate with sample data
            print("📚 Populating with sample data...")
            populate_sample_data()
            
            print("✅ Database initialization completed successfully!")
            print("\n📊 Database Summary:")
            print(f"   • Database file: {app.config['SQLALCHEMY_DATABASE_URI']}")
            print(f"   • Tables created: Users, Products, Categories, ChatSessions, ChatMessages, Orders, OrderItems")
            print(f"   • Sample data: 100+ products across multiple categories")
            print(f"   • Test users: admin@example.com / user@example.com")
            
        except Exception as e:
            print(f"❌ Error initializing database: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    init_database()
