from voximplant.apiclient import VoximplantAPI, VoximplantException
import datetime
import pytz

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the brief call session history from the 2020-02-25 00:00:00 UTC
    # to the 2020-02-26 00:00:00 UTC.

    FROM_DATE = datetime.datetime(2020, 2, 25, 0, 0, 0, timezone=pytz.utc)
    TO_DATE = datetime.datetime(2020, 2, 26, 0, 0, 0, timezone=pytz.utc)
    OUTPUT = "cvs"
    IS_ASYNC = True
    
    try:
        res = voxapi.get_brief_call_history(FROM_DATE,
            TO_DATE,
            OUTPUT,
            IS_ASYNC)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
