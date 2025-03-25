def format_segment(segment: dict) -> str:
    """Format a segment for display.
    
    Args:
        segment: A dictionary containing segment information
    
    Returns:
        A formatted string containing segment details
    """
    return f"Id: {segment['id']} - Name: {segment['name']} - Distance: {segment['distance']} km - Average Gradient: {segment['avg_grade']}% - URL: https://www.strava.com/segments/{segment['id']}"

def format_ranking(entry: dict) -> str:
    """Format a ranking entry for display.
    
    Args:
        entry: A dictionary containing ranking information
    
    Returns:
        A formatted string containing ranking details
    """
    return f"TOP1: {entry['rank']} - Name: {entry['athlete_name']} - Time: {entry['moving_time']} - Distance: {entry['distance']} km - Average Gradient: {entry['average_grade']}% - URL: https://www.strava.com/segments/{entry['segment_id']}"
