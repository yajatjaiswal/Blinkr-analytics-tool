import React from 'react';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

const Charts = ({ data }) => {
  // Prepare data for charts
  const disbursalTrendData = data.disbursal_trend || [];
  const stateDistributionData = data.state_distribution || [];
  const cityDistributionData = data.city_distribution || [];
  const tenureDistributionData = data.tenure_distribution || [];

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4'];

  const formatCurrency = (value) => `₹${value.toLocaleString()}`;
  const formatNumber = (value) => value.toLocaleString();

  const CustomTooltip = ({ active, payload, label, formatter }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="text-gray-900 font-medium">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }}>
              {entry.name}: {formatter ? formatter(entry.value) : entry.value}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-8">
      {/* Disbursal Trend Chart */}
      <div className="chart-container">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Disbursal Trend Over Time
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={disbursalTrendData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
            <XAxis 
              dataKey="date" 
              stroke="#6b7280"
              fontSize={12}
            />
            <YAxis 
              stroke="#6b7280"
              fontSize={12}
              tickFormatter={formatCurrency}
            />
            <Tooltip 
              content={<CustomTooltip formatter={formatCurrency} />}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="disbursed_amount"
              stroke="#3b82f6"
              strokeWidth={3}
              dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, stroke: '#3b82f6', strokeWidth: 2 }}
              name="Disbursed Amount"
            />
            <Line
              type="monotone"
              dataKey="sanction_amount"
              stroke="#10b981"
              strokeWidth={3}
              dot={{ fill: '#10b981', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, stroke: '#10b981', strokeWidth: 2 }}
              name="Sanction Amount"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* State and City Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* State Distribution */}
        <div className="chart-container">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Applications by State
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={stateDistributionData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis 
                dataKey="state" 
                stroke="#6b7280"
                fontSize={12}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis 
                stroke="#6b7280"
                fontSize={12}
                tickFormatter={formatNumber}
              />
              <Tooltip 
                content={<CustomTooltip formatter={formatNumber} />}
              />
              <Bar 
                dataKey="count" 
                fill="#3b82f6"
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* City Distribution */}
        <div className="chart-container">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Applications by City
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={cityDistributionData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis 
                dataKey="city" 
                stroke="#6b7280"
                fontSize={12}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis 
                stroke="#6b7280"
                fontSize={12}
                tickFormatter={formatNumber}
              />
              <Tooltip 
                content={<CustomTooltip formatter={formatNumber} />}
              />
              <Bar 
                dataKey="count" 
                fill="#10b981"
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Tenure Distribution */}
      <div className="chart-container">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Applications by Tenure
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <AreaChart data={tenureDistributionData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
            <XAxis 
              dataKey="tenure" 
              stroke="#6b7280"
              fontSize={12}
            />
            <YAxis 
              stroke="#6b7280"
              fontSize={12}
              tickFormatter={formatNumber}
            />
            <Tooltip 
              content={<CustomTooltip formatter={formatNumber} />}
            />
            <Area
              type="monotone"
              dataKey="count"
              stroke="#8b5cf6"
              fill="#8b5cf6"
              fillOpacity={0.6}
              name="Applications"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default Charts;
