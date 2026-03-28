import os
import requests
from dotenv import load_dotenv

class Satellite_Tracker:

    BASE_URL = "https://api.n2yo.com/rest/v1/satellite/"
    API_KEY = os.getenv("N2YO_API_KEY")

    def __init__(self):
        self.s = requests.Session()

    def get_tle(self, sat_id:int):
        """Retrieve the Two Line Elements (TLE) for a satellite identified by NORAD id."""
        #Request: https://api.n2yo.com/rest/v1/satellite/tle/25544&apiKey=API_KEY
        try:
            url = f"{self.BASE_URL}tle/{sat_id}/&apiKey={Satellite_Tracker.API_KEY}"
            response = self.s.get(url,timeout=21)
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error fetching TLE: {e}")
            return None

    def parse_tle(self, tle:str):
        """Parse the TLE string into its components.
        Taken from https://en.wikipedia.org/wiki/Two-line_element_set
        :examples :
        :line 1:

        Field 	Columns 	Content 	Example
            1 	01 	Line number 	1
            2 	03-07 	Satellite catalog number 	25544
            3 	08-	    Classification (U: unclassified, C: classified, S: secret)[11] 	U
            4 	10-11 	International Designator (last two digits of launch year) 	98
            5 	12-14 	International Designator (launch number of the year) 	067
            6 	15-17 	International Designator (piece of the launch) 	A
            7 	19-20 	Epoch year (last two digits of year) 	08
            8 	21-32 	Epoch (day of the year and fractional portion of the day) 	264.51782528
            9 	34-43 	First derivative of mean motion; the ballistic coefficient (rev/day, per day)[12] 	-.00002182
            10 	45-52 	Second derivative of mean motion (rev/day³, decimal point assumed)[12] 	00000-0
            11 	54-61 	B*, the drag term, or radiation pressure coefficient (units of 1/(Earth radii), decimal point assumed)[12] 	-11606-4
            12 	63      Ephemeris type (always zero; only used in undistributed TLE data)[13] 	0
            13 	65-68 	Element set number. Incremented when a new TLE is generated for this object.[12] 	292
            14 	69 	Checksum (modulo 10) 	7

        :line 2:
            1 	01 	Line number 	2
            2 	03-07 	Satellite Catalog number 	25544
            3 	09-16 	Inclination (degrees) 	51.6416
            4 	18-25 	Right ascension of the ascending node (degrees), in the ECI reference frame, measured from the vernal point 	247.4627
            5 	27-33 	Eccentricity (unitless, decimal point assumed) 	0006703
            6 	35-42 	Argument of perigee (degrees) 	130.5360
            7 	44-51 	Mean anomaly (degrees) 	325.0288
            8 	53-63 	Mean motion (revolutions per day) 	15.72125391
            9 	64-68 	Revolution number at epoch (revolutions) 	56353
            10 	69 	Checksum (modulo 10) 	7
        """

        tle_data = {}
        lines = tle.splitlines()
        print(lines)

        if len(lines) != 2 and len(lines) != 3:
            raise ValueError("TLE must be 2 or 3 lines.")

        if len(lines) == 2:
            line1 = lines[0]
            line2 = lines[1]

            tle_data = {
            "line1_num": line1[0],
            "sat_cat_num": line1[2:7],
            "classification": line1[7],
            "int_design_yr": line1[9:11],
            "int_design_launch_num": line1[11:14],
            "int_design_piece": line1[14:17],
            "epoch_yr": line1[18:20],
            "epoch_day": line1[20:32],
            "first_deriv_mean_motion": line1[33:43],
            "second_deriv_mean_motion": line1[45:52],
            "bstar": line1[54:61],
            "ephemeris_type": line1[62],
            "ele_set_num": line1[64:68],
            "chksum1": line1[68], # the first checksum is for the first line
            "line2_num": line2[0],
            "sat_cat_num2": line2[2:7],
            "inclination": line2[8:16],
            "rt_ascension": line2[17:25],
            "eccentricity": line2[26:33],
            "arg_perigee": line2[34:42],
            "mean_anomaly": line2[43:51],
            "mean_motion": line2[52:63],
            "rev_at_epoch": line2[63:68],
            "chksum2": line2[68]
            }

        return tle_data
