import React, { useState } from 'react';
import Navbar from './components/Navbar';
import UploadPDF from './pages/UploadPDF';
import ValidateJSONPage from './pages/ValidateJSON';
import Dashboard from './pages/Dashboard';

function App() {
  const [currentPage, setCurrentPage] = useState('upload');

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50">
      <Navbar currentPage={currentPage} setCurrentPage={setCurrentPage} />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {currentPage === 'upload' && <UploadPDF />}
        {currentPage === 'validate' && <ValidateJSONPage />}
        {currentPage === 'dashboard' && <Dashboard />}
      </main>

      <footer className="bg-white border-t border-blue-100 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-gray-600 text-sm">
          <p>Invoice QC API © 2024 • Built with React + Tailwind CSS</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
