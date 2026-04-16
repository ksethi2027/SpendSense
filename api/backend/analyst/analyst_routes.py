from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

analyst = Blueprint('analyst', __name__)


# GET /a/analyst/<analyst_id>/reports — Monthly summary reports [John-1]
@analyst.route('/analyst/<int:analyst_id>/reports', methods=['GET'])
def get_reports(analyst_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT pr.report_id, p.portfolio_name, tp.start_date, tp.end_date,
                   pr.report_type, pr.summary_text, pr.generated_at
            FROM Performance_Report pr
            JOIN Portfolio p ON p.portfolio_id = pr.portfolio_id
            JOIN Time_Period tp ON tp.period_id = pr.period_id
            WHERE pr.analyst_id = %s
            ORDER BY tp.start_date DESC
        ''', (analyst_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# POST /a/analyst/<analyst_id>/reports — Generate a new report [John-1]
@analyst.route('/analyst/<int:analyst_id>/reports', methods=['POST'])
def create_report(analyst_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.json
        cursor.execute('''
            INSERT INTO Performance_Report
                (analyst_id, portfolio_id, period_id, report_type, summary_text)
            VALUES (%s, %s, %s, %s, %s)
        ''', (analyst_id, data['portfolio_id'], data['period_id'],
              data['report_type'], data.get('summary_text', '')))
        get_db().commit()
        return jsonify({'message': 'Report created', 'report_id': cursor.lastrowid}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /a/analyst/<analyst_id>/spending — Aggregated spending data [John-2, John-4]
@analyst.route('/analyst/<int:analyst_id>/spending', methods=['GET'])
def get_spending_summaries(analyst_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT u.user_id, u.first_name, u.last_name,
                   tp.start_date, tp.end_date, tp.granularity,
                   ss.total_spent, ss.avg_spending, ss.trend_direction
            FROM Spending_Summary ss
            JOIN User u ON u.user_id = ss.user_id
            JOIN Time_Period tp ON tp.period_id = ss.period_id
            WHERE ss.analyst_id = %s
            ORDER BY ss.total_spent DESC
        ''', (analyst_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /a/portfolios/<portfolio_id> — Portfolio details [John-5]
@analyst.route('/portfolios/<int:portfolio_id>', methods=['GET'])
def get_portfolio(portfolio_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM Portfolio WHERE portfolio_id = %s', (portfolio_id,))
        portfolio = cursor.fetchone()
        if not portfolio:
            return jsonify({'error': 'Portfolio not found'}), 404
        cursor.execute('''
            SELECT holding_id, asset_name, asset_type, quantity,
                   current_value, allocation_pct
            FROM Holding WHERE portfolio_id = %s
        ''', (portfolio_id,))
        portfolio['holdings'] = cursor.fetchall()
        return jsonify(portfolio), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /a/portfolios/<portfolio_id>/transactions — Transaction history [John-5]
@analyst.route('/portfolios/<int:portfolio_id>/transactions', methods=['GET'])
def get_portfolio_transactions(portfolio_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT transaction_id, transaction_date, transaction_type, amount
            FROM Portfolio_Transaction
            WHERE portfolio_id = %s
            ORDER BY transaction_date DESC
        ''', (portfolio_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /a/portfolios/<portfolio_id>/risk — Risk vs return data [John-3, John-6]
@analyst.route('/portfolios/<int:portfolio_id>/risk', methods=['GET'])
def get_risk_profile(portfolio_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT p.portfolio_name, rr.risk_level,
                   ROUND(rr.return_rate * 100, 2) AS return_pct,
                   ROUND(rr.volatility * 100, 2) AS volatility_pct,
                   ROUND(rr.return_rate / NULLIF(rr.volatility, 0), 4) AS sharpe_proxy,
                   tp.start_date, tp.end_date
            FROM Risk_Return_Profile rr
            JOIN Portfolio p ON p.portfolio_id = rr.portfolio_id
            JOIN Time_Period tp ON tp.period_id = rr.period_id
            WHERE rr.portfolio_id = %s
            ORDER BY tp.start_date DESC
        ''', (portfolio_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# GET /a/portfolios/all — Get all portfolios (for analyst dashboard) [John-5]
@analyst.route('/portfolios/all', methods=['GET'])
def get_all_portfolios():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''
            SELECT p.portfolio_id, p.portfolio_name, p.total_value, p.created_at,
                   u.first_name, u.last_name
            FROM Portfolio p
            JOIN User u ON u.user_id = p.user_id
            ORDER BY p.total_value DESC
        ''')
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
