
import httpx


async def make_nominatim_request(url: str) -> dict:
    """Make a request to the Nominatim API with proper error handling."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

