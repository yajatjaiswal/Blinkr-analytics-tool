# Blinkr Loan Dashboard

A professional financial dashboard for loan disbursal analytics and insights.

## Features

- **Secure Login System** - Authentication required to access dashboard
- **Interactive Dashboard** - Real-time financial data visualization
- **Responsive Design** - Works on all devices and screen sizes
- **Modern UI/UX** - Professional design with smooth animations
- **Data Analytics** - Charts, tables, and summary statistics

## Login Credentials

**Username:** Admin  
**Password:** Admin@123

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

3. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

4. **Access Application**
   - Open browser and go to: `http://localhost:8000/`
   - You'll be redirected to the login page
   - Use the credentials above to access the dashboard

## Project Structure

```
blinkr_dashboard/
├── dashboard/                 # Main dashboard app
│   ├── views.py             # Dashboard views and API endpoints
│   ├── urls.py              # URL routing
│   └── ...
├── templates/
│   ├── login.html           # Login page
│   └── dashboard/           # Dashboard templates
│       └── dashboard.html   # Main dashboard
├── static/
│   ├── css/                 # Stylesheets
│   └── Assets/              # Images and assets
└── ...
```

## Authentication Flow

1. **Login Page** (`/` or `/login/`)
   - User enters credentials
   - System validates Admin/Admin@123
   - Redirects to dashboard on success

2. **Dashboard** (`/dashboard/`)
   - Protected route requiring authentication
   - Session-based authentication
   - Logout button available in header

3. **Logout** (`/logout/`)
   - Clears session
   - Redirects back to login page

## Security Notes

- This is a demo implementation with hardcoded credentials
- For production use, implement proper Django authentication
- Use environment variables for sensitive data
- Add CSRF protection and rate limiting

## Customization

- Update credentials in `dashboard/views.py`
- Modify login page design in `templates/login.html`
- Customize dashboard styling in `static/css/enhanced.css`
- Add more authentication methods as needed

## Support

For any issues or questions, please refer to the Django documentation or contact the development team.
