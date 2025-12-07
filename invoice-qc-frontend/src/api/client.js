// API client for Invoice QC Service
export const API_BASE_URL = "http://127.0.0.1:8000";



/**
 * Upload PDF file and extract + validate invoice
 * @param {File} file - PDF file to upload
 * @returns {Promise} API response
 */
export const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`${API_BASE_URL}/extract-and-validate-pdf`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Upload failed');
  }
  
  return response.json();
};

/**
 * Validate array of invoice JSON objects
 * @param {Array} invoices - Array of invoice objects
 * @returns {Promise} API response
 */
export const validateJSON = async (invoices) => {
  const response = await fetch(`${API_BASE_URL}/validate-json`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(invoices),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Validation failed');
  }
  
  return response.json();
};