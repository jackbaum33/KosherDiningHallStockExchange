from database import db, User, Meal, MarketState
from config import FRIENDS, CHICKEN_INDEX, BEEF_INDEX, MISC_INDEX, INITIAL_BALANCE, INITIAL_HOUSE_SUPPLY

def init_database():
    """Initialize database with tables and seed data"""
    
    # Create all tables
    db.create_all()
    
    # Check if already initialized
    if User.query.first() is not None:
        return  # Database already has data
    
    print("Initializing database...")
    
    # Create users
    for friend in FRIENDS:
        user = User(username=friend, balance=INITIAL_BALANCE)
        db.session.add(user)
    
    # Create meals
    for meal_name in CHICKEN_INDEX:
        meal = Meal(name=meal_name, category='Chicken', house_supply=INITIAL_HOUSE_SUPPLY)
        db.session.add(meal)
    
    for meal_name in BEEF_INDEX:
        meal = Meal(name=meal_name, category='Beef', house_supply=INITIAL_HOUSE_SUPPLY)
        db.session.add(meal)
    
    for meal_name in MISC_INDEX:
        meal = Meal(name=meal_name, category='Misc', house_supply=INITIAL_HOUSE_SUPPLY)
        db.session.add(meal)
    
    # Create market state
    market_state = MarketState(ipo_active=False)
    db.session.add(market_state)
    
    # Commit all changes
    db.session.commit()
    
    print(f"Database initialized with {len(FRIENDS)} users and {len(CHICKEN_INDEX) + len(BEEF_INDEX) + len(MISC_INDEX)} meals")