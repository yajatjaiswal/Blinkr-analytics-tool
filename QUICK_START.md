# 🚀 Blinkr Analytics Tool - Quick Start Guide

## Prerequisites

Before running the server, make sure you have:

1. **Python 3.8+** installed
2. **Node.js 14+** installed (for Tailwind CSS)
3. **Git** (for cloning the repository)

## Quick Start (Recommended)

The easiest way to start the server is using the automated script:

```bash
./start_server.sh
```

This script will:
- ✅ Activate the virtual environment
- ✅ Install Python dependencies
- ✅ Install Node.js dependencies
- ✅ Build Tailwind CSS
- ✅ Run Django migrations
- ✅ Start the development server

## Manual Setup

If you prefer to run the steps manually:

### 1. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Node.js Dependencies
```bash
cd theme/static_src
npm install
```

### 4. Build Tailwind CSS
```bash
npm run build
cd ../..
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Start the Server
```bash
python manage.py runserver
```

## Accessing the Application

Once the server is running:

- **Main Application**: http://localhost:8000
- **Admin Interface**: http://localhost:8000/admin

## Development Mode

For development with live CSS updates, run Tailwind in watch mode:

```bash
# Terminal 1: Django server
python manage.py runserver

# Terminal 2: Tailwind CSS (in theme/static_src directory)
npm run dev
```

## Troubleshooting

### Common Issues:

1. **Virtual Environment Not Found**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Node.js Not Installed**
   - Download from: https://nodejs.org/
   - Or install via Homebrew: `brew install node`

3. **Port Already in Use**
   ```bash
   python manage.py runserver 8001
   ```

4. **Database Issues**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Project Structure

```
Blinkr-analytics-tool/
├── blinkr_dashboard/     # Django project settings
├── dashboard/           # Main dashboard app
├── theme/              # Tailwind CSS theme
├── templates/          # HTML templates
├── static/            # Static files
├── manage.py          # Django management script
├── start_server.sh    # Quick start script
└── requirements.txt   # Python dependencies
```

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.
