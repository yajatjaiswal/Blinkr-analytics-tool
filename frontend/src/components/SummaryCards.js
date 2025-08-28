import React from 'react';
import { DollarSign, Users, TrendingUp, Calendar } from 'lucide-react';

const SummaryCards = ({ data }) => {
  const cards = [
    {
      title: 'Total Disbursed Amount',
      value: `₹${(data.total_disbursed_amount || 0).toLocaleString()}`,
      change: data.disbursed_amount_change || 0,
      icon: DollarSign,
      color: 'blue',
      format: 'currency'
    },
    {
      title: 'Total Applications',
      value: (data.total_applications || 0).toLocaleString(),
      change: data.applications_change || 0,
      icon: Users,
      color: 'green',
      format: 'number'
    },
    {
      title: 'Processing Fee Collected',
      value: `₹${(data.total_processing_fee || 0).toLocaleString()}`,
      change: data.processing_fee_change || 0,
      icon: TrendingUp,
      color: 'purple',
      format: 'currency'
    },
    {
      title: 'Interest Amount',
      value: `₹${(data.total_interest_amount || 0).toLocaleString()}`,
      change: data.interest_amount_change || 0,
      icon: Calendar,
      color: 'orange',
      format: 'currency'
    }
  ];

  const getColorClasses = (color) => {
    const colors = {
      blue: 'bg-blue-50 text-blue-600 border-blue-200',
      green: 'bg-green-50 text-green-600 border-green-200',
      purple: 'bg-purple-50 text-purple-600 border-purple-200',
      orange: 'bg-orange-50 text-orange-600 border-orange-200'
    };
    return colors[color] || colors.blue;
  };

  const getChangeColor = (change) => {
    if (change > 0) return 'text-green-600';
    if (change < 0) return 'text-red-600';
    return 'text-gray-600';
  };

  const formatChange = (change, format) => {
    if (format === 'currency') {
      return change > 0 ? `+₹${change.toLocaleString()}` : `-₹${Math.abs(change).toLocaleString()}`;
    }
    return change > 0 ? `+${change.toLocaleString()}` : `-${Math.abs(change).toLocaleString()}`;
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card, index) => {
        const IconComponent = card.icon;
        return (
          <div key={index} className="dashboard-card hover-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="dashboard-label text-gray-600 mb-2">
                  {card.title}
                </p>
                <p className="dashboard-stat text-gray-900 mb-2">
                  {card.value}
                </p>
                {card.change !== 0 && (
                  <div className={`flex items-center text-sm ${getChangeColor(card.change)}`}>
                    <TrendingUp className={`h-4 w-4 mr-1 ${card.change < 0 ? 'rotate-180' : ''}`} />
                    <span>
                      {formatChange(card.change, card.format)}
                    </span>
                  </div>
                )}
              </div>
              <div className={`p-3 rounded-full border ${getColorClasses(card.color)}`}>
                <IconComponent className="h-6 w-6" />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default SummaryCards;
