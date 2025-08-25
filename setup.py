#!/usr/bin/env python3
"""
Setup script for BLINKRLOAN DASHBOARD
This script helps with initial project setup and configuration.
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    if os.path.exists("venv"):
        print("✅ Virtual environment already exists")
        return True
    
    print("🔄 Creating virtual environment...")
    if run_command("python -m venv venv", "Creating virtual environment"):
        print("✅ Virtual environment created successfully")
        return True
    return False

def activate_virtual_environment():
    """Provide instructions for activating virtual environment"""
    if platform.system() == "Windows":
        print("\n📋 To activate the virtual environment, run:")
        print("   venv\\Scripts\\activate")
    else:
        print("\n📋 To activate the virtual environment, run:")
        print("   source venv/bin/activate")

def install_dependencies():
    """Install Python dependencies"""
    if not os.path.exists("venv"):
        print("❌ Virtual environment not found. Please create it first.")
        return False
    
    print("\n📦 Installing Python dependencies...")
    if platform.system() == "Windows":
        pip_cmd = "venv\\Scripts\\pip install -r requirements.txt"
    else:
        pip_cmd = "venv/bin/pip install -r requirements.txt"
    
    return run_command(pip_cmd, "Installing dependencies")

def setup_tailwind():
    """Setup Tailwind CSS"""
    print("\n🎨 Setting up Tailwind CSS...")
    
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    # Install Tailwind
    if not run_command(f"{python_cmd} manage.py tailwind install", "Installing Tailwind CSS"):
        return False
    
    # Build Tailwind
    if not run_command(f"{python_cmd} manage.py tailwind build", "Building Tailwind CSS"):
        return False
    
    return True

def run_migrations():
    """Run Django migrations"""
    print("\n🗄️ Setting up database...")
    
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    return run_command(f"{python_cmd} manage.py migrate", "Running migrations")

def main():
    """Main setup function"""
    print("🚀 BLINKRLOAN DASHBOARD SETUP")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Provide activation instructions
    activate_virtual_environment()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        print("   Please activate the virtual environment and run:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Setup Tailwind CSS
    if not setup_tailwind():
        print("❌ Failed to setup Tailwind CSS")
        print("   Please activate the virtual environment and run:")
        print("   python manage.py tailwind install")
        print("   python manage.py tailwind build")
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        print("❌ Failed to run migrations")
        print("   Please activate the virtual environment and run:")
        print("   python manage.py migrate")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Activate the virtual environment")
    if platform.system() == "Windows":
        print("      venv\\Scripts\\activate")
    else:
        print("      source venv/bin/activate")
    print("   2. Start the development server:")
    print("      python manage.py runserver")
    print("   3. Open http://127.0.0.1:8000 in your browser")
    print("\n🔄 For Tailwind development (watch mode):")
    print("   python manage.py tailwind start")

if __name__ == "__main__":
    main()
