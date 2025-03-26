import logging
from datetime import datetime
from typing import Dict, Tuple

from mcp.server.fastmcp import FastMCP

from helpers import format_ranking, format_segment
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

def register_segment_tools(mcp: FastMCP):
    @mcp.tool()
    async def get_nearby_segments(southwest_lat: float, southwest_lon: float, northeast_lat: float, northeast_lon: float) -> str:
        """Get nearby segments for a location.

        Args:
            southwest_lat: Latitude of the southwest corner of the bounding box
            southwest_lon: Longitude of the southwest corner of the bounding box
            northeast_lat: Latitude of the northeast corner of the bounding box
            northeast_lon: Longitude of the northeast corner of the bounding box

        Returns:
            A formatted string containing segment details
        """
        logger.debug(f"Fetching nearby segments for coordinates: lat={southwest_lat}, lon={southwest_lon}, lat={northeast_lat}, lon={northeast_lon}")
        url = f"{STRAVA_API_BASE}/segments/explore?bounds={southwest_lat},{southwest_lon},{northeast_lat},{northeast_lon}&activity_type=running&max_cat=0"
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

    @mcp.tool()
    async def get_segment_ranking(segment_id: int) -> str:
        """Get the ranking of a segment.

        Args:
            segment_id: The ID of the segment

        Returns:
            A formatted string containing segment details
        """
        logger.debug(f"Fetching segment ranking for segment ID: {segment_id}")
        url = f"{STRAVA_API_BASE}/segments/{segment_id}"
        data = await make_strava_request(url)
        print(data)
        logger.debug(f"Received response from Strava API: {data}")

        if not data or "entries" not in data:
            logger.warning("No data or entries found in Strava API response")
            return "Unable to fetch segment ranking or no entries found."

        entries = [format_ranking(entry) for entry in data["entries"]]
        logger.debug(f"Formatted {len(entries)} entries")
        return "\n---\n".join(entries)

    @mcp.tool()
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