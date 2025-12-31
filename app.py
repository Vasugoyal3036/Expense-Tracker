from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from helpers import get_db, init_db, format_currency, get_expense_stats, get_monthly_data
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize database on startup
with app.app_context():
    init_db()


def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@login_required
def index():
    """Main dashboard showing expenses"""
    db = get_db()
    cursor = db.cursor()
    
    # Get user's expenses
    cursor.execute('''
        SELECT id, description, amount, category, date, created_at 
        FROM expenses 
        WHERE user_id = ? 
        ORDER BY date DESC, created_at DESC
    ''', (session['user_id'],))
    expenses = cursor.fetchall()
    
    # Get statistics
    stats = get_expense_stats(session['user_id'])
    monthly_data = get_monthly_data(session['user_id'])
    
    # Categories for the form
    categories = [
        'Food & Dining', 'Transportation', 'Shopping', 'Entertainment',
        'Bills & Utilities', 'Healthcare', 'Education', 'Travel', 'Other'
    ]
    
    return render_template('index.html', 
                         expenses=expenses, 
                         stats=stats,
                         monthly_data=monthly_data,
                         categories=categories,
                         format_currency=format_currency)


@app.route('/add_expense', methods=['POST'])
@login_required
def add_expense():
    """Add a new expense"""
    description = request.form.get('description', '').strip()
    amount = request.form.get('amount', '')
    category = request.form.get('category', '')
    date = request.form.get('date', '')
    
    # Validation
    if not description or not amount or not category or not date:
        flash('All fields are required!', 'error')
        return redirect(url_for('index'))
    
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive")
    except ValueError:
        flash('Please enter a valid amount!', 'error')
        return redirect(url_for('index'))
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO expenses (user_id, description, amount, category, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (session['user_id'], description, amount, category, date))
    db.commit()
    
    flash('Expense added successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    """Delete an expense"""
    db = get_db()
    cursor = db.cursor()
    
    # Verify the expense belongs to the user
    cursor.execute('SELECT id FROM expenses WHERE id = ? AND user_id = ?', 
                  (expense_id, session['user_id']))
    if not cursor.fetchone():
        flash('Expense not found!', 'error')
        return redirect(url_for('index'))
    
    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    db.commit()
    
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/edit_expense/<int:expense_id>', methods=['POST'])
@login_required
def edit_expense(expense_id):
    """Edit an existing expense"""
    description = request.form.get('description', '').strip()
    amount = request.form.get('amount', '')
    category = request.form.get('category', '')
    date = request.form.get('date', '')
    
    if not description or not amount or not category or not date:
        flash('All fields are required!', 'error')
        return redirect(url_for('index'))
    
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive")
    except ValueError:
        flash('Please enter a valid amount!', 'error')
        return redirect(url_for('index'))
    
    db = get_db()
    cursor = db.cursor()
    
    # Verify ownership
    cursor.execute('SELECT id FROM expenses WHERE id = ? AND user_id = ?', 
                  (expense_id, session['user_id']))
    if not cursor.fetchone():
        flash('Expense not found!', 'error')
        return redirect(url_for('index'))
    
    cursor.execute('''
        UPDATE expenses 
        SET description = ?, amount = ?, category = ?, date = ?
        WHERE id = ?
    ''', (description, amount, category, date, expense_id))
    db.commit()
    
    flash('Expense updated successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Please fill in all fields!', 'error')
            return render_template('login.html')
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = username
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or not email or not password or not confirm_password:
            flash('Please fill in all fields!', 'error')
            return render_template('register.html')
        
        if len(username) < 3:
            flash('Username must be at least 3 characters!', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters!', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        db = get_db()
        cursor = db.cursor()
        
        # Check if username exists
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            flash('Username already exists!', 'error')
            return render_template('register.html')
        
        # Check if email exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            flash('Email already registered!', 'error')
            return render_template('register.html')
        
        # Create user
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        ''', (username, email, password_hash))
        db.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/api/stats')
@login_required
def api_stats():
    """API endpoint for expense statistics"""
    stats = get_expense_stats(session['user_id'])
    monthly_data = get_monthly_data(session['user_id'])
    return jsonify({
        'stats': stats,
        'monthly_data': monthly_data
    })


if __name__ == '__main__':
    app.run(debug=True)
