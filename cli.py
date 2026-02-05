"""
Standalone CLI version of the dining exchange
For backwards compatibility with the original interface
"""

from models import Market
from config import FRIENDS, CHICKEN_INDEX, BEEF_INDEX, MISC_INDEX, ALL_MEALS

def select_meal_from_indices():
    """Interactive menu to select a meal"""
    print("\n[1] Chicken | [2] Beef | [3] Misc")
    idx = input("Select Index: ")
    
    if idx == "1":
        meal_list = CHICKEN_INDEX
    elif idx == "2":
        meal_list = BEEF_INDEX
    elif idx == "3":
        meal_list = MISC_INDEX
    else:
        return None
    
    for i, meal in enumerate(meal_list, 1):
        print(f"{i}. {meal}")
    
    try:
        m_idx = int(input("Meal #: ")) - 1
        return meal_list[m_idx]
    except:
        return None

def show_market_summary(market):
    """Display market overview"""
    summary = market.get_market_summary()
    ipo_price = summary['ipo_price']
    
    print("\n" + "="*85)
    print(f"   U-M DINING EXCHANGE | IPO PRICE: ${ipo_price:.2f}")
    print("="*85)
    print(f"{'Meal':<30} | {'IPO':<6} | {'Best Ask':<10} | {'Best Bid'}")
    print("-" * 85)
    
    for meal_data in summary['meals']:
        meal = meal_data['name']
        supply = meal_data['house_supply'] if meal_data['house_supply'] > 0 else "-"
        b_ask = meal_data['best_ask']
        b_bid = meal_data['best_bid']
        
        a_str = f"${b_ask:.2f}" if b_ask else "N/A"
        b_str = f"${b_bid:.2f}" if b_bid else "N/A"
        
        print(f"{meal[:29]:<30} | {str(supply):<6} | {a_str:<10} | {b_str}")

def secondary_buy(market, user):
    """Place a buy order on secondary market"""
    meal = select_meal_from_indices()
    if not meal:
        return
    
    best_ask = market.get_best_ask(meal)
    
    if best_ask:
        print(f"\nCheapest {meal} available: ${best_ask['price']:.2f}")
        confirm = input(f"Snap-buy at ${best_ask['price']:.2f}? (y/n): ").lower()
        
        if confirm == 'y':
            try:
                qty = int(input("Quantity: "))
                success, message, trades = market.place_buy_order(
                    user, meal, best_ask['price'], qty, snap_buy=True
                )
                print(f"\n{message}")
                return
            except:
                print("Invalid input.")
                return
    
    print(f"\nNo snap-buys available. Place a custom bid.")
    try:
        price = float(input(f"Your Max Bid Price: $"))
        qty = int(input("Quantity: "))
        success, message, trades = market.place_buy_order(user, meal, price, qty)
        print(f"\n{message}")
    except:
        print("Invalid input.")

def secondary_sell(market, user, is_short=False):
    """Place a sell order on secondary market"""
    meal = select_meal_from_indices()
    if not meal:
        return
    
    if not is_short and market.portfolios[user][meal] <= 0:
        print("No shares to sell.")
        return
    
    try:
        qty = int(input(f"Qty to {'Short' if is_short else 'Sell'}: "))
        price = float(input("Min Ask Price: $"))
        success, message, trades = market.place_sell_order(user, meal, price, qty, is_short)
        print(f"\n{message}")
    except:
        print("Invalid input.")

def main():
    """Main CLI loop"""
    market = Market()
    current_user = ""
    
    while True:
        if not current_user:
            user = input("\nLogin: ")
            if user in FRIENDS:
                current_user = user
            else:
                continue
        
        ipo_price = market.get_current_ipo_price()
        balance = market.get_balance(current_user)
        
        print(f"\n[{current_user}] Cash: ${balance:.2f} | IPO Price: ${ipo_price:.2f}")
        print("1. Market | 2. BUY IPO | 3. START IPO | 4. SECONDARY BUY | 5. SELL | 6. SHORT | 7. Portfolio | 8. History | 9. Switch User | 0. Quit")
        choice = input("Select: ")
        
        if choice == "1":
            show_market_summary(market)
        
        elif choice == "2":
            if market.ipo_start_time:
                meal = select_meal_from_indices()
                if meal:
                    try:
                        qty = int(input(f"Buying {meal} at ${ipo_price:.2f}. Qty: "))
                        success, message = market.buy_from_ipo(current_user, meal, qty)
                        print(f"\n{message}")
                    except:
                        print("Invalid entry.")
            else:
                print("IPO not started.")
        
        elif choice == "3":
            market.start_ipo()
            print("IPO CLOCK STARTED")
        
        elif choice == "4":
            secondary_buy(market, current_user)
        
        elif choice == "5":
            secondary_sell(market, current_user, is_short=False)
        
        elif choice == "6":
            secondary_sell(market, current_user, is_short=True)
        
        elif choice == "7":
            portfolio = market.get_portfolio(current_user)
            if not portfolio:
                print("No positions")
            else:
                for meal, data in portfolio.items():
                    short_label = "(SHORT)" if data['is_short'] else ""
                    print(f"{meal}: {data['shares']} shares {short_label}")
        
        elif choice == "8":
            trades = market.get_trade_history(limit=10)
            for trade in trades:
                print(f"{trade['buyer']} <- {trade['seller']} | "
                      f"{trade['qty']} {trade['meal']} @ ${trade['price']:.2f}")
        
        elif choice == "9":
            current_user = ""
        
        elif choice == "0":
            print("Goodbye!")
            break

if __name__ == '__main__':
    main()