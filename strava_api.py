import os

import httpx

# from stravalib import Client
# from stravalib.util.limiter import DefaultRateLimiter
from dotenv import load_dotenv

load_dotenv()

STRAVA_ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")
STRAVA_TOKEN_EXPIRES = int(os.getenv("STRAVA_TOKEN_EXPIRES"))

# client = Client(access_token=STRAVA_ACCESS_TOKEN, refresh_token=STRAVA_REFRESH_TOKEN, token_expires=STRAVA_TOKEN_EXPIRES, rate_limiter=DefaultRateLimiter(priority='medium'))

# segments = client.get_segment_efforts(1234567890)

async def make_strava_request(url: str) -> dict:
    """Make a request to the Strava API with proper error handling."""

    headers = {
        "Authorization": f"Bearer {STRAVA_ACCESS_TOKEN}"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error making Strava request: {e}")
            return None
