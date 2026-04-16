from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

admin = Blueprint('admin', __name__)


# GET /ad/categories — List all expense categories [Mary-1]
@admin.route('/categories', methods=['GET'])
def get_categories():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM Expense_Category ORDER BY categoryName')
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# POST /ad/categories — Create new expense category [Mary-1]
@admin.route('/categories', methods=['POST'])
def create_category():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.json
        cursor.execute('''
            INSERT INTO Expense_Category (categoryName, description)
            VALUES (%s, %s)
        ''', (data['categoryName'], data.get('description', '')))
        get_db().commit()
        return jsonify({'message': 'Category created', 'category_id': cursor.lastrowid}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# PUT /ad/categories/<category_id> — Update a category [Mary-2]
@admin.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.json
        fields = []
        params = []
        for col in ['categoryName', 'description']:
            if col in data:
                fields.append(f'{col} = %s')
                params.append(data[col])
        if not fields:
            return jsonify({'error': 'No fields to update'}), 400
        params.append(category_id)
        cursor.execute(
            f'UPDATE Expense_Category SET {", ".join(fields)} WHERE category_id = %s',
            params
        )
        get_db().commit()
        return jsonify({'message': 'Category updated'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# DELETE /ad/categories/<category_id> — Delete a category [Mary-4]
@admin.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('DELETE FROM Expense_Category WHERE category_id = %s', (category_id,))
        get_db().commit()
        return jsonify({'message': 'Category deleted'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /ad/logs — View system activity [Mary-3]
@admin.route('/logs', methods=['GET'])
def get_logs():
    cursor = get_db().cursor(dictionary=True)
    try:
        limit = request.args.get('limit', 50, type=int)
        cursor.execute('''
            SELECT al.log_id, u.first_name, u.last_name, u.role_type,
                   al.action_type, al.target_table, al.target_id,
                   al.description, al.timestamp
            FROM Admin_Log al
            JOIN User u ON u.user_id = al.user_id
            ORDER BY al.timestamp DESC
            LIMIT %s
        ''', (limit,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /ad/users — List all users [Mary-5]
@admin.route('/users', methods=['GET'])
def get_users():
    cursor = get_db().cursor(dictionary=True)
    try:
        role = request.args.get('role')
        query = 'SELECT user_id, first_name, last_name, email, university, role_type FROM User'
        params = []
        if role:
            query += ' WHERE role_type = %s'
            params.append(role)
        query += ' ORDER BY last_name, first_name'
        cursor.execute(query, params)
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# PUT /ad/users/<user_id> — Update user role [Mary-5]
@admin.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.json
        fields = []
        params = []
        for col in ['first_name', 'last_name', 'email', 'role_type', 'university']:
            if col in data:
                fields.append(f'{col} = %s')
                params.append(data[col])
        if not fields:
            return jsonify({'error': 'No fields to update'}), 400
        params.append(user_id)
        cursor.execute(f'UPDATE User SET {", ".join(fields)} WHERE user_id = %s', params)
        get_db().commit()
        return jsonify({'message': 'User updated'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /ad/validation — Run data validation checks [Mary-6]
@admin.route('/validation', methods=['GET'])
def validate_data():
    cursor = get_db().cursor(dictionary=True)
    try:
        issues = []
        cursor.execute('''
            SELECT 'Negative expense' AS issue_type, expense_id AS record_id,
                   CAST(amount AS CHAR) AS bad_value
            FROM Expense WHERE amount <= 0
        ''')
        issues.extend(cursor.fetchall())

        cursor.execute('''
            SELECT 'Tuition overpaid' AS issue_type, payment_id AS record_id,
                   CAST(amountPaid AS CHAR) AS bad_value
            FROM Tuition_Payment WHERE amountPaid > amountDue
        ''')
        issues.extend(cursor.fetchall())

        cursor.execute('''
            SELECT 'Bad semester dates' AS issue_type, sem_id AS record_id,
                   CONCAT(startDate, ' -> ', endDate) AS bad_value
            FROM Semester WHERE endDate <= startDate
        ''')
        issues.extend(cursor.fetchall())

        return jsonify({'issues': issues, 'count': len(issues)}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
