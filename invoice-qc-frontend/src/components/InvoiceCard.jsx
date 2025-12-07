import React from 'react';

const InvoiceCard = ({ invoice }) => {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 border border-blue-100">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <p className="text-sm text-gray-500">Invoice ID</p>
          <p className="font-semibold text-gray-800">{invoice.invoice_id || 'N/A'}</p>
        </div>
        <div>
          <p className="text-sm text-gray-500">Date</p>
          <p className="font-semibold text-gray-800">{invoice.invoice_date || 'N/A'}</p>
        </div>
        <div>
          <p className="text-sm text-gray-500">Buyer</p>
          <p className="font-semibold text-gray-800">{invoice.buyer_name || 'N/A'}</p>
        </div>
        <div>
          <p className="text-sm text-gray-500">Seller</p>
          <p className="font-semibold text-gray-800">{invoice.seller_name || 'N/A'}</p>
        </div>
        <div>
          <p className="text-sm text-gray-500">Total Amount</p>
          <p className="font-semibold text-gray-800">
            {invoice.currency || 'USD'} {invoice.total_amount?.toFixed(2) || 'N/A'}
          </p>
        </div>
        <div>
          <p className="text-sm text-gray-500">Total with Tax</p>
          <p className="font-semibold text-gray-800">
            {invoice.currency || 'USD'} {invoice.total_with_tax?.toFixed(2) || 'N/A'}
          </p>
        </div>
      </div>

      {invoice.line_items && invoice.line_items.length > 0 && (
        <div className="mt-6">
          <h4 className="font-semibold text-gray-800 mb-3">Line Items</h4>
          <div className="space-y-2">
            {invoice.line_items.map((item, idx) => (
              <div key={idx} className="bg-blue-50 rounded-lg p-3 text-sm">
                <p className="font-medium text-gray-800">{item.description}</p>
                <p className="text-gray-600">
                  Qty: {item.quantity} × {invoice.currency || 'USD'} {item.unit_price?.toFixed(2)} = {invoice.currency || 'USD'} {item.line_total?.toFixed(2)}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default InvoiceCard;