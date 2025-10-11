# 💰 AI-Powered Personal Finance Tracker

A comprehensive full-stack web application for managing personal finances with intelligent insights, real-time analytics, and budget tracking capabilities.

[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)

## 📋 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Demo](#-demo)
- [Installation](#-installation)
- [API Documentation](#-api-documentation)
- [Screenshots](#-screenshots)
- [Project Structure](#-project-structure)
- [Key Learnings](#-key-learnings)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [Contact](#-contact)

## ✨ Features

### Core Functionality
- **🔐 User Authentication** - Secure JWT-based registration, login, and session management
- **💸 Transaction Management** - Track income and expenses with detailed categorization
- **🎯 Budget Tracking** - Set spending limits per category with real-time progress monitoring
- **📊 Financial Dashboard** - Interactive dashboard with spending summaries and visualizations
- **📈 AI-Powered Insights** - Intelligent analysis of spending patterns and behavior
- **🔮 Predictive Analytics** - Future expense predictions based on historical data
- **📱 Responsive Design** - Fully responsive UI that works seamlessly on all devices

### Technical Features
- RESTful API architecture
- JWT token-based authentication with refresh tokens
- PostgreSQL database with optimized queries
- Real-time data aggregation and calculations
- Category-based expense organization (15 default categories)
- Month-over-month financial comparison
- Spending trend analysis
- Budget alert system
- Transaction filtering and search

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Django 5.0** | Python web framework |
| **Django REST Framework** | RESTful API development |
| **PostgreSQL** | Relational database |
| **Simple JWT** | JWT authentication |
| **Pandas** | Data analysis and manipulation |
| **NumPy** | Numerical computations |
| **Scikit-learn** | Machine learning for predictions |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | User interface library |
| **React Router** | Client-side routing |
| **Axios** | HTTP client for API calls |
| **Tailwind CSS** | Utility-first CSS framework |
| **Context API** | Global state management |
| **React Hooks** | Modern React state management |

## 🎥 Demo

### Live Features
- Register/Login with JWT authentication
- Add income and expense transactions
- View real-time financial summary
- Track spending by category
- Set and monitor budgets
- Get AI-powered financial insights

**Dashboard Preview:**
Income: $5,000  |  Expenses: $3,200  |  Savings: $1,800 (36%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Category Breakdown:
🍔 Food & Dining     $850  ████████████░░░░░░░░  26.5%
🚗 Transportation    $450  ███████░░░░░░░░░░░░░  14.0%
🏠 Bills & Utilities $600  █████████░░░░░░░░░░░  18.7%

## 🚀 Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.10 or higher
- Node.js 18 or higher
- PostgreSQL 14 or higher
- Git

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/AshOP31244/ai-finance-tracker.git
cd ai-finance-tracker/backend

Create and activate virtual environment

bash# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install Python dependencies

bashpip install -r requirements.txt

Create PostgreSQL database

sql-- Open PostgreSQL shell
CREATE DATABASE finance_db;

Configure environment variables

Create a .env file in the backend folder:
envSECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True

DB_NAME=finance_db
DB_USER=postgres
DB_PASSWORD=your_postgresql_password
DB_HOST=localhost
DB_PORT=5432

Run database migrations

bashpython manage.py makemigrations
python manage.py migrate

Create default categories

bashpython manage.py create_default_categories

Create superuser (admin)

bashpython manage.py createsuperuser

Start development server

bashpython manage.py runserver
Backend will run at http://127.0.0.1:8000/
Frontend Setup

Navigate to frontend directory

bashcd ../frontend

Install Node dependencies

bashnpm install

Configure environment variables

Create a .env file in the frontend folder:
envREACT_APP_API_URL=http://127.0.0.1:8000/api

Start React development server

bashnpm start
Frontend will open at http://localhost:3000/
📡 API Documentation
Authentication Endpoints
MethodEndpointDescriptionPOST/api/auth/register/Register new userPOST/api/auth/login/Login and get JWT tokensPOST/api/auth/token/refresh/Refresh access tokenGET/api/auth/profile/Get current user profilePATCH/api/auth/profile/Update user profilePOST/api/auth/logout/Logout and blacklist token
Transaction Endpoints
MethodEndpointDescriptionGET/api/transactions/transactions/List all user transactionsPOST/api/transactions/transactions/Create new transactionGET/api/transactions/transactions/{id}/Get specific transactionPATCH/api/transactions/transactions/{id}/Update transactionDELETE/api/transactions/transactions/{id}/Delete transactionGET/api/transactions/transactions/summary/Financial summary (income, expenses, savings)GET/api/transactions/transactions/trends/Monthly spending trendsGET/api/transactions/transactions/recent/Recent transactions
Category Endpoints
MethodEndpointDescriptionGET/api/transactions/categories/List all categoriesPOST/api/transactions/categories/Create custom categoryGET/api/transactions/categories/expense_categories/Get expense categories onlyGET/api/transactions/categories/income_categories/Get income categories only
Budget Endpoints
MethodEndpointDescriptionGET/api/budgets/List all budgetsPOST/api/budgets/Create new budgetGET/api/budgets/{id}/Get specific budgetPATCH/api/budgets/{id}/Update budgetDELETE/api/budgets/{id}/Delete budgetGET/api/budgets/overview/Budget overview with alerts
Analytics Endpoints
MethodEndpointDescriptionGET/api/analytics/insights/AI-powered spending insightsGET/api/analytics/prediction/Future spending predictionsGET/api/analytics/comparison/Month-over-month comparison
Example API Request
Create Transaction:
bashcurl -X POST http://127.0.0.1:8000/api/transactions/transactions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "expense",
    "amount": "50.00",
    "category": 1,
    "date": "2025-01-15",
    "description": "Grocery shopping"
  }'
📸 Screenshots
Dashboard - Financial Overview
Show Image

Real-time financial summary cards
Category-wise spending breakdown
Recent transactions list
Visual progress bars

Transaction Management
Show Image

Easy-to-use transaction form
Category selection with emojis
Income/Expense toggle
Date picker and descriptions

Budget Tracking
Show Image

Budget progress visualization
Alert system for overspending
Category-wise budget allocation

📁 Project Structure
ai-finance-tracker/
├── backend/
│   ├── finance_tracker/          # Main Django project
│   │   ├── settings.py           # Django settings
│   │   ├── urls.py               # Main URL configuration
│   │   └── wsgi.py
│   ├── users/                    # User authentication app
│   │   ├── models.py             # CustomUser model
│   │   ├── serializers.py        # User serializers
│   │   ├── views.py              # Auth views
│   │   └── urls.py
│   ├── transactions/             # Transaction management app
│   │   ├── models.py             # Transaction, Category models
│   │   ├── serializers.py        # Transaction serializers
│   │   ├── views.py              # Transaction viewsets
│   │   ├── admin.py              # Admin configuration
│   │   └── management/
│   │       └── commands/
│   │           └── create_default_categories.py
│   ├── budgets/                  # Budget tracking app
│   │   ├── models.py             # Budget model
│   │   ├── serializers.py        # Budget serializers
│   │   └── views.py              # Budget viewsets
│   ├── analytics/                # AI analytics app
│   │   ├── views.py              # Insights & predictions
│   │   └── urls.py
│   ├── manage.py
│   └── requirements.txt          # Python dependencies
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/           # React components
│   │   │   └── TransactionForm.js
│   │   ├── pages/                # Page components
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   └── Dashboard.js
│   │   ├── services/             # API services
│   │   │   ├── api.js            # Axios configuration
│   │   │   ├── authService.js
│   │   │   └── transactionService.js
│   │   ├── context/              # React context
│   │   │   └── AuthContext.js
│   │   ├── utils/                # Utility functions
│   │   │   └── formatters.js
│   │   ├── App.js                # Main app component
│   │   └── index.js
│   ├── package.json              # Node dependencies
│   └── tailwind.config.js        # Tailwind configuration
│
├── .gitignore
└── README.md
🎓 Key Learnings
Backend Development

Designed and implemented RESTful APIs following best practices
Created custom Django models with relationships (ForeignKey, OneToMany)
Implemented JWT authentication with token refresh mechanism
Optimized database queries using Django ORM aggregations
Built custom management commands for data initialization
Handled CORS for cross-origin requests
Implemented serializers for data validation and transformation

Frontend Development

Built reusable React components with hooks (useState, useEffect, useContext)
Implemented protected routes and authentication flow
Created custom API service layer with Axios interceptors
Managed global state with Context API
Designed responsive layouts with Tailwind CSS
Handled form validation and error states
Implemented auto-token refresh on 401 errors

Full-Stack Integration

Connected React frontend with Django backend via REST APIs
Implemented JWT token storage and management in localStorage
Handled asynchronous API calls with async/await
Managed authentication state across components
Synchronized frontend and backend data models

Database Design

Normalized database schema with proper relationships
Created indexes for frequently queried fields
Implemented soft deletes and audit timestamps
Designed efficient many-to-one relationships

DevOps & Tools

Version control with Git and GitHub
Environment variable management with .env files
Virtual environment isolation
Package management (pip, npm)

🔮 Future Enhancements

 Data Export - Export transactions to CSV/PDF/Excel formats
 Receipt Scanning - OCR integration for automatic expense entry from receipts
 Multi-Currency Support - Track expenses in different currencies with conversion
 Recurring Transactions - Automatic creation of recurring bills and income
 Email Notifications - Budget alerts and monthly summaries via email
 Data Visualization - Interactive charts with Recharts or Chart.js
 Mobile App - React Native mobile application
 Bank Integration - Connect to bank APIs for automatic transaction import
 Split Expenses - Shared expenses with roommates/family
 Investment Tracking - Track stocks, crypto, and other investments
 Goal Setting - Savings goals with progress tracking
 Dark Mode - Theme switcher for better UX
 Two-Factor Authentication - Enhanced security with 2FA
 Social Features - Share financial tips and achievements
 API Rate Limiting - Implement throttling for security

🤝 Contributing
Contributions are welcome! Here's how you can help:

Fork the repository
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
👤 Author
Ashwaj Poojary

GitHub: @AshOP31244
Email: ashwajpoojary2@gmail.com
LinkedIn: [Add your LinkedIn URL]

🙏 Acknowledgments

Built as part of full-stack development portfolio
Inspired by modern fintech applications like Mint and YNAB
Django REST Framework documentation
React documentation and community
Tailwind CSS for beautiful UI components

📊 Project Statistics

Lines of Code: ~5,000+
API Endpoints: 20+
Database Tables: 6
React Components: 10+
Development Time: [Add your timeline]


⭐ Star this repository if you find it helpful!
Made with ❤️ and lots of ☕

---

## **Now Update Your GitHub:**
```powershell
cd D:\Projects\finance-tracker

# Add the new README
git add README.md

# Commit
git commit -m "docs: Add comprehensive README with full documentation"

# Push
git push
