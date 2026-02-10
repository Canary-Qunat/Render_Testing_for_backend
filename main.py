from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.database import get_db, init_db
from fastapi.templating import Jinja2Templates
from api.zerodha_client import Zerodha_Client
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Zerodha OAuth Backend")
    init_db()
    print("Backend ready at http://127.0.0.1:8000")
    yield   # app runs here
    print("Shutting down")


FRONTEND_URL = "http://localhost:3000"

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

templates = Jinja2Templates(directory="templates")
client = Zerodha_Client()


@app.get('/')
def read_root():
    return {
        "status": "running",
        "message": "Zerodha OAuth Backend API",
        "endpoints": {
            "login": "/kite-login",
            "callback": "/callback",
            "dashboard": "/dashboard",
            "docs": "/docs"
        }
    }

# Inject 'db' here so we can pass it to the client
@app.get('/dashboard')
def dashboard(request: Request, db: Session = Depends(get_db)):
    profile_data = client.get_profile(db)
    
    if not profile_data:
        # If no profile, we likely have no token, redirect to login
        return RedirectResponse(url="/kite-login")
    
    holdings = client.get_holdings(db)
    positions = client.get_positions(db)

    # calculate net positions
    net_positions = positions.get("net", []) if positions else []

    total_holdings_value = 0
    total_holdings_pnl = 0

    for holding in holdings:
        # Safety check for missing keys
        last_price = holding.get('last_price', 0) 
        qty = holding.get('quantity', 0)
        average_price = holding.get('average_price', 0)
        
        current_value = last_price * qty
        invested_value = average_price * qty # Fixed math: avg price * qty
        
        total_holdings_value += current_value
        total_holdings_pnl += (current_value - invested_value)

    total_positions_pnl = sum(pos.get('pnl', 0) for pos in net_positions)
    
    portfolio_summary = {
        'total_value': round(total_holdings_value, 2),
        'total_pnl': round(total_holdings_pnl + total_positions_pnl, 2),
        'holdings_pnl': round(total_holdings_pnl, 2),
        'positions_pnl': round(total_positions_pnl, 2),
        'holdings_count': len(holdings),
        'positions_count': len(net_positions)
    }
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "profile": profile_data,
        "holdings": holdings,
        "positions": net_positions,
        "summary": portfolio_summary
    })

@app.get("/kite-login")
def kite_login():
    try:
        login_url = client.get_login_url()
        return RedirectResponse(url=login_url) # Directly redirect user to Zerodha
    except Exception as e:
        print(f"Error generating login URL: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# API Endpoints for Frontend
@app.get("/api/profile")
def api_profile(db: Session = Depends(get_db)):
    """Get user profile as JSON"""
    profile_data = client.get_profile(db)
    if not profile_data:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return profile_data

@app.get("/api/holdings")
def api_holdings(db: Session = Depends(get_db)):
    """Get holdings as JSON"""
    holdings = client.get_holdings(db)
    return holdings

@app.get("/api/positions")
def api_positions(db: Session = Depends(get_db)):
    """Get positions as JSON"""
    positions = client.get_positions(db)
    return positions

@app.get("/api/summary")
def api_summary(db: Session = Depends(get_db)):
    """Get portfolio summary as JSON"""
    holdings = client.get_holdings(db)
    positions = client.get_positions(db)
    
    # Calculate net positions
    net_positions = positions.get("net", []) if positions else []
    
    total_holdings_value = 0
    total_holdings_pnl = 0
    
    for holding in holdings:
        last_price = holding.get('last_price', 0)
        qty = holding.get('quantity', 0)
        average_price = holding.get('average_price', 0)
        
        current_value = last_price * qty
        invested_value = average_price * qty
        
        total_holdings_value += current_value
        total_holdings_pnl += (current_value - invested_value)
    
    total_positions_pnl = sum(pos.get('pnl', 0) for pos in net_positions)
    
    return {
        'total_value': round(total_holdings_value, 2),
        'total_pnl': round(total_holdings_pnl + total_positions_pnl, 2),
        'holdings_pnl': round(total_holdings_pnl, 2),
        'positions_pnl': round(total_positions_pnl, 2),
        'holdings_count': len(holdings),
        'positions_count': len(net_positions)
    }

@app.get("/callback")
def kite_callback(request_token: str, status: str = "success", db: Session = Depends(get_db)):
    if status != "success":
        print(f"Login failed with status: {status}")
        return {"status": "failed", "message": "Login failed at Zerodha"}
    
    try:
        print(f"Received request_token: {request_token[:10]}...")
        
        # Pass DB session to client so it can save the token
        access_token = client.generate_access_token(request_token, db)
        
        if access_token:
            # Redirect to frontend dashboard instead of backend template
            return RedirectResponse(url="http://localhost:3000/dashboard.html")
        else:
            return {"status": "error", "message": "Could not generate access token"}

    except Exception as e:
        print(f"Callback error: {e}")
        return {"status": "error", "message": str(e)}