# 🚀 Invoice QC Frontend

A clean, responsive React + Tailwind interface for the **Invoice QC Service**.  
Enables PDF upload, real-time validation, and clear visualization of invoice extraction results.

---

## 🌟 Features

- 📄 Upload PDF invoices and validate instantly
- 🔍 Displays extracted fields, errors, and summary
- 🎨 Styled with Tailwind CSS
- ⚡ Built using Vite for fast development
- 🔗 Fully integrated with FastAPI backend

---

## 🛠 Tech Stack

- React 18 (Vite)
- Tailwind CSS
- Axios
- Lucide Icons

---

## 📦 Installation

# Navigate into the frontend folder

cd invoice-qc-frontend

# Install dependencies

npm install

🎨 Tailwind Setup

index.css
@tailwind base;
@tailwind components;
@tailwind utilities;

tailwind.config.js
export default {
content: ["./index.html", "./src/**/*.{js,jsx}"],
theme: { extend: {} },
plugins: [],
};

🔗 Configure Backend API URL

Update your Axios client:

    export const API_BASE_URL = "http://localhost:8000";

▶️ Run the App
npm run dev

Open:
http://localhost:5173

📁 Project Structure

invoice-qc-frontend/
├── public/
├── src/
│ ├── api/
│ ├── components/
│ ├── pages/
│ ├── assets/
│ ├── App.jsx
│ ├── main.jsx
│ ├── index.css
├── package.json
├── tailwind.config.js
├── vite.config.js

🤝 Backend Integration

The frontend connects to the FastAPI backend endpoints:

    POST /extract-and-validate-pdf
    POST /validate-json

Backend folder: invoice-qc-service/src/api.py

```

```
