import logging
from math import cos, pi
from typing import Tuple

from mcp.server.fastmcp import FastMCP

from nominatim.api import make_nominatim_request

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

NOMINATIM_API_BASE = "https://nominatim.openstreetmap.org"

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

def define_number_kilometers_per_degree_longitude(latitude: float) -> float:
    """Define the number of kilometers per degree of longitude.

    Args:
        latitude: Latitude of the location

    Returns:
        kilometers_per_degree: The number of kilometers per degree of latitude
    """
    earth_circumference = 40075.017
    return earth_circumference * cos(latitude * pi / 180) / 360

def define_number_kilometers_per_degree_latitude() -> float:
    """Define the number of kilometers per degree of latitude.

    Returns:
        kilometers_per_degree: The number of kilometers per degree of latitude
    """
    return 110.574

def define_rectangular_area(latitude: float, longitude: float, distance: float = 10) -> Tuple[float, float, float, float]:
    """Define a rectangular area.
    
    Args:
        latitude: Latitude of the center of the area
        longitude: Longitude of the center of the area
        distance: Distance in kilometers from the center to the corners of the rectangle
    
    Returns:
        southwest_latitude: Latitude of the southwest corner of the bounding box
        southwest_longitude: Longitude of the southwest corner of the bounding box
        northeast_latitude: Latitude of the northeast corner of the bounding box
        northeast_longitude: Longitude of the northeast corner of the bounding box
    """
    logger.debug(f"Distance: {distance} kilometers")
    kilometers_per_degree_latitude = define_number_kilometers_per_degree_latitude()
    kilometers_per_degree_longitude = define_number_kilometers_per_degree_longitude(latitude)

    southwest_latitude = latitude - (distance / kilometers_per_degree_latitude)
    southwest_longitude = longitude - (distance / kilometers_per_degree_longitude)
    northeast_latitude = latitude + (distance / kilometers_per_degree_latitude)
    northeast_longitude = longitude + (distance / kilometers_per_degree_longitude)

    logger.debug(f"Southwest: {southwest_latitude}, {southwest_longitude}")
    logger.debug(f"Northeast: {northeast_latitude}, {northeast_longitude}")
    return (southwest_latitude, southwest_longitude, northeast_latitude, northeast_longitude)

def register_location_tools(mcp: FastMCP):
    @mcp.tool()
    async def get_latitude_and_longitude_tool(address: str) -> Tuple[float, float]:
        return await get_latitude_and_longitude(address)

    @mcp.tool()
    def define_rectangular_area_tool(latitude: float, longitude: float, distance: float = 10000) -> Tuple[float, float, float, float]:
        return define_rectangular_area(latitude, longitude, distance) 