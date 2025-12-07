import React from 'react';
import { XCircle } from 'lucide-react';

const ErrorList = ({ errors }) => {
  if (!errors || errors.length === 0) return null;

  return (
    <div className="bg-red-50 border border-red-200 rounded-xl p-4">
      <h4 className="font-semibold text-red-800 mb-2 flex items-center">
        <XCircle className="w-5 h-5 mr-2" />
        Validation Errors
      </h4>
      <ul className="space-y-1">
        {errors.map((error, idx) => (
          <li key={idx} className="text-red-700 text-sm flex items-start">
            <span className="mr-2">•</span>
            <span>{error}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ErrorList;