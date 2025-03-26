import os

import httpx

from dotenv import load_dotenv

load_dotenv()

STRAVA_ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")

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
