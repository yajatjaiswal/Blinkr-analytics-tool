#!/bin/bash

# Blinkr Analytics Tool - Quick Start Script
echo "🚀 Starting Blinkr Analytics Tool..."

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
if [ ! -f "manage.py" ]; then
    print_error "Please run this script from the Blinkr-analytics-tool directory"
    exit 1
fi

# Step 1: Check if virtual environment exists
print_status "Checking virtual environment..."
if [ ! -d "venv" ]; then
    print_error "Virtual environment not found. Please create one first:"
    echo "python3 -m venv venv"
    exit 1
fi

# Step 2: Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment"
    exit 1
fi
print_success "Virtual environment activated"

# Step 3: Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    print_error "Failed to install Python dependencies"
    exit 1
fi
print_success "Python dependencies installed"

# Step 4: Check if Node.js is installed
print_status "Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js first:"
    echo "Visit: https://nodejs.org/"
    exit 1
fi
print_success "Node.js found: $(node --version)"

# Step 5: Install Node.js dependencies
print_status "Installing Node.js dependencies..."
cd theme/static_src
npm install
if [ $? -ne 0 ]; then
    print_error "Failed to install Node.js dependencies"
    exit 1
fi
print_success "Node.js dependencies installed"

# Step 6: Build Tailwind CSS
print_status "Building Tailwind CSS..."
npm run build
if [ $? -ne 0 ]; then
    print_error "Failed to build Tailwind CSS"
    exit 1
fi
print_success "Tailwind CSS built successfully"

# Step 7: Return to project root
cd ../..

# Step 8: Run Django migrations
print_status "Running Django migrations..."
python manage.py migrate
if [ $? -ne 0 ]; then
    print_error "Failed to run migrations"
    exit 1
fi
print_success "Migrations completed"

# Step 9: Check if superuser exists
print_status "Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
if User.objects.filter(is_superuser=True).exists():
    print('Superuser exists')
else:
    print('No superuser found. You can create one with: python manage.py createsuperuser')
"

# Step 10: Start the development server
print_success "🎉 All setup complete! Starting development server..."
echo ""
echo "🌐 Server will be available at: http://localhost:8000"
echo "🔧 Admin interface: http://localhost:8000/admin"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver
