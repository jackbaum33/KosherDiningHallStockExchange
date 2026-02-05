# U-M Dining Exchange

A stock exchange simulation for dining hall meals, built with Flask and SQLAlchemy. **Now with full database support for multi-device sync!**

## Features

- **IPO Trading**: Buy meals directly from the house with declining prices
- **Secondary Market**: Place bids and asks to trade with other users
- **Portfolio Management**: Track your positions and balance
- **Real-time Updates**: Market data refreshes every 5 seconds and syncs across all devices
- **Short Selling**: Go short on meals you think are overvalued
- **Order Book**: Full market depth for each meal
- **Multi-Device Support**: All data persists in database, accessible from any device
- **Production Ready**: Works with SQLite (dev) or PostgreSQL (production)

## What's New: Database Integration

All market data is now stored in a real database:
- ✅ Users and balances persist across sessions
- ✅ Orders sync in real-time across all devices
- ✅ Complete trade history
- ✅ Portfolio positions saved
- ✅ Market state synchronized
- ✅ Production-ready with PostgreSQL support

## Project Structure

```
dining_exchange/
├── app.py              # Flask application and API routes
├── database.py         # SQLAlchemy database models
├── market_service.py   # Business logic layer (database-backed)
├── init_db.py          # Database initialization
├── config.py           # Configuration (meals, users, settings)
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── templates/
│   └── index.html      # Main web interface
└── static/
    └── app.js          # Frontend JavaScript
```

## Installation

1. Clone and navigate to the directory:
```bash
cd dining_exchange
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (optional for development):
```bash
cp .env.example .env
# Edit .env if you want to customize settings
```

5. Run the application:
```bash
python app.py
```

6. Open your browser to `http://localhost:5000`

### Database Setup

**Development (Default):**
- Uses SQLite automatically
- Database file: `dining_exchange.db`
- No additional setup needed

**Production (PostgreSQL):**
1. Install PostgreSQL
2. Create a database:
```bash
createdb dining_exchange
```
3. Set DATABASE_URL in `.env`:
```
DATABASE_URL=postgresql://username:password@localhost:5432/dining_exchange
```
4. Run the app (tables will be created automatically)

### Deploying to Cloud

**Heroku:**
```bash
heroku create your-app-name
heroku addons:create heroku-postgresql
git push heroku main
```

**Railway/Render:**
- Connect your GitHub repo
- Add PostgreSQL addon
- Set environment variables
- Deploy!

## Usage

### Login
Enter your username from the configured friends list (Josh, Jack, Levi, etc.)

### Start IPO
Click "Start IPO" to begin the declining price mechanism. Price starts at $200 and decreases by $1 every 3 seconds.

### Buy from IPO
Purchase meals directly from the house at the current IPO price while supply lasts.

### Secondary Market
- **Buy**: Place bids or snap-buy at the best available ask price
- **Sell**: Place asks or immediately match with the best bid
- **Short**: Sell meals you don't own (creates negative position)

### Portfolio
View all your current positions, including shorts (negative shares).

## API Endpoints

All endpoints return JSON and support real-time database operations:

- `POST /api/login` - Authenticate user
- `POST /api/logout` - End session
- `GET /api/current_user` - Get user balance and IPO price
- `GET /api/market_summary` - Get all meals with bid/ask data (live from DB)
- `POST /api/start_ipo` - Start the IPO countdown (persisted to DB)
- `POST /api/buy_ipo` - Buy from IPO (updates DB atomically)
- `POST /api/secondary_buy` - Place buy order (saved to order book)
- `POST /api/sell` - Place sell order (saved to order book)
- `GET /api/portfolio` - Get user's positions (from DB)
- `GET /api/trade_history` - Get recent trades (from DB)
- `GET /api/order_book/<meal>` - Get full order book for a meal (from DB)

## Configuration

Edit `config.py` to customize:
- User list
- Meal categories (Chicken, Beef, Misc)
- Initial balance
- House supply per meal
- IPO pricing parameters

## How It Works

### Market Mechanics
1. **IPO Phase**: Users buy from house supply at declining price
2. **Secondary Market**: Users trade with each other via limit orders
3. **Order Matching**: Bids match with asks when prices cross
4. **Portfolio Tracking**: All positions and balances tracked in real-time

### Trading Logic
- Buy orders match with lowest asks first
- Sell orders match with highest bids first
- Remaining quantity enters order book as limit order
- Shorting allowed (can sell without owning)

## Database Schema

**Tables:**
- `users` - User accounts and balances
- `meals` - Meal definitions and house supply
- `positions` - User holdings (shares per meal)
- `orders` - Active/filled/cancelled limit orders
- `trades` - Complete trade history
- `market_state` - IPO clock and market status

**Key Features:**
- Atomic transactions for trade execution
- Unique constraints on user-meal positions
- Foreign key relationships for data integrity
- Indexed queries for fast order matching

## Future Enhancements

- ✅ Database persistence (DONE!)
- ✅ Multi-device sync (DONE!)
- WebSocket support for instant updates (no page refresh)
- Charts and price history
- Options trading
- Market maker bots
- User authentication (passwords/OAuth)
- Mobile app
- Admin dashboard
- Export trade data to CSV
- Price alerts and notifications