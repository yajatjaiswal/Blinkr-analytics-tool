import React from 'react';
import { Calendar, RefreshCw } from 'lucide-react';

const DateRangePicker = ({ startDate, endDate, onDateChange }) => {
  const handleStartDateChange = (e) => {
    onDateChange({ startDate: e.target.value, endDate });
  };

  const handleEndDateChange = (e) => {
    onDateChange({ startDate, endDate: e.target.value });
  };

  const setToday = () => {
    const today = new Date().toISOString().split('T')[0];
    onDateChange({ startDate: today, endDate: today });
  };

  const setLast7Days = () => {
    const end = new Date();
    const start = new Date();
    start.setDate(start.getDate() - 6);
    
    onDateChange({
      startDate: start.toISOString().split('T')[0],
      endDate: end.toISOString().split('T')[0]
    });
  };

  const setLast30Days = () => {
    const end = new Date();
    const start = new Date();
    start.setDate(start.getDate() - 29);
    
    onDateChange({
      startDate: start.toISOString().split('T')[0],
      endDate: end.toISOString().split('T')[0]
    });
  };

  const setThisMonth = () => {
    const now = new Date();
    const start = new Date(now.getFullYear(), now.getMonth(), 1);
    const end = new Date();
    
    onDateChange({
      startDate: start.toISOString().split('T')[0],
      endDate: end.toISOString().split('T')[0]
    });
  };

  const setLastMonth = () => {
    const now = new Date();
    const start = new Date(now.getFullYear(), now.getMonth() - 1, 1);
    const end = new Date(now.getFullYear(), now.getMonth(), 0);
    
    onDateChange({
      startDate: start.toISOString().split('T')[0],
      endDate: end.toISOString().split('T')[0]
    });
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
        {/* Title and Icon */}
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-blue-50 rounded-lg">
            <Calendar className="h-5 w-5 text-blue-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              Date Range Selection
            </h3>
            <p className="text-sm text-gray-500">
              Choose the date range for your analytics
            </p>
          </div>
        </div>

        {/* Date Inputs */}
        <div className="flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-4">
          <div className="flex items-center space-x-2">
            <label htmlFor="start-date" className="text-sm font-medium text-gray-700">
              From:
            </label>
            <input
              type="date"
              id="start-date"
              value={startDate}
              onChange={handleStartDateChange}
              className="form-input w-40"
            />
          </div>
          
          <div className="flex items-center space-x-2">
            <label htmlFor="end-date" className="text-sm font-medium text-gray-700">
              To:
            </label>
            <input
              type="date"
              id="end-date"
              value={endDate}
              onChange={handleEndDateChange}
              className="form-input w-40"
            />
          </div>
        </div>
      </div>

      {/* Quick Date Presets */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <h4 className="text-sm font-medium text-gray-700 mb-3">Quick Select:</h4>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={setToday}
            className={`px-3 py-1.5 text-xs font-medium rounded-lg border transition-colors ${
              startDate === endDate && startDate === new Date().toISOString().split('T')[0]
                ? 'bg-blue-100 text-blue-700 border-blue-200'
                : 'bg-gray-50 text-gray-600 border-gray-200 hover:bg-gray-100'
            }`}
          >
            Today
          </button>
          
          <button
            onClick={setLast7Days}
            className="px-3 py-1.5 text-xs font-medium rounded-lg border border-gray-200 bg-gray-50 text-gray-600 hover:bg-gray-100 transition-colors"
          >
            Last 7 Days
          </button>
          
          <button
            onClick={setLast30Days}
            className="px-3 py-1.5 text-xs font-medium rounded-lg border border-gray-200 bg-gray-50 text-gray-600 hover:bg-gray-100 transition-colors"
          >
            Last 30 Days
          </button>
          
          <button
            onClick={setThisMonth}
            className="px-3 py-1.5 text-xs font-medium rounded-lg border border-gray-200 bg-gray-50 text-gray-600 hover:bg-gray-100 transition-colors"
          >
            This Month
          </button>
          
          <button
            onClick={setLastMonth}
            className="px-3 py-1.5 text-xs font-medium rounded-lg border border-gray-200 bg-gray-50 text-gray-600 hover:bg-gray-100 transition-colors"
          >
            Last Month
          </button>
        </div>
      </div>

      {/* Date Range Info */}
      <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
        <div className="flex items-center space-x-2 text-sm text-blue-800">
          <RefreshCw className="h-4 w-4" />
          <span>
            Showing data from <strong>{startDate}</strong> to <strong>{endDate}</strong>
          </span>
        </div>
      </div>
    </div>
  );
};

export default DateRangePicker;
