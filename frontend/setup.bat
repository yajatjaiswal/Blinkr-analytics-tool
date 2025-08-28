@echo off
echo 🚀 Setting up Blinkr Analytics React Frontend...
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed!
    echo Please install Node.js from: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo ✅ Node.js found: 
node --version
echo.

REM Check if npm is available
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm is not available!
    echo Please ensure npm is properly installed with Node.js
    echo.
    pause
    exit /b 1
)

echo ✅ npm found:
npm --version
echo.

REM Install dependencies
echo 📦 Installing dependencies...
npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies!
    echo.
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully!
echo.

REM Check if Django backend is running
echo 🔍 Checking Django backend connection...
curl -s http://localhost:8000/api/summary/ >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Warning: Django backend might not be running on localhost:8000
    echo    Please ensure your Django server is started before using the frontend
    echo.
)

echo.
echo 🎉 Setup complete! Starting React development server...
echo.
echo 🌐 Frontend will be available at: http://localhost:3000
echo 🔗 Backend should be running at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the development server
npm start

pause
