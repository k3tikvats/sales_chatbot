import os
import sys
from flask import Flask
from app import create_app, db

def init_database():
    """Initialize database with sample data"""
    from app.utils.sample_data import create_sample_data
    
    print("Initializing database...")
    
    # Create all tables
    db.create_all()
    print("Database tables created.")
    
    # Create sample data
    create_sample_data()
    print("Sample data created successfully!")

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    if len(sys.argv) > 1 and sys.argv[1] == 'init-db':
        with app.app_context():
            init_database()
    else:
        print("Starting Flask development server...")
        print("API will be available at: http://localhost:5000")
        print("API documentation at: http://localhost:5000/api/health")
        app.run(host='0.0.0.0', port=5000, debug=True)
