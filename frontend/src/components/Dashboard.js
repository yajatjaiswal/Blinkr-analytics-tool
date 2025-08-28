import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { LogOut, Calendar, TrendingUp, DollarSign, Users, Filter } from 'lucide-react';
import SummaryCards from './SummaryCards';
import Charts from './Charts';
import DataTable from './DataTable';
import DateRangePicker from './DateRangePicker';
import axios from 'axios';

const Dashboard = () => {
  const { logout, user } = useAuth();
  const [summaryData, setSummaryData] = useState(null);
  const [chartsData, setChartsData] = useState(null);
  const [tableData, setTableData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState({
    startDate: new Date().toISOString().split('T')[0],
    endDate: new Date().toISOString().split('T')[0]
  });

  useEffect(() => {
    fetchDashboardData();
  }, [dateRange]);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      // Fetch all data in parallel
      const [summaryRes, chartsRes, tableRes] = await Promise.all([
        axios.get(`/api/summary/?start_date=${dateRange.startDate}&end_date=${dateRange.endDate}`),
        axios.get(`/api/charts/?start_date=${dateRange.startDate}&end_date=${dateRange.endDate}`),
        axios.get(`/api/table/?start_date=${dateRange.startDate}&end_date=${dateRange.endDate}&page=1&per_page=10`)
      ]);

      setSummaryData(summaryRes.data);
      setChartsData(chartsRes.data);
      setTableData(tableRes.data.applications || []);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    await logout();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="loading-spinner mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-8 w-8 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                  <TrendingUp className="h-5 w-5 text-white" />
                </div>
              </div>
              <div className="ml-3">
                <h1 className="text-xl font-semibold text-gray-900">
                  Blinkr Analytics Dashboard
                </h1>
                <p className="text-sm text-gray-500">
                  Loan Disbursal Analytics
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm font-medium text-gray-900">
                  Welcome, {user?.username || 'User'}
                </p>
                <p className="text-xs text-gray-500">
                  {new Date().toLocaleDateString()}
                </p>
              </div>
              <button
                onClick={handleLogout}
                className="btn-secondary flex items-center space-x-2"
              >
                <LogOut className="h-4 w-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Date Range Picker */}
        <div className="mb-8">
          <DateRangePicker
            startDate={dateRange.startDate}
            endDate={dateRange.endDate}
            onDateChange={setDateRange}
          />
        </div>

        {/* Summary Cards */}
        {summaryData && (
          <div className="mb-8">
            <SummaryCards data={summaryData} />
          </div>
        )}

        {/* Charts Section */}
        {chartsData && (
          <div className="mb-8">
            <Charts data={chartsData} />
          </div>
        )}

        {/* Data Table */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100">
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">
                Loan Applications
              </h3>
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <Filter className="h-4 w-4" />
                <span>Showing {tableData.length} applications</span>
              </div>
            </div>
          </div>
          <DataTable data={tableData} />
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
