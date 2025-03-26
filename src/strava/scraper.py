
import aiohttp
import pandas as pd
from bs4 import BeautifulSoup

from strava.utils import COOKIES, HEADERS, PARAMS


async def parse_strava_leaderboard(url) -> pd.DataFrame:
    try:
        # First, get the initial page to get any necessary cookies
        async with aiohttp.ClientSession() as session:
            
            # Modify URL for this year's data if requested
            url = f"{url}/leaderboard?date_range=this_year&filter=current_year&partial=true"
            
            async with session.get(url, params=PARAMS, cookies=COOKIES, headers=HEADERS) as response:
                response.raise_for_status()
                
                # Parse the HTML
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')


                # Get column names from headers
                headers = soup.find_all('th')
                column_names = [header.get_text(strip=True) for header in headers]
                
                # Extract leaderboard data
                leaderboard_data = []
                leaderboard_rows = soup.find_all('tr', class_='')
                
                for row in leaderboard_rows:
                    cols = row.find_all('td')
                    if len(cols) >= len(column_names):  # Ensure we have all columns
                        athlete_link = cols[1].find('a')
                        effort_link = cols[2].find('a')
                        
                        # Extract data with proper error handling
                        entry = {
                            'rank': cols[0].get_text(strip=True),
                            'athlete_name': athlete_link.get_text(strip=True) if athlete_link else '',
                            'athlete_id': athlete_link['href'].split('/')[-1] if athlete_link else '',
                            'date': effort_link.get_text(strip=True) if effort_link else '',
                            'effort_id': effort_link['href'].split('/')[-1] if effort_link else '',
                            'speed': cols[3].get_text(strip=True).replace(' km/h', ''),
                            'heart_rate': cols[4].get_text(strip=True).replace(' bpm', ''),
                            'power': cols[5].get_text(strip=True).replace(' W', '').replace('-', '')
                        }
                        
                        # Add VAM if it exists in the columns
                        if 'VAM' in column_names:
                            vam_index = column_names.index('VAM')
                            entry['VAM'] = cols[vam_index].get_text(strip=True)
                            
                        # Add time (it's always the last column)
                        time_index = len(column_names) - 1
                        entry['time'] = cols[time_index].get_text(strip=True)
                            
                        leaderboard_data.append(entry)
            
        # Create DataFrame
        df = pd.DataFrame(leaderboard_data)
        
        # Convert numeric columns
        if not df.empty:
            numeric_columns = ['rank', 'speed', 'heart_rate', 'power']
            if 'VAM' in df.columns:
                numeric_columns.append('VAM')
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        return df
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None
