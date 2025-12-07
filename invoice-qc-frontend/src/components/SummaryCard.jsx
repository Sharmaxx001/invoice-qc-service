import React from 'react';

const SummaryCard = ({ summary }) => {
  return (
    <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl shadow-lg p-6 text-white">
      <h3 className="text-xl font-bold mb-4">Validation Summary</h3>
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white/10 rounded-lg p-4 backdrop-blur-sm">
          <p className="text-sm opacity-90">Total</p>
          <p className="text-3xl font-bold">{summary.total_invoices}</p>
        </div>
        <div className="bg-green-500/20 rounded-lg p-4 backdrop-blur-sm">
          <p className="text-sm opacity-90">Valid</p>
          <p className="text-3xl font-bold">{summary.valid_invoices}</p>
        </div>
        <div className="bg-red-500/20 rounded-lg p-4 backdrop-blur-sm">
          <p className="text-sm opacity-90">Invalid</p>
          <p className="text-3xl font-bold">{summary.invalid_invoices}</p>
        </div>
      </div>

      {summary.missing_count_by_field && Object.keys(summary.missing_count_by_field).length > 0 && (
        <div className="mt-6 bg-white/10 rounded-lg p-4 backdrop-blur-sm">
          <h4 className="font-semibold mb-2">Missing Fields</h4>
          <div className="space-y-1 text-sm">
            {Object.entries(summary.missing_count_by_field).map(([field, count]) => (
              <div key={field} className="flex justify-between">
                <span className="opacity-90">{field}</span>
                <span className="font-semibold">{count}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SummaryCard;