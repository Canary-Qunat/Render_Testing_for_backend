# Canary Tracking System

A Python-based trading companion for tracking live positions, analyzing multi-timeframe trends, and auditing trade performance. This Flask web application integrates with Zerodha Kite Connect API to provide real-time portfolio monitoring and analytics.

## Prerequisites

- Python 3.7 or higher
- Zerodha Kite Connect API credentials (API Key and Secret Key) (all testing is done by using this for few i have personal credential but after some day's i will purchase for this project only so that every one use that)
- Active Zerodha trading account (that's only plus one)

  ## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Canary-Tracking-System.git
   cd Canary-Tracking-System
   ```

2. **Install dependencies**
   ```bash/powershell/terminal
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory with your Zerodha API credentials:
   ```
   API_KEY=your_api_key_here
   SECRET_KEY=your_secret_key_here
   ```

   ## Configuration

The application uses environment variables for configuration. Make sure to obtain your API credentials from the [Zerodha Kite Connect Developer Console](https://developers.kite.trade/).

### Getting Zerodha API Credentials

1. Log in to [Kite Connect](https://developers.kite.trade/)
2. Create a new app
3. Note down your API Key and Secret Key
4. Set the redirect URL to `http://localhost:5000/callback` (or your deployment URL)

## Usage

1. **Start the Flask application**
   ```bash
   python main.py
   ```

2. **Access the application**
   
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

3. **Authentication Flow**
   - On first visit, you'll be redirected to Zerodha login
   - Log in with your Zerodha credentials
   - Authorize the application
   - You'll be redirected back to your dashboard

## Project Structure

```
Canary-Tracking-System/
├── api/
│   ├── config_api.py          # API configuration and environment variables
│   └── zerodha_client.py      # Zerodha Kite Connect client wrapper
├── templates/
│   ├── base.html              # Base template with common layout
│   ├── dashboard.html         # Main dashboard view
│   └── profile.html           # User profile page
├── main.py                    # Flask application entry point
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
├── LICENSE                   # Project license
└── README.md                 # This file
```

## API Endpoints

- **`/` or `/dashboard`**: Main dashboard displaying holdings, positions, and portfolio summary
- **`/login`**: Initiates Zerodha OAuth login flow
- **`/callback`**: OAuth callback endpoint for handling authentication
- **`/profile`**: User profile page displaying account information

## Features Breakdown

### Dashboard
- **Holdings Overview**: View all your long-term holdings with current prices
- **Positions Tracking**: Monitor intraday and overnight positions
- **P&L Calculation**: Automatic profit/loss calculation for holdings and positions
- **Portfolio Summary**: Aggregated view of total portfolio value and performance

### Profile
- **User Information**: Display account details and user profile
- **Account Status**: View account type and trading status

## Dependencies

- **kiteconnect**: Official Zerodha Kite Connect Python client
- **flask**: Web framework for building the application
- **python-dotenv**: Environment variable management
- **pandas**: Data manipulation and analysis
- **requests**: HTTP library for API calls
- **gunicorn**: WSGI HTTP server for production deployment

## Security Notes

- Access tokens are stored locally in `access_token.txt`
- Never share your API credentials or access tokens
- The `.env` file containing sensitive credentials is excluded from version control
- For production deployment, consider using a database to store access tokens securely

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Support

For issues and questions:
- Open an issue on GitHub
