import logging
from datetime import datetime
from typing import Tuple

import mcp.types as types
from mcp.server.fastmcp import FastMCP

from helpers import format_ranking, format_segment
from nominatim_api import make_nominatim_request
from strava_api import make_strava_request
from strava_bs4 import parse_strava_leaderboard

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

STRAVA_API_BASE = "https://www.strava.com/api/v3"
STRAVA_URL_BASE = "https://www.strava.com/"
NOMINATIM_API_BASE = "https://nominatim.openstreetmap.org"

# Initialize FastMCP server
mcp = FastMCP("strava")

# Register the prompts
@mcp.prompt("find-segments-by-address")
async def find_segments_by_address(address: str) -> types.GetPromptResult:
    return types.GetPromptResult(
        messages=[
            types.PromptMessage(
                role="system",
                content=types.TextContent(
                    type="text",
                    text="You are a helpful assistant that finds Strava segments near addresses. You will use the following tools in sequence:\n"
                    "1. get_latitude_and_longitude to get coordinates\n"
                    "2. define_rectangular_area to create a search area\n"
                    "3. get_nearby_segments to find segments"
                )
            ),
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Find all Strava segments near this address: {address}"
                )
            ),
            types.PromptMessage(
                role="assistant",
                content=types.TextContent(
                    type="text",
                    text="I'll help you find Strava segments near that address. Let me break this down into steps:\n"
                    "1. First, I'll get the coordinates for the address using get_latitude_and_longitude\n"
                    "2. Then, I'll define a rectangular area around those coordinates using define_rectangular_area with a 10km radius\n"
                    "3. Finally, I'll find all segments in that area using get_nearby_segments\n\n"
                    "Let's start by getting the coordinates for the address."
                )
            ),
            types.PromptMessage(
                role="tool",
                content=types.TextContent(
                    type="text",
                    text="get_latitude_and_longitude"
                )
            ),
            types.PromptMessage(
                role="assistant",
                content=types.TextContent(
                    type="text",
                    text="Now that we have the coordinates, let's define a search area around them."
                )
            ),
            types.PromptMessage(
                role="tool",
                content=types.TextContent(
                    type="text",
                    text="define_rectangular_area"
                )
            ),
            types.PromptMessage(
                role="assistant",
                content=types.TextContent(
                    type="text",
                    text="Finally, let's find all segments in this area."
                )
            ),
            types.PromptMessage(
                role="tool",
                content=types.TextContent(
                    type="text",
                    text="get_nearby_segments"
                )
            )
        ]
    )

# Register the tools
@mcp.tool()
async def get_latitude_and_longitude(address: str) -> Tuple[float, float]:
    """Get the latitude and longitude of an address.

    Args:
        address: The address to get the latitude and longitude of

    Returns:
        latitude: The latitude of the address
        longitude: The longitude of the address
    """
    logger.debug(f"Fetching latitude and longitude for address: {address}")
    data = await make_nominatim_request(f"{NOMINATIM_API_BASE}/search?q={address}&format=json")
    logger.debug(f"Received response from Nominatim API: {data}")

    if not data or "lat" not in data[0] or "lon" not in data[0]:
        logger.warning("No data or latitude and longitude found in Nominatim API response")
        raise ValueError(f"Unable to fetch latitude and longitude for address: {address}")

    latitude = float(data[0]["lat"])
    longitude = float(data[0]["lon"])
    logger.debug(f"Latitude: {latitude}, Longitude: {longitude}")
    return (latitude, longitude)

@mcp.tool()
def define_rectangular_area(lat: float, lon: float, distance: float = 10000) -> Tuple[float, float, float, float]:
    """Define a rectangular area.
    
    Args:
        lat: Latitude of the center of the area
        lon: Longitude of the center of the area
        distance: Distance in meters from the center to the corners of the rectangle
    
    Returns:
        southwest_lat: Latitude of the southwest corner of the bounding box
        southwest_lon: Longitude of the southwest corner of the bounding box
        northeast_lat: Latitude of the northeast corner of the bounding box
        northeast_lon: Longitude of the northeast corner of the bounding box
    """
    # 111000 is the approximate number of meters per degree of latitude
    meters_per_degree_lat = 111000
    meters_per_degree_lon = 111000 * abs(lat)
    logger.debug(f"Distance: {distance} meters")
    southwest_lat = lat - (distance / meters_per_degree_lat)
    northeast_lat = lat + (distance / meters_per_degree_lat)
    southwest_lon = lon - (distance / meters_per_degree_lon)
    northeast_lon = lon + (distance / meters_per_degree_lon)
    logger.debug(f"Southwest: {southwest_lat}, {southwest_lon}")
    logger.debug(f"Northeast: {northeast_lat}, {northeast_lon}")
    return (southwest_lat, southwest_lon, northeast_lat, northeast_lon)

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
async def get_number_of_climb_attempts_on_the_year(segment_id: int) -> Tuple[int, int]:
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

@mcp.prompt("find-segments-by-coordinates")
async def find_segments_by_coordinates(
    southwest_lat: str,
    southwest_lon: str,
    northeast_lat: str,
    northeast_lon: str
) -> types.GetPromptResult:
    return types.GetPromptResult(
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Find all Strava segments within these coordinates:\n"
                    f"Southwest: {southwest_lat}, {southwest_lon}\n"
                    f"Northeast: {northeast_lat}, {northeast_lon}"
                )
            )
        ]
    )

@mcp.prompt("get-segment-ranking")
async def get_segment_ranking_prompt(segment_id: str) -> types.GetPromptResult:
    return types.GetPromptResult(
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Get the ranking information for Strava segment with ID: {segment_id}"
                )
            )
        ]
    )

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')