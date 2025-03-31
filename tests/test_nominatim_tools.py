from src.tools.nominatim import define_rectangular_area

def test_define_rectangle_area_one_kilometer():
    # Given
    latitude = 48.844510
    longitude = 1.630324
    expected_southwest_lat = 48.83546628267043
    expected_southwest_lon = 1.6166739651707096
    expected_northeast_lat = 48.85355371732957
    expected_northeast_lon = 1.6439740348292906

    distance = 1

    # When
    actual_southwest_lat, actual_southwest_lon, actual_northeast_lat, actual_northeast_lon = define_rectangular_area(latitude, longitude, distance)

    # Then
    assert actual_southwest_lat == expected_southwest_lat
    assert actual_southwest_lon == expected_southwest_lon
    assert actual_northeast_lat == expected_northeast_lat
    assert actual_northeast_lon == expected_northeast_lon

def test_define_rectangle_area_ten_kilometers():
    # Given
    latitude = 48.720867
    longitude = 1.587213

    distance = 10

    expected_southwest_lat = 48.63042982670429
    expected_southwest_lon = 1.4510485115912939
    expected_northeast_lat = 48.81130417329571
    expected_northeast_lon = 1.723377488408706

    # When
    actual_southwest_lat, actual_southwest_lon, actual_northeast_lat, actual_northeast_lon = define_rectangular_area(latitude, longitude, distance)

    # Then
    assert actual_southwest_lat == expected_southwest_lat
    assert actual_southwest_lon == expected_southwest_lon
    assert actual_northeast_lat == expected_northeast_lat
    assert actual_northeast_lon == expected_northeast_lon

def test_define_rectangle_area_five_kilometers():
    # Given
    latitude = 42.9083745
    longitude = 0.1452684

    distance = 5

    expected_southwest_lat = 42.863155913352145
    expected_southwest_lon = 0.08394521221753556
    expected_northeast_lat = 42.95359308664786
    expected_northeast_lon = 0.20659158778246442

    # When
    actual_southwest_lat, actual_southwest_lon, actual_northeast_lat, actual_northeast_lon = define_rectangular_area(latitude, longitude, distance)

    # Then
    assert actual_southwest_lat == expected_southwest_lat
    assert actual_southwest_lon == expected_southwest_lon
    assert actual_northeast_lat == expected_northeast_lat
    assert actual_northeast_lon == expected_northeast_lon
