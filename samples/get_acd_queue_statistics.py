from voximplant.apiclient import VoximplantAPI, VoximplantException
import datetime
import pytz

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get WT and TT statistics for the queue from the specified date.

    FROM_DATE = datetime.datetime(2021, 4, 8, 0, 0, 0, timezone=pytz.utc)
    TO_DATE = datetime.datetime(2021, 4, 10, 0, 0, 0, timezone=pytz.utc)
    ACD_QUEUE_ID = 54
    REPORT = ["WT", "TT"]
    AGGREGATION = "day"
    
    try:
        res = voxapi.get_acd_queue_statistics(FROM_DATE,
            to_date=TO_DATE,
            acd_queue_id=ACD_QUEUE_ID,
            report=REPORT,
            aggregation=AGGREGATION)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
