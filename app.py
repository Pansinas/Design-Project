from flask import Flask, render_template, request
from bank_statement_analyzer import load_data, plot_spending_pie_chart, predict_future_expense

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return "No file uploaded", 400
    
    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    df = load_data(file)
    plot_spending_pie_chart(df)
    future_expense = predict_future_expense(df)
    
    return f"Predicted Expense for Next Month: ₹{future_expense:.2f}"

if __name__ == "__main__":
    app.run(debug=True)
