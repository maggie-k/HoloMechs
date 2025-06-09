from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flashing messages

def init_db():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, 'models.db')

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS vehicles (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER, make TEXT, model TEXT, year INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS services (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER, vehicle_id INTEGER, service_type TEXT, status TEXT)''')
    conn.commit()
    conn.close()

def get_db_connection():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'data', 'models.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        # Skip DB check and accept all logins
        flash(f'Welcome, {username}! Login successful!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/request', methods=['GET', 'POST'])
def request_service():
    if request.method == 'POST':
        service_type = request.form.get('service_type')
        if not service_type:
            flash('Please select a service type.', 'warning')
            return redirect(url_for('request_service'))

        # Here you'd save the service request to DB, using dummy user_id=1 for now
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO services (user_id, vehicle_id, service_type, status) VALUES (?, ?, ?, ?)',
            (1, None, service_type, 'Pending')
        )
        conn.commit()
        conn.close()

        flash(f'Service request for "{service_type}" submitted!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('request_service.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
