from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

employee = Blueprint('employee', __name__)


# GET /e/employee/<user_id>/expenses — Track personal expenses [Marcus-1]
@employee.route('/employee/<int:user_id>/expenses', methods=['GET'])
def get_expenses_by_category(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT ec.categoryName, SUM(e.amount) AS total_spent,
                   COUNT(*) AS num_transactions,
                   MIN(e.expenseDate) AS first_expense,
                   MAX(e.expenseDate) AS last_expense
            FROM Expense e
            JOIN Expense_Category ec ON ec.category_id = e.category_id
            WHERE e.user_id = %s
            GROUP BY ec.categoryName
            ORDER BY total_spent DESC
        ''', (user_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# POST /e/employee/<user_id>/expenses — Add an expense [Marcus-1]
@employee.route('/employee/<int:user_id>/expenses', methods=['POST'])
def add_expense(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.json
        cursor.execute('''
            INSERT INTO Expense (user_id, category_id, amount, description,
                                 expenseDate, is_academic, is_shared)
            VALUES (%s, %s, %s, %s, %s, 0, 0)
        ''', (user_id, data['category_id'], data['amount'],
              data.get('description', ''), data['expenseDate']))
        get_db().commit()
        return jsonify({'message': 'Expense added', 'expense_id': cursor.lastrowid}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# DELETE /e/expenses/<expense_id> — Delete an expense [Marcus-1]
@employee.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('DELETE FROM Expense WHERE expense_id = %s', (expense_id,))
        get_db().commit()
        return jsonify({'message': 'Expense deleted'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /e/employee/<user_id>/income — Get all income records [Marcus-2]
@employee.route('/employee/<int:user_id>/income', methods=['GET'])
def get_income(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT income_id, category_income, amount_income, date_income
            FROM Income
            WHERE user_id = %s
            ORDER BY date_income DESC
        ''', (user_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# POST /e/employee/<user_id>/income — Log income [Marcus-2]
@employee.route('/employee/<int:user_id>/income', methods=['POST'])
def add_income(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.json
        cursor.execute('''
            INSERT INTO Income (user_id, category_income, amount_income, date_income)
            VALUES (%s, %s, %s, %s)
        ''', (user_id, data['category_income'], data['amount_income'], data['date_income']))
        get_db().commit()
        return jsonify({'message': 'Income recorded', 'income_id': cursor.lastrowid}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /e/employee/<user_id>/investments — Get holdings [Marcus-3]
@employee.route('/employee/<int:user_id>/investments', methods=['GET'])
def get_investments(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT p.portfolio_id, p.portfolio_name, p.total_value,
                   h.holding_id, h.asset_name, h.asset_type,
                   h.quantity, h.current_value, h.allocation_pct
            FROM Portfolio p
            JOIN Holding h ON h.portfolio_id = p.portfolio_id
            WHERE p.user_id = %s
            ORDER BY p.portfolio_name, h.current_value DESC
        ''', (user_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# PUT /e/investments/<holding_id> — Update investment [Marcus-3]
@employee.route('/investments/<int:holding_id>', methods=['PUT'])
def update_investment(holding_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.json
        fields = []
        params = []
        for col in ['current_value', 'allocation_pct', 'quantity']:
            if col in data:
                fields.append(f'{col} = %s')
                params.append(data[col])
        if not fields:
            return jsonify({'error': 'No fields to update'}), 400
        params.append(holding_id)
        cursor.execute(f'UPDATE Holding SET {", ".join(fields)} WHERE holding_id = %s', params)
        get_db().commit()
        return jsonify({'message': 'Investment updated'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /e/employee/<user_id>/peer-transactions — P2P transactions [Marcus-4]
@employee.route('/employee/<int:user_id>/peer-transactions', methods=['GET'])
def get_peer_transactions(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT transaction_id, platform, counterparty_name,
                   amount, direction, date_t
            FROM Peer_Transaction
            WHERE user_id = %s
            ORDER BY date_t DESC
        ''', (user_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /e/employee/<user_id>/insurance — Insurance records [Marcus-5]
@employee.route('/employee/<int:user_id>/insurance', methods=['GET'])
def get_insurance(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT insurance_id, category_i AS insurance_type, provider,
                   monthly_premium, due_date AS due_day_of_month,
                   monthly_premium * 12 AS annual_cost
            FROM Insurance
            WHERE user_id = %s
            ORDER BY due_date
        ''', (user_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /e/employee/<user_id>/housing-bills — Housing bills [Marcus-6]
@employee.route('/employee/<int:user_id>/housing-bills', methods=['GET'])
def get_housing_bills(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT bill_id, category_hb AS bill_type, amount_hb,
                   due_date_hb, paid_date,
                   CASE
                     WHEN paid_date IS NOT NULL THEN 'Paid'
                     WHEN due_date_hb < CURDATE() THEN 'Overdue'
                     ELSE 'Upcoming'
                   END AS payment_status
            FROM Housing_Bill
            WHERE user_id = %s
            ORDER BY due_date_hb DESC
        ''', (user_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# PUT /e/housing-bills/<bill_id> — Mark a bill as paid [Marcus-6]
@employee.route('/housing-bills/<int:bill_id>', methods=['PUT'])
def update_housing_bill(bill_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.json
        cursor.execute('''
            UPDATE Housing_Bill SET paid_date = %s WHERE bill_id = %s
        ''', (data['paid_date'], bill_id))
        get_db().commit()
        return jsonify({'message': 'Bill updated'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
