import mcp.types as types
from mcp.server.fastmcp import FastMCP


def register_segment_prompts(mcp: FastMCP):
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
