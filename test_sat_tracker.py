import pytest
from sat_api import Satellite_Tracker
from pytest_mock import MockerFixture  # Add this import

class TestSatTracker:

    
    def test_get_tle(self,mocker: MockerFixture):
        mock_tle_response = {
            "info": {
            "satid": 25544,
            "satname": "SPACE STATION",
            "transactionscount": 2
            },
            "tle": "1 25544U 98067A   26066.51273615  .00014539  00000-0  27602-3 0  9992\r\n2 25544  51.6318  83.1189 0008132 167.0679 193.0520 15.48507964555998"
        }

        test_sat = Satellite_Tracker()

        # Create mock response
        mock_response = mocker.Mock()
        mock_response.json.return_value = mock_tle_response

        # Mock the instance's session.get
        test_sat.s.get = mocker.Mock(return_value=mock_response)

        # Call the function
        
        result = test_sat.get_tle(25544)

        assert result['info']['satid'] == 25544 # pyright: ignore[reportOptionalSubscript]
        assert result['info']['satname'] == 'SPACE STATION'# pyright: ignore[reportOptionalSubscript]
        assert result['info']['transactionscount'] == 2 # pyright: ignore[reportOptionalSubscript]
        assert result['tle'] == "1 25544U 98067A   26066.51273615  .00014539  00000-0  27602-3 0  9992\r\n2 25544  51.6318  83.1189 0008132 167.0679 193.0520 15.48507964555998" # pyright: ignore[reportOptionalSubscript]

        test_sat.s.get.assert_called_once()
