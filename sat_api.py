import os
import satellite_ids
import requests
from dotenv import load_dotenv

class satellite_tracker:

    BASE_URL = "https://api.n2yo.com/rest/v1/satellite/"
    API_KEY = os.getenv("N2YO_API_KEY")

    def __init__(self):
        self.s = requests.Session()

    def get_tle(self,sat_id:int):
        """Retrieve the Two Line Elements (TLE) for a satellite identified by NORAD id."""
        #Request: https://api.n2yo.com/rest/v1/satellite/tle/25544&apiKey=API_KEY
        try:
            url = f"{self.BASE_URL}tle/{sat_id}/&apiKey={satellite_tracker.API_KEY}"
            response = self.s.get(url,timeout=20)
            return response.json()
    
        except requests.exceptions.RequestException as e:
            print(f"Error fetching TLE: {e}")
            return None
