
from kiteconnect import KiteConnect
from sqlalchemy.orm import Session
# Import functions from your database file
from database.database import save_token_to_db, get_latest_token
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
secret_key = os.getenv('SECRET_KEY')
token_path = 'access_token.txt'

class Zerodha_Client():

    def __init__(self):
        self.api_key = api_key
        self.secret_key = secret_key
        self.kite = KiteConnect(api_key=self.api_key)

    def get_login_url(self):
        return self.kite.login_url()
    
    # Updated to take DB session and use DB functions
    def generate_access_token(self, request_token, db: Session):
        data = self.kite.generate_session(request_token=request_token, api_secret=self.secret_key)
        access_token = data["access_token"]
        
        # Save to DB instead of file
        save_token_to_db(access_token=access_token, db=db)
        
        # Set it immediately for current instance
        self.kite.set_access_token(access_token)
        return access_token
    
    # Updated to load from DB
    def setup_kite(self, db: Session):
        access_token = get_latest_token(db)

        if not access_token:
            print("Access token not found in DB")
            return False
        else:
            self.kite.set_access_token(access_token=access_token)
            return True
        
    # All service methods now accept 'db' to ensure connection is live
    def get_profile(self, db: Session):
        if self.setup_kite(db):
            try:
                return self.kite.profile()
            except Exception as e:
                print(f"Error fetching profile: {e}")
                return None
        return None
    
    def get_holdings(self, db: Session):
        if self.setup_kite(db):
            try:
                return self.kite.holdings()
            except Exception as e:
                print(f"Error fetching holdings: {e}")
                return []
        return []
    
    def get_positions(self, db: Session):
        if self.setup_kite(db):
            try:
                return self.kite.positions()
            except Exception as e:
                print(f"Error fetching positions: {e}")
                return {}
        return {}