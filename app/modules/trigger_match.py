import os 
import requests
from dotenv import load_dotenv

load_dotenv()

class TriggerMatch():
    # url = f"https://onction-matching-engine-762140739532.europe-west2.run.app/v1/match"
    url = f"http://144.91.85.115:8000/v1/match"
    api_key = os.getenv('API_KEY')
    
    def __init__(self):
        pass

    def create_header(self):
        headers = {
            "accept": "application/json",
            "X-API-Key": f"{self.api_key}".strip(),
            "Content-Type": "application/json",
        } 
        return headers
    
    def trigger_matching_engine(self, params, payload):
        trade = requests.post(
            self.url,
            headers=self.create_header(),
            params=params, 
            json = payload)
        return trade.json() 
