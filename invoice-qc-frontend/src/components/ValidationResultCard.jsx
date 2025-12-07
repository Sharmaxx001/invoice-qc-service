import React from 'react';
import { CheckCircle, XCircle } from 'lucide-react';
import ErrorList from './ErrorList';

const ValidationResultCard = ({ result, index }) => {
  return (
    <div
      className={`rounded-xl shadow-md p-6 border-2 ${
        result.valid
          ? 'bg-white border-green-200'
          : 'bg-red-50 border-red-200'
      }`}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          {result.valid ? (
            <CheckCircle className="w-6 h-6 text-green-600" />
          ) : (
            <XCircle className="w-6 h-6 text-red-600" />
          )}
          <div>
            <h4 className="font-semibold text-gray-800">
              Invoice #{index + 1}
            </h4>
            <p className="text-sm text-gray-600">
              ID: {result.invoice_id || 'N/A'}
            </p>
          </div>
        </div>
        <span
          className={`px-3 py-1 rounded-full text-sm font-semibold ${
            result.valid
              ? 'bg-green-100 text-green-800'
              : 'bg-red-100 text-red-800'
          }`}
        >
          {result.valid ? 'Valid' : 'Invalid'}
        </span>
      </div>

      {result.errors && result.errors.length > 0 && (
        <ErrorList errors={result.errors} />
      )}
    </div>
  );
};

export default ValidationResultCard;