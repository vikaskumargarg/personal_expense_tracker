from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import matplotlib.pyplot as plt

# Initialize Flask app
app = Flask(__name__)

# Database file
DB_FILE = "expenses.csv"

# Initialize database if it doesn't exist
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    df.to_csv(DB_FILE, index=False)

@app.route('/')
def index():
    df = pd.read_csv(DB_FILE)
    return render_template("index.html", expenses=df.to_dict(orient="records"))

@app.route('/add', methods=["POST"])
def add_expense():
    data = {
        "Date": request.form["date"],
        "Category": request.form["category"],
        "Amount": float(request.form["amount"]),
        "Description": request.form["description"]
    }
    df = pd.read_csv(DB_FILE)
    df = df.append(data, ignore_index=True)
    df.to_csv(DB_FILE, index=False)
    return redirect(url_for("index"))

@app.route('/analytics')
def analytics():
    df = pd.read_csv(DB_FILE)
    if df.empty:
        return "No data available to display analytics."
    
    # Generate Pie Chart
    plt.figure(figsize=(8, 6))
    df.groupby("Category")["Amount"].sum().plot(kind="pie", autopct='%1.1f%%')
    plt.title("Spending by Category")
    plt.ylabel("")
    plt.savefig("static/analytics.png")
    plt.close()
    
    return render_template("analytics.html", image_path="/static/analytics.png")

if __name__ == '__main__':
    app.run(debug=True)
