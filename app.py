from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import os
from models import Market
from config import FRIENDS, ALL_MEALS

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize market
market = Market()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    if username in FRIENDS:
        session['user'] = username
        return jsonify({'success': True, 'user': username})
    return jsonify({'success': False, 'message': 'Invalid user'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'success': True})

@app.route('/api/current_user')
def current_user():
    user = session.get('user')
    if user:
        return jsonify({
            'username': user,
            'balance': market.get_balance(user),
            'ipo_price': market.get_current_ipo_price()
        })
    return jsonify({'username': None}), 401

@app.route('/api/market_summary')
def market_summary():
    return jsonify(market.get_market_summary())

@app.route('/api/start_ipo', methods=['POST'])
def start_ipo():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    market.start_ipo()
    return jsonify({'success': True, 'ipo_price': market.get_current_ipo_price()})

@app.route('/api/buy_ipo', methods=['POST'])
def buy_ipo():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    user = session['user']
    meal = request.json.get('meal')
    qty = request.json.get('qty')
    
    success, message = market.buy_from_ipo(user, meal, qty)
    return jsonify({'success': success, 'message': message})

@app.route('/api/secondary_buy', methods=['POST'])
def secondary_buy():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    user = session['user']
    meal = request.json.get('meal')
    price = request.json.get('price')
    qty = request.json.get('qty')
    snap_buy = request.json.get('snap_buy', False)
    
    success, message, trades = market.place_buy_order(user, meal, price, qty, snap_buy)
    return jsonify({'success': success, 'message': message, 'trades': trades})

@app.route('/api/sell', methods=['POST'])
def sell():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    user = session['user']
    meal = request.json.get('meal')
    price = request.json.get('price')
    qty = request.json.get('qty')
    is_short = request.json.get('is_short', False)
    
    success, message, trades = market.place_sell_order(user, meal, price, qty, is_short)
    return jsonify({'success': success, 'message': message, 'trades': trades})

@app.route('/api/portfolio')
def portfolio():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    user = session['user']
    return jsonify(market.get_portfolio(user))

@app.route('/api/trade_history')
def trade_history():
    return jsonify(market.get_trade_history(limit=20))

@app.route('/api/order_book/<meal>')
def order_book(meal):
    return jsonify(market.get_order_book(meal))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)