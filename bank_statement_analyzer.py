import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import pdfplumber
import re

# Function to classify transactions into categories
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

# Load bank statement data
def load_data(file_path):
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".pdf"):
        df = extract_pdf_data(file_path)
    else:
        raise ValueError("Unsupported file format")
    
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d", errors='coerce')
    df.dropna(subset=["Date"], inplace=True)
    df["Category"] = df["Description"].apply(categorize_transaction)
    return df

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
    plt.show()
