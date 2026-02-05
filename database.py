from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import event

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    balance = db.Column(db.Float, default=10000.0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    positions = db.relationship('Position', back_populates='user', cascade='all, delete-orphan')
    buy_orders = db.relationship('Order', foreign_keys='Order.buyer_id', back_populates='buyer')
    sell_orders = db.relationship('Order', foreign_keys='Order.seller_id', back_populates='seller')
    trades_as_buyer = db.relationship('Trade', foreign_keys='Trade.buyer_id', back_populates='buyer')
    trades_as_seller = db.relationship('Trade', foreign_keys='Trade.seller_id', back_populates='seller')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'balance': self.balance
        }

class Meal(db.Model):
    __tablename__ = 'meals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(20), nullable=False)  # Chicken, Beef, Misc
    house_supply = db.Column(db.Integer, default=500, nullable=False)
    
    # Relationships
    positions = db.relationship('Position', back_populates='meal', cascade='all, delete-orphan')
    orders = db.relationship('Order', back_populates='meal', cascade='all, delete-orphan')
    trades = db.relationship('Trade', back_populates='meal', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'house_supply': self.house_supply
        }

class Position(db.Model):
    __tablename__ = 'positions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    shares = db.Column(db.Integer, default=0, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='positions')
    meal = db.relationship('Meal', back_populates='positions')
    
    # Unique constraint: one position per user per meal
    __table_args__ = (db.UniqueConstraint('user_id', 'meal_id', name='_user_meal_uc'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'meal_id': self.meal_id,
            'meal_name': self.meal.name,
            'shares': self.shares,
            'is_short': self.shares < 0
        }

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    order_type = db.Column(db.String(4), nullable=False)  # 'BID' or 'ASK'
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    remaining_quantity = db.Column(db.Integer, nullable=False)
    
    # For bids, buyer_id is set; for asks, seller_id is set
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    status = db.Column(db.String(20), default='ACTIVE', nullable=False)  # ACTIVE, FILLED, CANCELLED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    meal = db.relationship('Meal', back_populates='orders')
    buyer = db.relationship('User', foreign_keys=[buyer_id], back_populates='buy_orders')
    seller = db.relationship('User', foreign_keys=[seller_id], back_populates='sell_orders')
    
    def to_dict(self):
        return {
            'id': self.id,
            'meal_id': self.meal_id,
            'meal_name': self.meal.name,
            'order_type': self.order_type,
            'price': self.price,
            'quantity': self.quantity,
            'remaining_quantity': self.remaining_quantity,
            'user': self.buyer.username if self.buyer_id else self.seller.username,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

class Trade(db.Model):
    __tablename__ = 'trades'
    
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Nullable for IPO
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Nullable for IPO
    seller_name = db.Column(db.String(50), nullable=False)  # Store "IPO_HOUSE" for IPO trades
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    meal = db.relationship('Meal', back_populates='trades')
    buyer = db.relationship('User', foreign_keys=[buyer_id], back_populates='trades_as_buyer')
    seller = db.relationship('User', foreign_keys=[seller_id], back_populates='trades_as_seller')
    
    def to_dict(self):
        return {
            'id': self.id,
            'meal_id': self.meal_id,
            'meal_name': self.meal.name,
            'buyer': self.buyer.username if self.buyer else None,
            'seller': self.seller_name,
            'quantity': self.quantity,
            'price': self.price,
            'timestamp': self.timestamp.isoformat()
        }

class MarketState(db.Model):
    __tablename__ = 'market_state'
    
    id = db.Column(db.Integer, primary_key=True)
    ipo_start_time = db.Column(db.DateTime, nullable=True)
    ipo_active = db.Column(db.Boolean, default=False, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ipo_start_time': self.ipo_start_time.isoformat() if self.ipo_start_time else None,
            'ipo_active': self.ipo_active
        }