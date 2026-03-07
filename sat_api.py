import os
from dotenv import load_dotenv

class satellite_tracker:

    BASE_URL = "https://api.n2yo.com/rest/v1/satellite/"
    API_KEY = os.getenv("N2YO_API_KEY")
    print(f"my api key: {API_KEY}")
    def __init__(self):
        pass