import pytest
from main import get_weather

def test_get_weather(mocker):
    mock_get = mocker.patch("main.requests.get")

    # Mock the response object
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'temp': 20, 'condition': 'sunny'}

    result = get_weather("Dubai")

    assert result == {'temp': 20, 'condition': 'sunny'}
    mock_get.assert_called_once_with("https://api.weather.com/v1/Dubai")
