import mcp.types as types
from mcp.server.fastmcp import FastMCP

def register_location_prompts(mcp: FastMCP):
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