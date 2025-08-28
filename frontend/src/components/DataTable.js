import React, { useState } from 'react';
import { format } from 'date-fns';
import { Eye, Download, Filter } from 'lucide-react';

const DataTable = ({ data }) => {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [searchTerm, setSearchTerm] = useState('');

  // Sorting function
  const sortData = (data, key, direction) => {
    return [...data].sort((a, b) => {
      let aValue = a[key];
      let bValue = b[key];

      // Handle numeric values
      if (typeof aValue === 'number' && typeof bValue === 'number') {
        return direction === 'asc' ? aValue - bValue : bValue - aValue;
      }

      // Handle string values
      if (typeof aValue === 'string' && typeof bValue === 'string') {
        aValue = aValue.toLowerCase();
        bValue = bValue.toLowerCase();
        if (aValue < bValue) return direction === 'asc' ? -1 : 1;
        if (aValue > bValue) return direction === 'asc' ? 1 : -1;
        return 0;
      }

      // Handle date values
      if (aValue && bValue) {
        const aDate = new Date(aValue);
        const bDate = new Date(bValue);
        if (!isNaN(aDate) && !isNaN(bDate)) {
          return direction === 'asc' ? aDate - bDate : bDate - aDate;
        }
      }

      return 0;
    });
  };

  // Handle sort
  const handleSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  // Filter and sort data
  const filteredAndSortedData = sortData(
    data.filter(item => 
      item.full_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.pan?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.state?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.city?.toLowerCase().includes(searchTerm.toLowerCase())
    ),
    sortConfig.key,
    sortConfig.direction
  );

  // Format currency
  const formatCurrency = (value) => {
    if (!value) return '₹0';
    return `₹${parseFloat(value).toLocaleString()}`;
  };

  // Format date
  const formatDate = (dateString) => {
    if (!dateString) return '-';
    try {
      return format(new Date(dateString), 'MMM dd, yyyy');
    } catch {
      return dateString;
    }
  };

  // Get status badge
  const getStatusBadge = (isLeadClosed) => {
    if (isLeadClosed) {
      return <span className="status-badge status-closed">Closed</span>;
    }
    return <span className="status-badge status-active">Active</span>;
  };

  const columns = [
    { key: 'full_name', label: 'Applicant Name', sortable: true },
    { key: 'pan', label: 'PAN', sortable: true },
    { key: 'sanction_amount', label: 'Sanction Amount', sortable: true, format: formatCurrency },
    { key: 'disbursed_amount', label: 'Disbursed Amount', sortable: true, format: formatCurrency },
    { key: 'processing_fee', label: 'Processing Fee', sortable: true, format: formatCurrency },
    { key: 'interest_amount', label: 'Interest', sortable: true, format: formatCurrency },
    { key: 'state', label: 'State', sortable: true },
    { key: 'city', label: 'City', sortable: true },
    { key: 'tenure', label: 'Tenure', sortable: true },
    { key: 'disbursal_date', label: 'Disbursal Date', sortable: true, format: formatDate },
    { key: 'status', label: 'Status', sortable: false }
  ];

  return (
    <div className="p-6">
      {/* Search and Filter Bar */}
      <div className="mb-6 flex flex-col sm:flex-row gap-4 items-center justify-between">
        <div className="relative flex-1 max-w-md">
          <input
            type="text"
            placeholder="Search by name, PAN, state, or city..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="form-input pl-10 w-full"
          />
          <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
        </div>
        <div className="text-sm text-gray-500">
          Showing {filteredAndSortedData.length} of {data.length} applications
        </div>
      </div>

      {/* Table */}
      <div className="table-scroll">
        <table className="data-table">
          <thead>
            <tr>
              {columns.map((column) => (
                <th
                  key={column.key}
                  className={`${column.sortable ? 'cursor-pointer hover:bg-gray-100' : ''}`}
                  onClick={() => column.sortable && handleSort(column.key)}
                >
                  <div className="flex items-center space-x-1">
                    <span>{column.label}</span>
                    {column.sortable && (
                      <span className="text-gray-400">
                        {sortConfig.key === column.key ? (
                          sortConfig.direction === 'asc' ? '↑' : '↓'
                        ) : '↕'}
                      </span>
                    )}
                  </div>
                </th>
              ))}
              <th className="w-20">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredAndSortedData.map((item, index) => (
              <tr key={index} className="hover:bg-gray-50">
                {columns.map((column) => (
                  <td key={column.key}>
                    {column.key === 'status' ? (
                      getStatusBadge(item.is_lead_closed)
                    ) : column.format ? (
                      column.format(item[column.key])
                    ) : (
                      item[column.key] || '-'
                    )}
                  </td>
                ))}
                <td>
                  <div className="flex items-center space-x-2">
                    <button
                      className="p-1 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded"
                      title="View Details"
                    >
                      <Eye className="h-4 w-4" />
                    </button>
                    <button
                      className="p-1 text-green-600 hover:text-green-800 hover:bg-green-50 rounded"
                      title="Download"
                    >
                      <Download className="h-4 w-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Empty State */}
      {filteredAndSortedData.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <Filter className="h-12 w-12 mx-auto" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            No applications found
          </h3>
          <p className="text-gray-500">
            Try adjusting your search criteria or date range.
          </p>
        </div>
      )}
    </div>
  );
};

export default DataTable;
