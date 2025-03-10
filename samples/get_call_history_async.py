from voximplant.apiclient import VoximplantAPI, VoximplantException
import datetime
import pytz

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the first call session history record with calls and record URLs
    # from the 2020-02-25 00:00:00 UTC to the 2020-02-26 00:00:00 UTC.

    FROM_DATE = datetime.datetime(2020, 2, 25, 0, 0, 0, timezone=pytz.utc)
    TO_DATE = datetime.datetime(2020, 2, 26, 0, 0, 0, timezone=pytz.utc)
    WITH_CALLS = True
    WITH_RECORDS = True
    OUTPUT = "csv"
    
    try:
        res = voxapi.get_call_history_async(FROM_DATE,
            TO_DATE,
            with_calls=WITH_CALLS,
            with_records=WITH_RECORDS,
            output=OUTPUT)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
