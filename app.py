from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this before deploying!

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# In-memory users store: user_id -> User instance
users = {}

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

# In-memory expenses list
expenses = []
next_expense_id = 1  # incremental ID for expenses

# Routes

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if any(u.username == username for u in users.values()):
            flash('Username already exists!')
            return redirect(url_for('register'))

        user_id = len(users) + 1
        password_hash = generate_password_hash(password)
        users[user_id] = User(user_id, username, password_hash)
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = next((u for u in users.values() if u.username == username), None)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))

        flash('Invalid username or password')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    # Show only current user's expenses
    user_expenses = [e for e in expenses if e['user_id'] == current_user.id]
    return render_template('index.html', expenses=user_expenses)

@app.route('/add', methods=['POST'])
@login_required
def add_expense():
    global next_expense_id
    item = request.form['item']
    amount = float(request.form['amount'])
    date = datetime.date.today().strftime("%Y-%m-%d")
    expenses.append({
        'id': next_expense_id,
        'item': item,
        'amount': amount,
        'date': date,
        'user_id': current_user.id
    })
    next_expense_id += 1
    return redirect(url_for('index'))

@app.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = next((e for e in expenses if e['id'] == expense_id and e['user_id'] == current_user.id), None)
    if not expense:
        return "Expense not found or not authorized", 404

    if request.method == 'POST':
        expense['item'] = request.form['item']
        expense['amount'] = float(request.form['amount'])
        # Optionally update date here
        return redirect(url_for('index'))

    return render_template('edit.html', expense=expense)

@app.route('/delete/<int:expense_id>')
@login_required
def delete_expense(expense_id):
    global expenses
    expenses = [e for e in expenses if not (e['id'] == expense_id and e['user_id'] == current_user.id)]
    return redirect(url_for('index'))

@app.route('/summary', methods=['GET', 'POST'])
@login_required
def summary():
    filtered_expenses = []
    total = 0
    selected_month = ""
    category_totals = defaultdict(float)

    if request.method == 'POST':
        selected_month = request.form['month']  # e.g., "2025-08"
        for e in expenses:
            if e['user_id'] == current_user.id and e['date'].startswith(selected_month):
                filtered_expenses.append(e)
                total += e['amount']
                category_totals[e['item']] += e['amount']

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    return render_template('summary.html',
                           expenses=filtered_expenses,
                           total=total,
                           month=selected_month,
                           categories=categories,
                           amounts=amounts)

if __name__ == '__main__':
    app.run(debug=True)
