from voximplant.apiclient import VoximplantAPI, VoximplantException
import datetime
import pytz

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the first call session history record from the 2012-01-01 00:00:00 UTC to the 2014-01-01 00:00:00 UTC

    FROM_DATE = datetime.datetime(2012, 1, 1, 0, 0, 0, pytz.utc)
    TO_DATE = datetime.datetime(2014, 1, 1, 0, 0, 0, pytz.utc)
    COUNT = 1
    
    try:
        res = voxapi.get_call_history(FROM_DATE, TO_DATE, count=COUNT)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
