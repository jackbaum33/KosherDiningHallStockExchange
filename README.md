# U-M Dining Exchange

A stock exchange simulation for dining hall meals, built with Flask.

## Features

- **IPO Trading**: Buy meals directly from the house with declining prices
- **Secondary Market**: Place bids and asks to trade with other users
- **Portfolio Management**: Track your positions and balance
- **Real-time Updates**: Market data refreshes every 5 seconds
- **Short Selling**: Go short on meals you think are overvalued
- **Order Book**: Full market depth for each meal

## Project Structure

```
dining_exchange/
├── app.py              # Flask application and API routes
├── models.py           # Market and trading logic
├── config.py           # Configuration (meals, users, settings)
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Main web interface
└── static/
    └── app.js          # Frontend JavaScript
```

## Installation
(virtual environment required)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser to `http://localhost:5000`

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

- `POST /api/login` - Authenticate user
- `POST /api/logout` - End session
- `GET /api/current_user` - Get user balance and IPO price
- `GET /api/market_summary` - Get all meals with bid/ask data
- `POST /api/start_ipo` - Start the IPO countdown
- `POST /api/buy_ipo` - Buy from IPO
- `POST /api/secondary_buy` - Place buy order
- `POST /api/sell` - Place sell order
- `GET /api/portfolio` - Get user's positions
- `GET /api/trade_history` - Get recent trades
- `GET /api/order_book/<meal>` - Get full order book for a meal

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

## Future Enhancements

- WebSocket support for real-time updates
- Charts and price history
- Options trading
- Market maker bots
- Database persistence
- User authentication
- Mobile app