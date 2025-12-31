import sqlite3
from flask import g
from datetime import datetime, timedelta

DATABASE = 'expenses.db'


def get_db():
    """Get database connection"""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    """Initialize the database with tables"""
    db = get_db()
    cursor = db.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    db.commit()


def format_currency(amount):
    """Format amount as currency"""
    return f"${amount:,.2f}"


def get_expense_stats(user_id):
    """Get expense statistics for a user"""
    db = get_db()
    cursor = db.cursor()
    
    # Total expenses
    cursor.execute('SELECT COALESCE(SUM(amount), 0) as total FROM expenses WHERE user_id = ?', (user_id,))
    total = cursor.fetchone()['total']
    
    # This month's expenses
    first_day = datetime.now().replace(day=1).strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT COALESCE(SUM(amount), 0) as monthly 
        FROM expenses 
        WHERE user_id = ? AND date >= ?
    ''', (user_id, first_day))
    monthly = cursor.fetchone()['monthly']
    
    # This week's expenses
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT COALESCE(SUM(amount), 0) as weekly 
        FROM expenses 
        WHERE user_id = ? AND date >= ?
    ''', (user_id, week_ago))
    weekly = cursor.fetchone()['weekly']
    
    # Expenses by category
    cursor.execute('''
        SELECT category, SUM(amount) as total 
        FROM expenses 
        WHERE user_id = ? 
        GROUP BY category 
        ORDER BY total DESC
    ''', (user_id,))
    by_category = [dict(row) for row in cursor.fetchall()]
    
    # Count of transactions
    cursor.execute('SELECT COUNT(*) as count FROM expenses WHERE user_id = ?', (user_id,))
    transaction_count = cursor.fetchone()['count']
    
    # Average expense
    avg_expense = total / transaction_count if transaction_count > 0 else 0
    
    return {
        'total': total,
        'monthly': monthly,
        'weekly': weekly,
        'by_category': by_category,
        'transaction_count': transaction_count,
        'average': avg_expense
    }


def get_monthly_data(user_id):
    """Get monthly expense data for charts"""
    db = get_db()
    cursor = db.cursor()
    
    # Get last 6 months of data
    months = []
    for i in range(5, -1, -1):
        date = datetime.now() - timedelta(days=i*30)
        month_start = date.replace(day=1).strftime('%Y-%m-%d')
        if date.month == 12:
            next_month = date.replace(year=date.year + 1, month=1, day=1)
        else:
            next_month = date.replace(month=date.month + 1, day=1)
        month_end = next_month.strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT COALESCE(SUM(amount), 0) as total 
            FROM expenses 
            WHERE user_id = ? AND date >= ? AND date < ?
        ''', (user_id, month_start, month_end))
        
        months.append({
            'month': date.strftime('%b'),
            'total': cursor.fetchone()['total']
        })
    
    return months
