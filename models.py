import time
from config import (
    FRIENDS, ALL_MEALS, INITIAL_BALANCE, INITIAL_HOUSE_SUPPLY,
    IPO_START_PRICE, IPO_DECAY_RATE, IPO_DECAY_INTERVAL, MEAL_CATEGORIES
)

class Market:
    def __init__(self):
        self.balances = {name: INITIAL_BALANCE for name in FRIENDS}
        self.portfolios = {name: {meal: 0 for meal in ALL_MEALS} for name in FRIENDS}
        self.house_supply = {meal: INITIAL_HOUSE_SUPPLY for meal in ALL_MEALS}
        self.trade_history = []
        self.ipo_start_time = None
        self.asks = {meal: [] for meal in ALL_MEALS}
        self.bids = {meal: [] for meal in ALL_MEALS}
    
    def get_current_ipo_price(self):
        """Calculate current IPO price based on time elapsed"""
        if self.ipo_start_time is None:
            return IPO_START_PRICE
        elapsed = time.time() - self.ipo_start_time
        decay = int(elapsed // IPO_DECAY_INTERVAL) * IPO_DECAY_RATE
        return max(0.0, IPO_START_PRICE - decay)
    
    def start_ipo(self):
        """Start the IPO clock"""
        if self.ipo_start_time is None:
            self.ipo_start_time = time.time()
        return True
    
    def get_balance(self, user):
        """Get user's cash balance"""
        return self.balances.get(user, 0.0)
    
    def get_portfolio(self, user):
        """Get user's portfolio with non-zero positions"""
        portfolio = {}
        for meal, shares in self.portfolios[user].items():
            if shares != 0:
                portfolio[meal] = {
                    'shares': shares,
                    'is_short': shares < 0
                }
        return portfolio
    
    def get_best_ask(self, meal):
        """Get lowest ask price for a meal"""
        if not self.asks[meal]:
            return None
        return min(self.asks[meal], key=lambda x: x['price'])
    
    def get_best_bid(self, meal):
        """Get highest bid price for a meal"""
        if not self.bids[meal]:
            return None
        return max(self.bids[meal], key=lambda x: x['price'])
    
    def get_market_summary(self):
        """Get market overview with all meals"""
        ipo_price = self.get_current_ipo_price()
        summary = {
            'ipo_price': ipo_price,
            'ipo_active': self.ipo_start_time is not None,
            'meals': []
        }
        
        for meal in ALL_MEALS:
            best_ask = self.get_best_ask(meal)
            best_bid = self.get_best_bid(meal)
            
            # Determine category
            category = 'Misc'
            for cat_name, cat_meals in MEAL_CATEGORIES.items():
                if meal in cat_meals:
                    category = cat_name
                    break
            
            meal_data = {
                'name': meal,
                'category': category,
                'house_supply': self.house_supply[meal],
                'best_ask': best_ask['price'] if best_ask else None,
                'best_bid': best_bid['price'] if best_bid else None,
                'spread': (best_ask['price'] - best_bid['price']) if (best_ask and best_bid) else None
            }
            summary['meals'].append(meal_data)
        
        return summary
    
    def get_order_book(self, meal):
        """Get full order book for a specific meal"""
        return {
            'meal': meal,
            'asks': sorted(self.asks[meal], key=lambda x: x['price']),
            'bids': sorted(self.bids[meal], key=lambda x: x['price'], reverse=True)
        }
    
    def execute_trade(self, buyer, seller, meal, price, qty, listing=None):
        """Execute a trade between buyer and seller"""
        cost = price * qty
        
        # Update balances
        self.balances[buyer] -= cost
        if seller != "IPO_HOUSE":
            self.balances[seller] += cost
        
        # Transfer shares
        self.portfolios[buyer][meal] += qty
        if seller != "IPO_HOUSE":
            self.portfolios[seller][meal] -= qty
        
        # Record trade
        trade = {
            'timestamp': time.time(),
            'meal': meal,
            'buyer': buyer,
            'seller': seller,
            'qty': qty,
            'price': price
        }
        self.trade_history.append(trade)
        
        # Cleanup order book
        if listing:
            listing['qty'] -= qty
            if listing['qty'] <= 0:
                if 'seller' in listing:
                    self.asks[meal].remove(listing)
                else:
                    self.bids[meal].remove(listing)
        
        return trade
    
    def buy_from_ipo(self, user, meal, qty):
        """Buy shares directly from IPO"""
        if self.ipo_start_time is None:
            return False, "IPO not started"
        
        if meal not in ALL_MEALS:
            return False, "Invalid meal"
        
        ipo_price = self.get_current_ipo_price()
        cost = ipo_price * qty
        
        if qty > self.house_supply[meal]:
            return False, "Insufficient supply"
        
        if self.balances[user] < cost:
            return False, "Insufficient funds"
        
        self.house_supply[meal] -= qty
        self.execute_trade(user, "IPO_HOUSE", meal, ipo_price, qty)
        
        return True, f"Bought {qty} shares of {meal} at ${ipo_price:.2f}"
    
    def place_buy_order(self, user, meal, price, qty, snap_buy=False):
        """Place a buy order (bid) on the secondary market"""
        if meal not in ALL_MEALS:
            return False, "Invalid meal", []
        
        trades_executed = []
        remaining_qty = qty
        
        # Try to match with existing asks
        while remaining_qty > 0:
            sorted_asks = sorted(self.asks[meal], key=lambda x: x['price'])
            if not sorted_asks:
                break
            
            best_ask = sorted_asks[0]
            
            # Only match if ask price is at or below our bid price
            if best_ask['price'] > price:
                break
            
            # Execute trade
            trade_qty = min(remaining_qty, best_ask['qty'])
            
            if self.balances[user] < (best_ask['price'] * trade_qty):
                break  # Insufficient funds
            
            trade = self.execute_trade(user, best_ask['seller'], meal, 
                                      best_ask['price'], trade_qty, best_ask)
            trades_executed.append(trade)
            remaining_qty -= trade_qty
        
        # If there's remaining quantity and not a snap-buy, place bid
        if remaining_qty > 0 and not snap_buy:
            self.bids[meal].append({
                'user': user,
                'qty': remaining_qty,
                'price': price
            })
            return True, f"Executed {qty - remaining_qty} shares, {remaining_qty} shares added to order book", trades_executed
        
        if trades_executed:
            return True, f"Executed {qty - remaining_qty} shares", trades_executed
        
        return False, "No matching orders", []
    
    def place_sell_order(self, user, meal, price, qty, is_short=False):
        """Place a sell order (ask) on the secondary market"""
        if meal not in ALL_MEALS:
            return False, "Invalid meal", []
        
        # Check if user has shares (unless shorting)
        if not is_short and self.portfolios[user][meal] < qty:
            return False, "Insufficient shares", []
        
        trades_executed = []
        remaining_qty = qty
        
        # Try to match with existing bids
        while remaining_qty > 0:
            sorted_bids = sorted(self.bids[meal], key=lambda x: x['price'], reverse=True)
            if not sorted_bids:
                break
            
            best_bid = sorted_bids[0]
            
            # Only match if bid price is at or above our ask price
            if best_bid['price'] < price:
                break
            
            # Execute trade
            trade_qty = min(remaining_qty, best_bid['qty'])
            trade = self.execute_trade(best_bid['user'], user, meal, 
                                      best_bid['price'], trade_qty, best_bid)
            trades_executed.append(trade)
            remaining_qty -= trade_qty
        
        # If there's remaining quantity, place ask
        if remaining_qty > 0:
            self.asks[meal].append({
                'seller': user,
                'qty': remaining_qty,
                'price': price
            })
            return True, f"Executed {qty - remaining_qty} shares, {remaining_qty} shares added to order book", trades_executed
        
        if trades_executed:
            return True, f"Executed {qty - remaining_qty} shares", trades_executed
        
        return False, "No matching orders", []
    
    def get_trade_history(self, limit=20):
        """Get recent trade history"""
        return list(reversed(self.trade_history[-limit:]))