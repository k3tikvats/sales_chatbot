# Deployment Guide

## E-commerce Sales Chatbot Deployment

This guide covers deploying the E-commerce Sales Chatbot to various platforms.

## Prerequisites

- Python 3.8+ (for backend)
- Node.js 16+ (for frontend)
- PostgreSQL or MySQL (for production database)
- Redis (optional, for session storage)

## Environment Setup

### Backend Environment Variables

Create a `.env` file in the backend directory:

```env
# Production Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-very-secure-secret-key-here
JWT_SECRET_KEY=your-very-secure-jwt-secret-key-here

# Database Configuration (PostgreSQL example)
DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce_chatbot

# OR for MySQL
# DATABASE_URL=mysql://username:password@localhost:3306/ecommerce_chatbot

# Chat Configuration
OPENAI_API_KEY=your-openai-api-key-here
CHAT_MODEL=gpt-3.5-turbo
MAX_CONVERSATION_HISTORY=20

# CORS Configuration
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Email Configuration (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379/0

# Pagination
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
```

### Frontend Environment Variables

Create a `.env.production` file in the frontend directory:

```env
REACT_APP_API_URL=https://your-api-domain.com/api
REACT_APP_NAME=ShopBot E-commerce Chatbot
REACT_APP_VERSION=1.0.0
GENERATE_SOURCEMAP=false
```

## Database Setup

### PostgreSQL Setup

1. Install PostgreSQL:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql
brew services start postgresql

# Windows
# Download from https://www.postgresql.org/download/windows/
```

2. Create database and user:

```sql
-- Connect to PostgreSQL as superuser
sudo -u postgres psql

-- Create database
CREATE DATABASE ecommerce_chatbot;

-- Create user
CREATE USER chatbot_user WITH PASSWORD 'secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE ecommerce_chatbot TO chatbot_user;

-- Exit
\q
```

3. Update DATABASE_URL in your .env file:

```env
DATABASE_URL=postgresql://chatbot_user:secure_password@localhost:5432/ecommerce_chatbot
```

### MySQL Setup

1. Install MySQL:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server

# macOS
brew install mysql
brew services start mysql

# Windows
# Download from https://dev.mysql.com/downloads/mysql/
```

2. Create database and user:

```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create database
CREATE DATABASE ecommerce_chatbot;

-- Create user
CREATE USER 'chatbot_user'@'localhost' IDENTIFIED BY 'secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON ecommerce_chatbot.* TO 'chatbot_user'@'localhost';
FLUSH PRIVILEGES;

-- Exit
EXIT;
```

## Deployment Options

### Option 1: Traditional VPS/Server Deployment

#### Backend Deployment

1. **Install dependencies:**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Install Nginx and Supervisor
sudo apt install nginx supervisor
```

2. **Setup application:**

```bash
# Clone repository
git clone https://github.com/yourusername/ecommerce-chatbot.git
cd ecommerce-chatbot/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Setup environment
cp .env.example .env
# Edit .env with your production values
```

3. **Initialize database:**

```bash
python init_db.py
```

4. **Configure Gunicorn:**

Create `/etc/supervisor/conf.d/ecommerce-chatbot.conf`:

```ini
[program:ecommerce-chatbot]
command=/path/to/your/project/backend/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 run:app
directory=/path/to/your/project/backend
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/ecommerce-chatbot.log
```

5. **Configure Nginx:**

Create `/etc/nginx/sites-available/ecommerce-chatbot`:

```nginx
server {
    listen 80;
    server_name your-api-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/ecommerce-chatbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl restart supervisor
```

#### Frontend Deployment

1. **Build the application:**

```bash
cd frontend
npm install
npm run build
```

2. **Configure Nginx for frontend:**

Create `/etc/nginx/sites-available/ecommerce-chatbot-frontend`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    root /path/to/your/project/frontend/build;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/ecommerce-chatbot-frontend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Option 2: Docker Deployment

#### Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "run:app"]
```

#### Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
# Build stage
FROM node:18-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose

Create `docker-compose.yml`:

```yaml
version: "3.8"

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: ecommerce_chatbot
      POSTGRES_USER: chatbot_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://chatbot_user:secure_password@postgres:5432/ecommerce_chatbot
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    ports:
      - "5000:5000"

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

Deploy with Docker:

```bash
docker-compose up -d
```

### Option 3: Cloud Platform Deployment

#### Heroku Deployment

1. **Backend setup:**

Create `backend/Procfile`:

```
web: gunicorn run:app
release: python init_db.py
```

Create `backend/runtime.txt`:

```
python-3.11.8
```

Deploy:

```bash
# Install Heroku CLI
# Create Heroku app
heroku create your-app-name-api

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key
heroku config:set JWT_SECRET_KEY=your-jwt-secret
heroku config:set OPENAI_API_KEY=your-openai-key

# Deploy
git subtree push --prefix backend heroku main
```

2. **Frontend setup (Netlify):**

Build command: `npm run build`
Publish directory: `build`
Environment variables: Set in Netlify dashboard

#### AWS Deployment

1. **Backend (AWS Elastic Beanstalk):**

```bash
# Install EB CLI
pip install awsebcli

# Initialize EB application
eb init

# Create environment
eb create production

# Deploy
eb deploy
```

2. **Frontend (AWS S3 + CloudFront):**

```bash
# Build application
npm run build

# Upload to S3
aws s3 sync build/ s3://your-bucket-name --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```

## SSL/HTTPS Setup

### Using Let's Encrypt (Certbot)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Generate SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
sudo certbot --nginx -d your-api-domain.com

# Auto-renewal (add to crontab)
0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoring and Maintenance

### Health Checks

Add health check endpoints to your backend:

```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

### Logging

Configure proper logging in production:

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/ecommerce_chatbot.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### Database Backups

Set up automated database backups:

```bash
# PostgreSQL backup script
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U chatbot_user ecommerce_chatbot > $BACKUP_DIR/backup_$DATE.sql

# Keep only last 30 days
find $BACKUP_DIR -name "backup_*.sql" -mtime +30 -delete
```

## Performance Optimization

1. **Database indexing:** Ensure proper indexes on frequently queried columns
2. **Caching:** Implement Redis caching for frequently accessed data
3. **CDN:** Use CloudFront or similar for static assets
4. **Database connection pooling:** Configure proper connection pooling
5. **API rate limiting:** Implement rate limiting to prevent abuse

## Security Best Practices

1. **Environment variables:** Never commit sensitive data to version control
2. **HTTPS:** Always use HTTPS in production
3. **Database security:** Use strong passwords and restrict database access
4. **CORS:** Configure CORS properly for your domain
5. **Input validation:** Validate all user inputs
6. **Security headers:** Add security headers in Nginx/Apache configuration
7. **Regular updates:** Keep all dependencies updated

## Troubleshooting

### Common Issues

1. **Database connection errors:** Check DATABASE_URL and database server status
2. **CORS errors:** Verify CORS_ORIGINS setting
3. **Build failures:** Check Node.js/Python versions and dependencies
4. **SSL issues:** Verify certificate installation and renewal

### Logs Locations

- Application logs: `/var/log/ecommerce-chatbot.log`
- Nginx logs: `/var/log/nginx/access.log`, `/var/log/nginx/error.log`
- System logs: `/var/log/syslog`

For additional support, check the main README.md file or create an issue in the project repository.
