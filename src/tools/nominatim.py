import logging
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

def register_location_tools(mcp: FastMCP):
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