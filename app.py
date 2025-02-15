from flask import Flask, request, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pdfplumber
import re
import os

app = Flask(__name__)

# Sample function to classify transactions into categories
def categorize_transaction(description):
    categories = {
        "food": ["restaurant", "cafe", "dining", "burger", "pizza"],
        "transport": ["uber", "bus", "metro", "taxi", "fuel"],
        "shopping": ["mall", "clothing", "electronics", "amazon", "flipkart"],
        "rent": ["rent", "landlord", "lease"],
        "bills": ["electricity", "water", "internet", "phone"]
    }
    for category, keywords in categories.items():
        if any(keyword in description.lower() for keyword in keywords):
            return category
    return "other"

# Extract text from PDF and parse into DataFrame
def extract_pdf_data(file_path):
    transactions = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")
            for line in lines:
                match = re.search(r'(\d{2}/\d{2}/\d{4})\s+([A-Za-z0-9 ]+)\s+(-?\d+\.\d+)', line)
                if match:
                    date, description, amount = match.groups()
                    transactions.append([date, description, float(amount)])
    return pd.DataFrame(transactions, columns=["Date", "Description", "Amount"])

# Generate Pie Chart of spending categories
def plot_spending_pie_chart(df):
    category_totals = df.groupby("Category")["Amount"].sum()
    plt.figure(figsize=(8, 6))
    category_totals.plot.pie(autopct='%1.1f%%', cmap="coolwarm", startangle=140)
    plt.title("Spending Breakdown by Category")
    plt.ylabel('')
    image_path = os.path.join("static", "spending_chart.png")
    plt.savefig(image_path)
    plt.close()
    return image_path

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".pdf"):
            file_path = os.path.join("uploads", file.filename)
            file.save(file_path)

            df = extract_pdf_data(file_path)
            df["Category"] = df["Description"].apply(categorize_transaction)
            chart_path = plot_spending_pie_chart(df)

            return render_template("index.html", chart_path=chart_path, table=df.to_html())

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
