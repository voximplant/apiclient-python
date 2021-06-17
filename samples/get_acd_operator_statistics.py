from voximplant.apiclient import VoximplantAPI, VoximplantException
import pytz
import datetime

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get AC and TT statistics for two operators and the queue from the
    # specified date.

    FROM_DATE = datetime.datetime(2021, 4, 8, 0, 0, 0, pytz.utc)
    USER_ID = 1768
    TO_DATE = datetime.datetime(2021, 4, 10, 0, 0, 0, pytz.utc)
    ACD_QUEUE_ID = 54
    REPORT = "AC"
    AGGREGATION = "day"
    
    try:
        res = voxapi.get_acd_operator_statistics(FROM_DATE,
            USER_ID,
            to_date=TO_DATE,
            acd_queue_id=ACD_QUEUE_ID,
            report=REPORT,
            aggregation=AGGREGATION)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
