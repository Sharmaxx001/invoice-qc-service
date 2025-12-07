import React, { useState } from 'react';
import { FileText, Upload, CheckCircle, XCircle } from 'lucide-react';
import { uploadPDF } from '../api/client';
import InvoiceCard from '../components/InvoiceCard';
import ErrorList from '../components/ErrorList';
import SummaryCard from '../components/SummaryCard';

const UploadPDF = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError(null);
    } else {
      setError('Please select a valid PDF file');
      setFile(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a PDF file first');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await uploadPDF(file);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-md p-6 border border-blue-100">
        <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
          <Upload className="w-6 h-6 mr-2 text-blue-600" />
          Upload Invoice PDF
        </h2>
        
        <div className="space-y-4">
          <div className="border-2 border-dashed border-blue-300 rounded-xl p-8 text-center hover:border-blue-500 transition-colors">
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              className="hidden"
              id="pdf-upload"
            />
            <label htmlFor="pdf-upload" className="cursor-pointer">
              <FileText className="w-16 h-16 mx-auto text-blue-400 mb-4" />
              <p className="text-gray-600 mb-2">
                {file ? file.name : 'Click to select a PDF file'}
              </p>
              <p className="text-sm text-gray-400">or drag and drop</p>
            </label>
          </div>

          <button
            onClick={handleUpload}
            disabled={!file || loading}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Processing...
              </>
            ) : (
              <>
                <Upload className="w-5 h-5 mr-2" />
                Extract & Validate
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
          <div className={`rounded-xl shadow-md p-6 border-2 ${
            result.result.valid
              ? 'bg-green-50 border-green-200'
              : 'bg-red-50 border-red-200'
          }`}>
            <div className="flex items-center space-x-3">
              {result.result.valid ? (
                <CheckCircle className="w-8 h-8 text-green-600" />
              ) : (
                <XCircle className="w-8 h-8 text-red-600" />
              )}
              <div>
                <h3 className="text-xl font-bold text-gray-800">
                  {result.result.valid ? 'Invoice Valid' : 'Invoice Invalid'}
                </h3>
                <p className="text-sm text-gray-600">
                  Invoice ID: {result.result.invoice_id || 'N/A'}
                </p>
              </div>
            </div>
          </div>

          {result.result.errors && result.result.errors.length > 0 && (
            <ErrorList errors={result.result.errors} />
          )}

          <div>
            <h3 className="text-xl font-bold text-gray-800 mb-4">Extracted Data</h3>
            <InvoiceCard invoice={result.extracted} />
          </div>

          <SummaryCard summary={result.summary} />
        </div>
      )}
    </div>
  );
};

export default UploadPDF;