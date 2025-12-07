import React, { useState } from 'react';
import { Code, CheckCircle } from 'lucide-react';
import { validateJSON } from '../api/client';
import ValidationResultCard from '../components/ValidationResultCard';
import SummaryCard from '../components/SummaryCard';

const ValidateJSONPage = () => {
  const [jsonInput, setJsonInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const exampleJSON = [
    {
      invoice_id: "INV-2024-001",
      invoice_date: "2024-12-06",
      buyer_name: "Acme Corp",
      seller_name: "Tech Supplies Inc",
      total_amount: 1000.00,
      tax_amount: 100.00,
      total_with_tax: 1100.00,
      currency: "USD"
    }
  ];

  const handleValidate = async () => {
    if (!jsonInput.trim()) {
      setError('Please enter JSON data');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const invoices = JSON.parse(jsonInput);
      if (!Array.isArray(invoices)) {
        throw new Error('Input must be a JSON array');
      }
      const data = await validateJSON(invoices);
      setResult(data);
    } catch (err) {
      if (err instanceof SyntaxError) {
        setError('Invalid JSON format');
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const loadExample = () => {
    setJsonInput(JSON.stringify(exampleJSON, null, 2));
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-md p-6 border border-blue-100">
        <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
          <Code className="w-6 h-6 mr-2 text-blue-600" />
          Validate JSON Invoices
        </h2>

        <div className="space-y-4">
          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="text-sm font-medium text-gray-700">
                Paste JSON Array of Invoices
              </label>
              <button
                onClick={loadExample}
                className="text-sm text-blue-600 hover:text-blue-700 font-medium"
              >
                Load Example
              </button>
            </div>
            <textarea
              value={jsonInput}
              onChange={(e) => setJsonInput(e.target.value)}
              placeholder='[{"invoice_id": "INV-001", ...}]'
              className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
            />
          </div>

          <button
            onClick={handleValidate}
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Validating...
              </>
            ) : (
              <>
                <CheckCircle className="w-5 h-5 mr-2" />
                Validate Invoices
              </>
            )}
          </button>
        </div>

        {error && (
          <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}
      </div>

      {result && (
        <div className="space-y-6">
          <SummaryCard summary={result.summary} />

          <div>
            <h3 className="text-xl font-bold text-gray-800 mb-4">Validation Results</h3>
            <div className="space-y-4">
              {result.results.map((res, idx) => (
                <ValidationResultCard key={idx} result={res} index={idx} />
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ValidateJSONPage;