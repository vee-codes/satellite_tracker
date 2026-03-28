import pytest
from sat_api import Satellite_Tracker
from pytest_mock import MockerFixture

@pytest.fixture
def example_tle() -> str:
    tle = "1 25544U 98067A   26066.51273615  .00014539  00000-0  27602-3 0  9992\r\n2 25544  51.6318  83.1189 0008132 167.0679 193.0520 15.48507964555998"
    return tle

class TestSatTracker:

    def test_get_tle(self,example_tle,mocker: MockerFixture):
        mock_tle_response = {
            "info": {
            "satid": 25544,
            "satname": "SPACE STATION",
            "transactionscount": 2
            },
            "tle": example_tle
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

    def test_parse_tle(self):
        tle = "1 25544U 98067A   26066.51273615  .00014539  00000-0  27602-3 0  9992\r\n2 25544  51.6318  83.1189 0008132 167.0679 193.0520 15.48507964555998"
        test_sat = Satellite_Tracker()
        res = test_sat.parse_tle(tle)
        
        # line 1
        assert res['line1_num'] == '1'
        assert res['sat_cat_num'] == '25544'
        assert res['classification'] == 'U'
        assert res['int_design_yr'] == '98'
        assert res['int_design_launch_num'] == '067'
        assert res['int_design_piece'] == 'A  '
        assert res['epoch_yr'] == '26'
        assert res['epoch_day'] == '066.51273615'
        assert res['first_deriv_mean_motion'] == ' .00014539' # positive represented with whitespace/negative with "-"
        assert res["second_deriv_mean_motion"] == '00000-0'
        assert res['bstar'] == '27602-3'
        assert res['ephemeris_type'] == '0'
        assert res['ele_set_num'] == ' 999'
        assert res['chksum1'] == '2'

        # line 2
        assert res['line2_num'] == '2'
        assert res['sat_cat_num2'] == '25544'
        assert res['inclination'] == ' 51.6318'
        assert res['rt_ascension'] == ' 83.1189'
        assert res['eccentricity'] == '0008132'
        assert res['arg_perigee'] == '167.0679'
        assert res['mean_anomaly'] == '193.0520'
        assert res['mean_motion'] == '15.48507964'
        assert res['rev_at_epoch'] == '55599'
        assert res['chksum2'] == '8'

    def test_checkum_calc(self,example_tle):
        test_sat = Satellite_Tracker()
        res = test_sat.parse_tle(example_tle)
        assert test_sat.tle_checksum(example_tle)[0] == 2
        assert test_sat.tle_checksum(example_tle)[1] == 8

