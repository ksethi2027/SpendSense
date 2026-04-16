from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

students = Blueprint('students', __name__)


# GET /s/students/<user_id>/semesters — Budget expenses by semester [Jane-1]
@students.route('/students/<int:user_id>/semesters', methods=['GET'])
def get_semesters(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT s.sem_id, s.semName, s.startDate, s.endDate, s.totalBudget,
                   COALESCE(SUM(e.amount), 0) AS total_spent,
                   s.totalBudget - COALESCE(SUM(e.amount), 0) AS remaining_budget
            FROM Semester s
            LEFT JOIN Expense e ON e.user_id = s.user_id
                AND e.expenseDate BETWEEN s.startDate AND s.endDate
            WHERE s.user_id = %s
            GROUP BY s.sem_id, s.semName, s.startDate, s.endDate, s.totalBudget
            ORDER BY s.startDate DESC
        ''', (user_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# POST /s/students/<user_id>/semesters — Create a new semester [Jane-1]
@students.route('/students/<int:user_id>/semesters', methods=['POST'])
def create_semester(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.json
        cursor.execute('''
            INSERT INTO Semester (user_id, semName, startDate, endDate, totalBudget)
            VALUES (%s, %s, %s, %s, %s)
        ''', (user_id, data['semName'], data['startDate'], data['endDate'], data['totalBudget']))
        get_db().commit()
        return jsonify({'message': 'Semester created', 'sem_id': cursor.lastrowid}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /s/students/<user_id>/tuition — Track tuition payments [Jane-2]
@students.route('/students/<int:user_id>/tuition', methods=['GET'])
def get_tuition(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT tp.payment_id, s.semName, tp.amountDue, tp.amountPaid,
                   tp.amountDue - tp.amountPaid AS balance_remaining,
                   tp.dueDate, tp.paidDate, tp.status
            FROM Tuition_Payment tp
            JOIN Semester s ON s.sem_id = tp.sem_id
            WHERE s.user_id = %s
            ORDER BY tp.dueDate DESC
        ''', (user_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# PUT /s/tuition/<payment_id> — Update tuition payment [Jane-2]
@students.route('/tuition/<int:payment_id>', methods=['PUT'])
def update_tuition(payment_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.json
        cursor.execute('''
            UPDATE Tuition_Payment
            SET amountPaid = %s, paidDate = %s, status = %s
            WHERE payment_id = %s
        ''', (data['amountPaid'], data.get('paidDate'), data['status'], payment_id))
        get_db().commit()
        return jsonify({'message': 'Tuition payment updated'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /s/students/<user_id>/textbooks — Compare textbook prices [Jane-3]
@students.route('/students/<int:user_id>/textbooks', methods=['GET'])
def get_textbooks(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT t.textbook_id, t.title, t.courseName, t.isbn,
                   tp.vendor, tp.price, tp.`condition`
            FROM Textbook t
            JOIN Textbook_Price tp ON tp.textbook_id = t.textbook_id
            WHERE t.user_id = %s
            ORDER BY t.title, tp.price
        ''', (user_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /s/students/<user_id>/discounts — View active discounts [Jane-4]
@students.route('/students/<int:user_id>/discounts', methods=['GET'])
def get_discounts(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT sd.discount_id, sd.discountName, sd.discountCode,
                   sd.discountpct, sd.validFrom, sd.validUntil
            FROM Student_Discount sd
            WHERE sd.validUntil IS NULL OR sd.validUntil >= CURDATE()
            ORDER BY sd.discountpct DESC
        ''')
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /s/students/<user_id>/splits — Track split expenses [Jane-5]
@students.route('/students/<int:user_id>/splits', methods=['GET'])
def get_splits(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT e.expense_id, e.description AS expense_description,
                   e.amount AS total_amount, f.friendName,
                   se.shareAmount, se.status, se.settledDate
            FROM Expense e
            JOIN Split_Expense se ON se.expense_id = e.expense_id
            JOIN Friend f ON f.friend_id = se.friend_id
            WHERE e.user_id = %s
            ORDER BY e.expenseDate DESC
        ''', (user_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# PUT /s/splits/<split_id> — Settle a split expense [Jane-5]
@students.route('/splits/<int:split_id>', methods=['PUT'])
def settle_split(split_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.json
        cursor.execute('''
            UPDATE Split_Expense
            SET status = %s, settledDate = %s
            WHERE split_id = %s
        ''', (data['status'], data.get('settledDate'), split_id))
        get_db().commit()
        return jsonify({'message': 'Split expense updated'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /s/students/<user_id>/savings — View savings goals [Jane-6]
@students.route('/students/<int:user_id>/savings', methods=['GET'])
def get_savings(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT goal_id, goalName, targetAmount, savedAmount,
                   targetAmount - savedAmount AS amount_remaining,
                   ROUND(savedAmount / targetAmount * 100, 1) AS pct_complete,
                   targetDate
            FROM Savings_Goal
            WHERE user_id = %s
            ORDER BY targetDate
        ''', (user_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# POST /s/students/<user_id>/savings — Create a savings goal [Jane-6]
@students.route('/students/<int:user_id>/savings', methods=['POST'])
def create_savings_goal(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.json
        cursor.execute('''
            INSERT INTO Savings_Goal (user_id, goalName, targetAmount, savedAmount, targetDate)
            VALUES (%s, %s, %s, %s, %s)
        ''', (user_id, data['goalName'], data['targetAmount'],
              data.get('savedAmount', 0), data.get('targetDate')))
        get_db().commit()
        return jsonify({'message': 'Savings goal created', 'goal_id': cursor.lastrowid}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# PUT /s/savings/<goal_id> — Update a savings goal [Jane-6]
@students.route('/savings/<int:goal_id>', methods=['PUT'])
def update_savings_goal(goal_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.json
        fields = []
        params = []
        for col in ['goalName', 'targetAmount', 'savedAmount', 'targetDate']:
            if col in data:
                fields.append(f'{col} = %s')
                params.append(data[col])
        if not fields:
            return jsonify({'error': 'No fields to update'}), 400
        params.append(goal_id)
        cursor.execute(f'UPDATE Savings_Goal SET {", ".join(fields)} WHERE goal_id = %s', params)
        get_db().commit()
        return jsonify({'message': 'Savings goal updated'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# DELETE /s/savings/<goal_id> — Delete a savings goal [Jane-6]
@students.route('/savings/<int:goal_id>', methods=['DELETE'])
def delete_savings_goal(goal_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('DELETE FROM Savings_Goal WHERE goal_id = %s', (goal_id,))
        get_db().commit()
        return jsonify({'message': 'Savings goal deleted'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# POST /s/students/<user_id>/expenses — Log an expense [Jane-1, Jane-3]
@students.route('/students/<int:user_id>/expenses', methods=['POST'])
def add_expense(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.json
        cursor.execute('''
            INSERT INTO Expense (user_id, category_id, amount, description,
                                 expenseDate, is_academic, is_shared)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (user_id, data['category_id'], data['amount'], data.get('description', ''),
              data['expenseDate'], data.get('is_academic', 0), data.get('is_shared', 0)))
        get_db().commit()
        return jsonify({'message': 'Expense added', 'expense_id': cursor.lastrowid}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /s/students/<user_id>/expenses — Get all expenses [Jane-1]
@students.route('/students/<int:user_id>/expenses', methods=['GET'])
def get_expenses(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT e.expense_id, e.amount, e.description, e.expenseDate,
                   e.is_academic, e.is_shared, ec.categoryName
            FROM Expense e
            JOIN Expense_Category ec ON ec.category_id = e.category_id
            WHERE e.user_id = %s
            ORDER BY e.expenseDate DESC
        ''', (user_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
