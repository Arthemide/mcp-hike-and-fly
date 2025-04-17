import pytest

from src.tools.strava import (
    get_nearby_segments,
    get_number_of_climb_attempts_on_the_year,
)


@pytest.mark.parametrize("segment_id, expected_last_month, expected_beginning_of_year", [
    (7037936, 6, 7),
    (12349239, 8, 25),
])
async def test_get_number_of_climb_attempts_on_the_year(segment_id, expected_last_month, expected_beginning_of_year):
    # When
    result = await get_number_of_climb_attempts_on_the_year(segment_id)

    # Then
    assert result['last_month_climbs_attempts'] == expected_last_month
    assert result['beginning_of_the_year_climbs_attempts'] == expected_beginning_of_year

@pytest.mark.asyncio
async def test_get_nearby_segments_returns_no_segments():
    # Given
    expected_southwest_lat = 48.85355371732957
    expected_southwest_lon = 1.6166739651707096
    expected_northeast_lat = 48.85355371732957
    expected_northeast_lon = 1.6439740348292906

    expected_result = "No segments found."

    # When
    actual_result = await get_nearby_segments(expected_southwest_lat, expected_southwest_lon, expected_northeast_lat, expected_northeast_lon)

    # Then
    assert actual_result == expected_result

@pytest.mark.asyncio
async def test_get_nearby_segments_returns_segments():
    # Given
    # 45.052859, 5.992628
    # 45.101033, 6.085844
    expected_southwest_lat = 45.052859
    expected_southwest_lon = 5.992628
    expected_northeast_lat = 45.101033
    expected_northeast_lon = 6.085844

    expected_result = "Id: 652851 - Name: Alpe d'Huez - Distance: 12024.9 km - Average Gradient: 8.8% - URL: https://www.strava.com/segments/652851\n---\nId: 24847998 - Name: La Garde -> Huez Village - Distance: 6259.4 km - Average Gradient: 7.7% - URL: https://www.strava.com/segments/24847998\n---\nId: 21476037 - Name: Deux Mille: Bend 21 to 19 - Distance: 832.3 km - Average Gradient: 10.5% - URL: https://www.strava.com/segments/21476037\n---\nId: 17407860 - Name:  2e km - Distance: 1014.2 km - Average Gradient: 10.3% - URL: https://www.strava.com/segments/17407860\n---\nId: 20977032 - Name: Finish Lepape La Marmotte - Grand Fondo 2019 - Distance: 2016.0 km - Average Gradient: 8.8% - URL: https://www.strava.com/segments/20977032\n---\nId: 10042913 - Name: Turn off to Huez to tourist Finish - Distance: 3022.6 km - Average Gradient: 8.0% - URL: https://www.strava.com/segments/10042913\n---\nId: 21476085 - Name: Deux Mille: Bend 13 to 8 - Distance: 2644.9 km - Average Gradient: 8.4% - URL: https://www.strava.com/segments/21476085\n---\nId: 21476123 - Name: Deux Mille: Bend 6 to 3 - Distance: 1789.8 km - Average Gradient: 7.9% - URL: https://www.strava.com/segments/21476123\n---\nId: 21476104 - Name: Deux Mille: Bend 8 to 6 - Distance: 1632.7 km - Average Gradient: 8.0% - URL: https://www.strava.com/segments/21476104\n---\nId: 17671529 - Name: Run-in to Bourg roundabout - Distance: 986.6 km - Average Gradient: -1.8% - URL: https://www.strava.com/segments/17671529"

    # When
    actual_result = await get_nearby_segments(expected_southwest_lat, expected_southwest_lon, expected_northeast_lat, expected_northeast_lon)

    # Then
    assert actual_result == expected_result
