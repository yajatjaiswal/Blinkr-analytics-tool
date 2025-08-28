import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check authentication status on app load
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      // Check if user is authenticated by calling Django backend
      const response = await axios.get('/api/check-auth/', { withCredentials: true });
      if (response.data.authenticated) {
        setIsAuthenticated(true);
        setUser(response.data.user);
      }
    } catch (error) {
      console.log('Not authenticated');
    } finally {
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    try {
      const response = await axios.post('/authenticate/', {
        username,
        password
      }, { withCredentials: true });

      if (response.data.success) {
        setIsAuthenticated(true);
        setUser({ username });
        return { success: true };
      } else {
        return { success: false, message: response.data.message || 'Login failed' };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { 
        success: false, 
        message: error.response?.data?.message || 'Login failed. Please try again.' 
      };
    }
  };

  const logout = async () => {
    try {
      await axios.post('/logout/', {}, { withCredentials: true });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setIsAuthenticated(false);
      setUser(null);
    }
  };

  const value = {
    isAuthenticated,
    user,
    loading,
    login,
    logout,
    checkAuthStatus
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
