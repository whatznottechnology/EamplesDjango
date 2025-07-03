# Installation Guide

This guide provides step-by-step instructions for setting up the Examples project both locally and on cPanel.

## Table of Contents
- [Local Development Setup](#local-development-setup)
- [cPanel Deployment](#cpanel-deployment)
- [Common Issues](#common-issues)

## Local Development Setup

### Prerequisites
- Python 3.9 or higher
- Node.js 14 or higher
- MySQL 8.0 or higher

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd examples
```

### Step 2: Set Up Python Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Node.js Dependencies
```bash
npm install
```

### Step 5: Set Up Database
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE examples_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'examples_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON examples_db.* TO 'examples_user'@'localhost';
FLUSH PRIVILEGES;
```

### Step 6: Configure Environment
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=examples_db
DB_USER=examples_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### Step 7: Initialize Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Step 8: Build Static Files
```bash
npm run build-css
python manage.py collectstatic
```

### Step 9: Run Development Server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see the site.

## cPanel Deployment

### Prerequisites
- cPanel hosting account
- Python selector enabled
- Domain pointed to your hosting

### Step 1: Create Database in cPanel
1. Log in to cPanel
2. Go to "MySQL Databases"
3. Create a new database: `whatznotc_examples`
4. Create a new user: `whatznotc_examples`
5. Add user to database with all privileges

### Step 2: Set Up Python App
1. In cPanel, go to "Setup Python App"
2. Click "Create Application"
3. Configure:
   - Python version: 3.9
   - Application root: /home/username/examples.whatznot.com
   - Application URL: examples.whatznot.com
   - Application startup file: passenger_wsgi.py
   - Application Entry point: application
   - Environment: production

### Step 3: Upload Files
Using File Manager or FTP:
1. Upload all project files to /home/username/examples.whatznot.com
2. Set permissions:
```bash
chmod 755 /home/username/examples.whatznot.com
chmod 755 /home/username/examples.whatznot.com/static
chmod 755 /home/username/examples.whatznot.com/media
chmod 755 /home/username/examples.whatznot.com/logs
chmod 644 /home/username/examples.whatznot.com/db.sqlite3
```

### Step 4: Install Dependencies
In SSH Terminal:
```bash
cd /home/username/examples.whatznot.com
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 5: Configure Production Settings
Update examples/production_settings.py:
1. Set ALLOWED_HOSTS
2. Configure database credentials
3. Set up email settings
4. Generate new SECRET_KEY

### Step 6: Initialize Application
```bash
python manage.py collectstatic --noinput --settings=examples.production_settings
python manage.py migrate --settings=examples.production_settings
python manage.py createsuperuser --settings=examples.production_settings
```

### Step 7: Set Up SSL
1. In cPanel, go to "SSL/TLS"
2. Install Let's Encrypt SSL for your domain
3. Force HTTPS in .htaccess

### Step 8: Final Configuration
1. Set up cron jobs for periodic tasks
2. Configure backup settings
3. Test all functionality

## Common Issues

### Local Development

1. Database Connection Error
```
Check MySQL service is running
Verify database credentials in .env
```

2. Static Files Not Loading
```
Run: python manage.py collectstatic
Check STATIC_ROOT and STATIC_URL settings
```

3. Image Upload Issues
```
Check media folder permissions
Verify Pillow installation
```

### cPanel Deployment

1. 503 Service Unavailable
```
Check application logs
Verify passenger_wsgi.py configuration
Restart Python application
```

2. Static/Media Files Not Loading
```
Check file permissions
Verify .htaccess configuration
Check static and media folders exist
```

3. Database Connection Issues
```
Verify database credentials
Check database user privileges
Ensure MySQL service is running
```

## Maintenance

### Regular Updates
```bash
# Local
git pull
pip install -r requirements.txt
python manage.py migrate
npm install
npm run build-css

# Production
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --settings=examples.production_settings
python manage.py collectstatic --noinput --settings=examples.production_settings
touch passenger_wsgi.py  # Restart application
```

### Backup
1. Database: Regular MySQL dumps
2. Media files: Regular file backups
3. Configuration files: Version control

## Security Checklist
- [ ] Change default admin URL
- [ ] Set strong database passwords
- [ ] Enable SSL
- [ ] Configure proper file permissions
- [ ] Set secure SECRET_KEY
- [ ] Enable CSRF protection
- [ ] Configure secure cookie settings
- [ ] Set up backup system
- [ ] Configure error logging 