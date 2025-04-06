from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                bank TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS balances (
                bank TEXT PRIMARY KEY,
                balance REAL
            )
        ''')
        for bank in ['SBI', 'BOB']:
            cur = conn.execute('SELECT * FROM balances WHERE bank = ?', (bank,))
            if not cur.fetchone():
                conn.execute('INSERT INTO balances (bank, balance) VALUES (?, ?)', (bank, 0))

@app.route('/')
def index():
    sort = request.args.get('sort', 'desc')
    selected_bank = request.args.get('bank', 'All')
    with get_db_connection() as conn:
        if selected_bank == 'All':
            query = f'SELECT * FROM expenses ORDER BY amount {sort}'
            expenses = conn.execute(query).fetchall()
        else:
            query = f'SELECT * FROM expenses WHERE bank = ? ORDER BY amount {sort}'
            expenses = conn.execute(query, (selected_bank,)).fetchall()

        balance_sbi = conn.execute('SELECT balance FROM balances WHERE bank = ?', ('SBI',)).fetchone()[0]
        balance_bob = conn.execute('SELECT balance FROM balances WHERE bank = ?', ('BOB',)).fetchone()[0]

    return render_template('index.html', expenses=expenses, selected_bank=selected_bank, balance_sbi=balance_sbi, balance_bob=balance_bob)

@app.route('/add', methods=['POST'])
def add_expense():
    amount = float(request.form['amount'])
    category = request.form['category']
    description = request.form['description']
    date = request.form['date']
    bank = request.form['bank']
    with get_db_connection() as conn:
        conn.execute('INSERT INTO expenses (amount, category, description, date, bank) VALUES (?, ?, ?, ?, ?)',
                     (amount, category, description, date, bank))
        conn.execute('UPDATE balances SET balance = balance - ? WHERE bank = ?', (amount, bank))
    return redirect('/')

@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    with get_db_connection() as conn:
        cur = conn.execute('SELECT amount, bank FROM expenses WHERE id = ?', (expense_id,)).fetchone()
        if cur:
            conn.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
            conn.execute('UPDATE balances SET balance = balance + ? WHERE bank = ?', (cur['amount'], cur['bank']))
    return redirect('/')

@app.route('/set-balance', methods=['POST'])
def set_balance():
    bank = request.form['bank']
    new_balance = float(request.form['new_balance'])
    with get_db_connection() as conn:
        conn.execute('UPDATE balances SET balance = ? WHERE bank = ?', (new_balance, bank))
    return redirect('/')

@app.route('/chart-data')
def chart_data():
    selected_bank = request.args.get('bank', 'All')
    with get_db_connection() as conn:
        if selected_bank == 'All':
            rows = conn.execute('SELECT category, SUM(amount) as total FROM expenses GROUP BY category').fetchall()
        else:
            rows = conn.execute('SELECT category, SUM(amount) as total FROM expenses WHERE bank = ? GROUP BY category', (selected_bank,)).fetchall()
        labels = [row['category'] for row in rows]
        data = [row['total'] for row in rows]
    return jsonify({'labels': labels, 'data': data})

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)