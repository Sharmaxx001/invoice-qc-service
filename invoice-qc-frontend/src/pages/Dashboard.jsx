import React from 'react';
import { BarChart3 } from 'lucide-react';

const Dashboard = () => {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-md p-6 border border-blue-100">
        <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
          <BarChart3 className="w-6 h-6 mr-2 text-blue-600" />
          Analytics Dashboard
        </h2>
        <p className="text-gray-600">
          Upload invoices or validate JSON data to see analytics and statistics here.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg p-6 text-white">
          <p className="text-sm opacity-90 mb-2">Total Processed</p>
          <p className="text-4xl font-bold">0</p>
        </div>
        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl shadow-lg p-6 text-white">
          <p className="text-sm opacity-90 mb-2">Valid Invoices</p>
          <p className="text-4xl font-bold">0</p>
        </div>
        <div className="bg-gradient-to-br from-red-500 to-red-600 rounded-xl shadow-lg p-6 text-white">
          <p className="text-sm opacity-90 mb-2">Invalid Invoices</p>
          <p className="text-4xl font-bold">0</p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-md p-6 border border-blue-100">
        <h3 className="text-lg font-bold text-gray-800 mb-4">Quick Stats</h3>
        <div className="h-64 flex items-center justify-center text-gray-400">
          <p>No data available yet. Start processing invoices to see charts.</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;