from flask import Flask, render_template, request, jsonify
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

app = Flask(__name__)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("service_account.json", scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("medical_equipment_troubleshooter").sheet1

def load_data():
    return pd.DataFrame(sheet.get_all_records())

@app.route('/')
def index():
    data = load_data()
    products = sorted(data["Product"].unique())
    return render_template('index.html', products=products)

@app.route('/get_errors', methods=['POST'])
def get_errors():
    product = request.json['product']
    data = load_data()
    errors = sorted(data[data["Product"] == product]["Error"].unique())
    return jsonify(errors)

@app.route('/get_solution', methods=['POST'])
def get_solution():
    product = request.json['product']
    error = request.json['error']
    data = load_data()
    result = data[(data["Product"] == product) & (data["Error"] == error)]
    solution = result.iloc[0]['Solution'] if not result.empty else "No solution found"
    return jsonify(solution)

@app.route('/add_entry', methods=['POST'])
def add_entry():
    new_product = request.form['product']
    new_error = request.form['error']
    new_solution = request.form['solution']
    sheet.append_row([new_product, new_error, new_solution])
    return "Added successfully"

if __name__ == '__main__':
    app.run(debug=True)
