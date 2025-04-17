import logging
from datetime import datetime
from typing import Dict

from mcp.server.fastmcp import FastMCP

from helpers import format_segment
from strava.api import make_strava_request
from strava.scraper import parse_strava_leaderboard

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

STRAVA_API_BASE = "https://www.strava.com/api/v3"
STRAVA_URL_BASE = "https://www.strava.com/"

async def get_nearby_segments(southwest_latitude: float, southwest_longitude: float, northeast_latitude: float, northeast_longitude: float) -> str:
    """Get nearby segments for a location.

    Args:
        southwest_latitude: Latitude of the southwest corner of the bounding box
        southwest_longitude: Longitude of the southwest corner of the bounding box
        northeast_latitude: Latitude of the northeast corner of the bounding box
        northeast_longitude: Longitude of the northeast corner of the bounding box

    Returns:
        A formatted string containing segment details
    """
    logger.debug(f"Fetching nearby segments for coordinates: southwest_latitude={southwest_latitude}, southwest_longitude={southwest_longitude}, northeast_latitude={northeast_latitude}, northeast_longitude={northeast_longitude}")
    url = f"{STRAVA_API_BASE}/segments/explore?bounds={southwest_latitude},{southwest_longitude},{northeast_latitude},{northeast_longitude}&activity_type=riding"
    data = await make_strava_request(url)
    logger.debug(f"Received response from Strava API: {data}")

    if not data or "segments" not in data:
        logger.warning("No data or segments found in Strava API response")
        return "Unable to fetch segments or no segments found."

    if not data["segments"]:
        logger.info("No segments found in the response")
        return "No segments found."

    segments = [format_segment(segment) for segment in data["segments"]]
    logger.debug(f"Formatted {len(segments)} segments")
    return "\n---\n".join(segments)

async def get_number_of_climb_attempts_on_the_year(segment_id: int) -> Dict[str, int]:
    """Get the number of climb attempts on the year for a given segment.

    Args:
        segment_id: The ID of the segment

    Returns:
        last_month_climbs_attempts: The number of climb attempts last month
        beginning_of_the_year_climbs_attempts: The number of climb attempts beginning of the year
    """
    last_month_climbs_attempts = 0
    beginning_of_the_year_climbs_attempts = 0

    result = await parse_strava_leaderboard(f"{STRAVA_URL_BASE}/segments/{segment_id}")

    # Get this year's leaderboard 
    if not result.empty:
        print("\nFetching this year's leaderboard...")   
        print("\nThis Year's Leaderboard Data:")
        print(result)

        now = datetime.now()
        
        last_month_climbs_attempts = len(result[result['date'].str.contains(now.strftime('%b'))])
        beginning_of_the_year_climbs_attempts = len(result[result['date'].str.contains(now.strftime('%Y'))])

        print(f"Number of climbs attempts last month: {last_month_climbs_attempts}")
        print(f"Number of climbs attempts beginning of the year: {beginning_of_the_year_climbs_attempts}")

    return {
        'last_month_climbs_attempts': last_month_climbs_attempts,
        'beginning_of_the_year_climbs_attempts': beginning_of_the_year_climbs_attempts
    }

def register_segment_tools(mcp: FastMCP):
    @mcp.tool()
    async def get_nearby_segments_tool(southwest_lat: float, southwest_lon: float, northeast_lat: float, northeast_lon: float) -> str:
        return await get_nearby_segments(southwest_lat, southwest_lon, northeast_lat, northeast_lon)

    @mcp.tool()
    async def get_number_of_climb_attempts_on_the_year_tool(segment_id: int) -> Dict[str, int]:
        return await get_number_of_climb_attempts_on_the_year(segment_id) 