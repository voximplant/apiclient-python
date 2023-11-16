from voximplant.apiclient import VoximplantAPI, VoximplantException
import datetime
import pytz

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Generate a service_level report file in csv format for the period
    # from 2021-03-17 00:00:00 to 2021-03-17 22:00:00.

    FROM_DATE = datetime.datetime(2021, 3, 17, 0, 0, 0, timezone=pytz.utc)
    TO_DATE = datetime.datetime(2021, 3, 17, 22, 0, 0, timezone=pytz.utc)
    REPORT_TYPE = "service_level"
    APPLICATION_ID = 1
    SQ_QUEUE_ID = 1
    MAX_WAITING_SEC = 6
    
    try:
        res = voxapi.request_smart_queue_history(FROM_DATE,
            TO_DATE,
            REPORT_TYPE,
            application_id=APPLICATION_ID,
            sq_queue_id=SQ_QUEUE_ID,
            max_waiting_sec=MAX_WAITING_SEC)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
