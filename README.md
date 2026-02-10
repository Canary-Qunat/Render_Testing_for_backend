# Frontend - Canary Trading System

A simple, vanilla HTML/CSS/JavaScript frontend for the Canary Trading System backend.

## Features

- 🔐 **Zerodha OAuth Login** - Secure authentication flow
- 📊 **Live Dashboard** - Real-time portfolio tracking
- 💰 **P&L Tracking** - Automatic profit/loss calculations
- 📈 **Holdings & Positions** - View all your investments
- 🎨 **Modern UI** - Gradient backgrounds with glassmorphism effects
- 📱 **Responsive Design** - Works on all screen sizes

## Structure

```
frontend/
├── index.html          # Login/landing page
├── dashboard.html      # Main dashboard
├── css/
│   └── styles.css     # All styling
└── js/
    ├── api.js         # API communication layer
    └── dashboard.js   # Dashboard logic
```

## How to Run

### 1. Start the Backend

First, make sure your FastAPI backend is running:

```bash
# From the project root directory
uvicorn main:app --reload
```

The backend will run on `http://localhost:8000`

### 2. Start the Frontend

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Start a simple HTTP server on port 3000:

```bash
# Using Python 3
python -m http.server 3000
```

The frontend will be available at `http://localhost:3000`

### 3. Access the Application

1. Open your browser and go to `http://localhost:3000`
2. Click "Login with Zerodha"
3. Complete the Zerodha authentication
4. You'll be redirected to the dashboard

## How It Works

### Login Flow

1. User clicks "Login with Zerodha" on `index.html`
2. Frontend redirects to backend `/kite-login` endpoint
3. Backend generates Zerodha login URL and redirects user
4. User authenticates with Zerodha
5. Zerodha redirects back to backend `/callback` endpoint
6. Backend saves access token to database
7. Backend redirects to frontend `dashboard.html`

### Dashboard Data Flow

1. Dashboard loads and calls API endpoints:
   - `GET /api/profile` - User profile data
   - `GET /api/holdings` - Holdings list
   - `GET /api/positions` - Positions list
   - `GET /api/summary` - Portfolio summary
2. JavaScript fetches data from backend
3. Data is formatted and displayed in tables
4. User can refresh to get latest data

## API Endpoints

The backend provides these JSON endpoints for the frontend:

- **GET /api/profile** - Returns user profile information
- **GET /api/holdings** - Returns list of holdings
- **GET /api/positions** - Returns list of positions
- **GET /api/summary** - Returns portfolio summary with P&L

## Technologies Used

- **HTML5** - Structure
- **CSS3** - Styling with gradients and glassmorphism
- **Vanilla JavaScript** - Logic and API calls
- **Fetch API** - HTTP requests to backend

## Browser Compatibility

Works on all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari

## Troubleshooting

### CORS Errors

If you see CORS errors in the browser console, make sure:
1. Backend is running on port 8000
2. Frontend is running on port 3000
3. CORS is configured in `main.py` to allow `http://localhost:3000`

### Data Not Loading

If dashboard shows "Failed to load data":
1. Check that backend is running
2. Verify you're logged in (access token in database)
3. Check browser console for errors
4. Try logging in again

### Port Already in Use

If port 3000 is already in use, you can use a different port:

```bash
python -m http.server 3001
```

Then update the `FRONTEND_URL` in `main.py` and `API_BASE_URL` in frontend JavaScript files.
