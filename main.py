import sat_api
from satellite_ids import * 
import json

def pretty_print_json(data,indent=2,sort_keys=False):
     print(json.dumps(data, indent=indent, sort_keys=sort_keys, default=str))

def main():
    
    iss_tracker = sat_api.Satellite_Tracker()
    iss_tle = iss_tracker.get_tle(ISS_ID)
    pretty_print_json(iss_tle)
    
if __name__ == "__main__":
    main()
