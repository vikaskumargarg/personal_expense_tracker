from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

DB_FILE = 'expenses.csv'

@app.route('/')
def index():
    try:
        df = pd.read_csv(DB_FILE)
        if df.empty:
            return render_template('index.html', message="No data available.")
    except pd.errors.EmptyDataError:
        return render_template('index.html', message="The CSV file is empty.")
    return render_template('index.html', data=df.to_html())

@app.route('/add', methods=['POST'])
def add_expense():
    date = request.form['date']
    description = request.form['description']
    amount = request.form['amount']
    new_expense = pd.DataFrame({
        'Date': [date],
        'Description': [description],
        'Amount': [amount]
    })
    try:
        df = pd.read_csv(DB_FILE)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=['Date', 'Description', 'Amount'])
    df = pd.concat([df, new_expense], ignore_index=True)
    df.to_csv(DB_FILE, index=False)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
