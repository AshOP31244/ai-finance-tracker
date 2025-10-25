import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import transactionService from '../services/transactionService';
import { formatCurrency, getCurrentMonthRange, formatDate } from '../utils/formatters';
import TransactionForm from '../components/TransactionForm';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [summary, setSummary] = useState(null);
  const [recentTransactions, setRecentTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showTransactionForm, setShowTransactionForm] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const { startDate, endDate } = getCurrentMonthRange();
      const summaryData = await transactionService.getSummary(startDate, endDate);
      setSummary(summaryData);
      
      // Fetch recent transactions
      try {
        const recentData = await transactionService.getTransactions();
        const transactions = recentData.results || recentData;
        setRecentTransactions(Array.isArray(transactions) ? transactions.slice(0, 5) : []);
      } catch (error) {
        console.error('Error fetching recent transactions:', error);
        setRecentTransactions([]);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const handleTransactionAdded = () => {
    fetchData();
    setShowTransactionForm(false);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 font-medium">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  const savingsRate = summary?.savings_rate || 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Enhanced Navbar */}
      <nav className="bg-white shadow-lg border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center space-x-3">
              <div className="text-3xl">💰</div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  Finance Tracker
                </h1>
                <p className="text-xs text-gray-500">Manage your money wisely</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="hidden md:block text-right">
                <p className="text-sm font-semibold text-gray-800">{user?.username}</p>
                <p className="text-xs text-gray-500">{user?.email}</p>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-50 rounded-lg transition-colors duration-200"
              >
                <span>🚪</span>
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header with Add Button */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h2 className="text-3xl font-bold text-gray-900">Dashboard</h2>
            <p className="text-gray-600 mt-1">Track your income and expenses</p>
          </div>
          <button
            onClick={() => setShowTransactionForm(!showTransactionForm)}
            className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-indigo-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
          >
            <span className="text-xl">{showTransactionForm ? '✕' : '+'}</span>
            <span>{showTransactionForm ? 'Close' : 'Add Transaction'}</span>
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Summary & Transactions */}
          <div className="lg:col-span-2 space-y-6">
            {/* Enhanced Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Income Card */}
              <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-2xl shadow-xl p-6 text-white transform hover:scale-105 transition-transform duration-200">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium opacity-90">Total Income</p>
                  <div className="text-3xl">💰</div>
                </div>
                <p className="text-3xl font-bold mb-1">
                  {formatCurrency(summary?.total_income || 0)}
                </p>
                <p className="text-xs opacity-75">This month</p>
              </div>

              {/* Expenses Card */}
              <div className="bg-gradient-to-br from-red-500 to-red-600 rounded-2xl shadow-xl p-6 text-white transform hover:scale-105 transition-transform duration-200">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium opacity-90">Total Expenses</p>
                  <div className="text-3xl">💸</div>
                </div>
                <p className="text-3xl font-bold mb-1">
                  {formatCurrency(summary?.total_expenses || 0)}
                </p>
                <p className="text-xs opacity-75">This month</p>
              </div>

              {/* Savings Card */}
              <div className="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl shadow-xl p-6 text-white transform hover:scale-105 transition-transform duration-200">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium opacity-90">Net Savings</p>
                  <div className="text-3xl">💵</div>
                </div>
                <p className="text-3xl font-bold mb-1">
                  {formatCurrency(summary?.net_savings || 0)}
                </p>
                <p className="text-xs opacity-75">
                  Savings rate: {savingsRate.toFixed(1)}%
                </p>
              </div>
            </div>

            {/* Category Breakdown */}
            {summary?.category_breakdown && summary.category_breakdown.length > 0 ? (
              <div className="bg-white rounded-2xl shadow-xl p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-bold text-gray-900">Spending by Category</h2>
                  <span className="text-sm text-gray-500">{summary.category_breakdown.length} categories</span>
                </div>
                <div className="space-y-4">
                  {summary.category_breakdown.map((cat, index) => {
                    const percentage = ((cat.total / summary.total_expenses) * 100).toFixed(1);
                    return (
                      <div key={index} className="group">
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center space-x-3">
                            <span className="text-2xl group-hover:scale-125 transition-transform duration-200">
                              {cat.category__icon}
                            </span>
                            <div>
                              <p className="font-semibold text-gray-800">{cat.category__name}</p>
                              <p className="text-xs text-gray-500">{cat.count} transactions</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="font-bold text-gray-900">{formatCurrency(cat.total)}</p>
                            <p className="text-xs text-gray-500">{percentage}%</p>
                          </div>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                          <div
                            className="h-2 rounded-full bg-gradient-to-r from-blue-500 to-indigo-600 transition-all duration-500"
                            style={{ width: `${percentage}%` }}
                          ></div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
                <div className="text-7xl mb-4 animate-bounce">📊</div>
                <h3 className="text-2xl font-bold text-gray-900 mb-2">No Transactions Yet</h3>
                <p className="text-gray-600 mb-6">Start tracking your finances by adding your first transaction!</p>
                <button
                  onClick={() => setShowTransactionForm(true)}
                  className="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-indigo-700 shadow-lg"
                >
                  Add Your First Transaction
                </button>
              </div>
            )}

            {/* Recent Transactions */}
            {recentTransactions.length > 0 && (
              <div className="bg-white rounded-2xl shadow-xl p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Transactions</h2>
                <div className="space-y-3">
                  {recentTransactions.map((transaction) => (
                    <div
                      key={transaction.id}
                      className="flex items-center justify-between p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors duration-200"
                    >
                      <div className="flex items-center space-x-3">
                        <div className="text-2xl">{transaction.category_icon || '📝'}</div>
                        <div>
                          <p className="font-semibold text-gray-800">{transaction.category_name || 'Uncategorized'}</p>
                          <p className="text-sm text-gray-500">{formatDate(transaction.date)}</p>
                          {transaction.description && (
                            <p className="text-xs text-gray-400 mt-1">{transaction.description}</p>
                          )}
                        </div>
                      </div>
                      <div className="text-right">
                        <p className={`font-bold text-lg ${
                          transaction.type === 'income' ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {transaction.type === 'income' ? '+' : '-'}{formatCurrency(transaction.amount)}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Right Column - Transaction Form */}
          {showTransactionForm && (
            <div className="lg:col-span-1">
              <div className="sticky top-20">
                <TransactionForm onSuccess={handleTransactionAdded} />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;