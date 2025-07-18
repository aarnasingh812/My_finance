from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime

bills_bp = Blueprint('bills', __name__)

DATA_FILE = 'bills_data.json'

# Utility functions
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def get_month_key(month=None, year=None):
    now = datetime.now()
    if not month:
        month = now.month
    if not year:
        year = now.year
    return f"{year}-{month:02d}"

# API Endpoints
@bills_bp.route('/bills', methods=['POST'])
def add_bill():
    data = request.json
    bill_type = data.get('type')
    amount = data.get('amount')
    month = data.get('month')
    year = data.get('year')

    if not bill_type or not isinstance(amount, (int, float)):
        return jsonify({"error": "Invalid input"}), 400

    bills_data = load_data()
    month_key = get_month_key(month, year)

    if month_key not in bills_data:
        bills_data[month_key] = []

    bills_data[month_key].append({
        "type": bill_type,
        "amount": amount
    })

    save_data(bills_data)
    return jsonify({"message": f"Bill added for {month_key}"}), 201

@bills_bp.route('/bills/<int:year>/<int:month>', methods=['GET'])
def get_bills(year, month):
    bills_data = load_data()
    month_key = get_month_key(month, year)

    if month_key not in bills_data:
        return jsonify({"message": f"No bills found for {month_key}"}), 404

    bills = bills_data[month_key]
    total = sum(bill["amount"] for bill in bills)

    return jsonify({
        "month": month_key,
        "bills": bills,
        "total": total
    }), 200