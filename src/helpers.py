def format_segment(segment: dict) -> str:
    """Format a segment for display.
    
    Args:
        segment: A dictionary containing segment information
    
    Returns:
        A formatted string containing segment details
    """
    return f"Id: {segment['id']} - Name: {segment['name']} - Distance: {segment['distance']} km - Average Gradient: {segment['avg_grade']}% - URL: https://www.strava.com/segments/{segment['id']}"