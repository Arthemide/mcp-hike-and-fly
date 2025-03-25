import pytest

from server import get_number_of_climb_attempts_on_the_year


@pytest.mark.asyncio
@pytest.mark.parametrize("segment_id, expected_last_month, expected_beginning_of_year", [
    (7037936, 5, 6),
    (12349239, 8, 25),
])
async def test_get_number_of_climb_attempts_on_the_year(segment_id, expected_last_month, expected_beginning_of_year):
    # When
    result = await get_number_of_climb_attempts_on_the_year(segment_id)

    # Then
    assert result['last_month_climbs_attempts'] == expected_last_month
    assert result['beginning_of_the_year_climbs_attempts'] == expected_beginning_of_year
