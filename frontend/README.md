# 🚀 Blinkr Analytics Dashboard - React Frontend

A modern, responsive React frontend for the Blinkr Analytics Dashboard that connects to your Django backend API.

## ✨ Features

- **Modern React 18** with hooks and functional components
- **Beautiful UI/UX** with Tailwind CSS
- **Responsive Design** that works on all devices
- **Interactive Charts** using Recharts library
- **Real-time Data** from Django backend APIs
- **Authentication System** with protected routes
- **Search & Filtering** for data tables
- **Date Range Selection** with quick presets
- **Sortable Tables** with multiple columns
- **Loading States** and error handling

## 🏗️ Architecture

```
frontend/
├── public/                 # Static files
├── src/
│   ├── components/         # React components
│   │   ├── Dashboard.js    # Main dashboard
│   │   ├── Login.js        # Authentication
│   │   ├── SummaryCards.js # KPI cards
│   │   ├── Charts.js       # Data visualizations
│   │   ├── DataTable.js    # Data table
│   │   └── DateRangePicker.js # Date selection
│   ├── contexts/           # React contexts
│   │   └── AuthContext.js  # Authentication state
│   ├── App.js              # Main app component
│   ├── index.js            # Entry point
│   └── index.css           # Global styles
├── package.json            # Dependencies
└── tailwind.config.js      # Tailwind configuration
```

## 🚀 Quick Start

### Prerequisites

- **Node.js 16+** and npm
- **Django backend** running on localhost:8000

### Installation

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```

4. **Open in browser:**
   ```
   http://localhost:3000
   ```

## 🔧 Configuration

### Backend API Connection

The frontend is configured to connect to your Django backend at `http://localhost:8000`. This is set in:

- `package.json` - proxy configuration
- `src/contexts/AuthContext.js` - API endpoints

### Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_APP_NAME=Blinkr Analytics
```

## 📱 Components Overview

### 1. **Dashboard** (`Dashboard.js`)
- Main dashboard layout
- Header with user info and logout
- Orchestrates all dashboard components

### 2. **Summary Cards** (`SummaryCards.js`)
- Key Performance Indicators (KPIs)
- Beautiful metric cards with icons
- Change indicators and trends

### 3. **Charts** (`Charts.js`)
- Line charts for trends
- Bar charts for distributions
- Area charts for tenure analysis
- Responsive chart containers

### 4. **Data Table** (`DataTable.js`)
- Sortable columns
- Search and filtering
- Pagination support
- Action buttons for each row

### 5. **Date Range Picker** (`DateRangePicker.js`)
- Custom date inputs
- Quick preset buttons
- Date range validation
- Visual feedback

### 6. **Login** (`Login.js`)
- Beautiful authentication form
- Error handling
- Loading states
- Demo credentials display

## 🎨 Styling

### Tailwind CSS
- **Custom color palette** for brand consistency
- **Responsive utilities** for mobile-first design
- **Custom animations** and transitions
- **Component-based classes** for reusability

### Custom CSS
- **Loading spinners** and animations
- **Form styling** with focus states
- **Table enhancements** with hover effects
- **Status badges** for different states

## 🔌 API Integration

### Authentication Endpoints
- `POST /authenticate/` - User login
- `POST /logout/` - User logout
- `GET /api/check-auth/` - Check auth status

### Data Endpoints
- `GET /api/summary/` - Dashboard summary data
- `GET /api/charts/` - Chart data
- `GET /api/table/` - Table data with pagination
- `GET /api/distinct-values/` - Filter options

## 🚀 Build & Deploy

### Development Build
```bash
npm run build
```

### Production Deployment
```bash
npm run build
# Copy build/ folder to your web server
```

### Docker (Optional)
```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🧪 Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm test -- --watch
```

## 📱 Responsive Design

- **Mobile-first** approach
- **Breakpoints**: sm (640px), md (768px), lg (1024px), xl (1280px)
- **Flexible grids** that adapt to screen size
- **Touch-friendly** interactions for mobile devices

## 🔒 Security Features

- **Protected routes** with authentication
- **CSRF protection** via Django backend
- **Input validation** and sanitization
- **Secure API calls** with credentials

## 🚀 Performance Optimizations

- **Code splitting** with React.lazy()
- **Memoization** for expensive calculations
- **Debounced search** for better UX
- **Optimized re-renders** with proper state management

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure Django backend has CORS configured
   - Check proxy settings in package.json

2. **API Connection Issues**
   - Verify Django server is running on port 8000
   - Check network tab for failed requests

3. **Build Errors**
   - Clear node_modules and reinstall
   - Check Node.js version compatibility

4. **Styling Issues**
   - Ensure Tailwind CSS is properly configured
   - Check for CSS conflicts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the Django backend documentation
- Review the API endpoints
- Check browser console for errors
- Verify network connectivity

---

**Happy Coding! 🎉**
