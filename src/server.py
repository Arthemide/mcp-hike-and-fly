import logging

from mcp.server.fastmcp import FastMCP

from prompts.location import register_location_prompts
from prompts.segments import register_segment_prompts
from tools.nominatim import register_location_tools
from tools.strava import register_segment_tools

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("strava")

# Register tools and prompts
register_location_tools(mcp)
register_segment_tools(mcp)

register_location_prompts(mcp)
register_segment_prompts(mcp)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')