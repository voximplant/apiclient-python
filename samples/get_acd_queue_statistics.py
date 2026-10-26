from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException
import pytz
import datetime

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get WT and TT statistics for the queue from the specified date.

    FROM_DATE = datetime.datetime(2021, 4, 8, 0, 0, 0, timezone=pytz.utc)
    ACD_QUEUE_ID = 54
    TO_DATE = datetime.datetime(2021, 4, 10, 0, 0, 0, timezone=pytz.utc)
    REPORT = ["WT", "TT"]
    AGGREGATION = "day"
    
    try:
        res = voxapi.get_acd_queue_statistics(FROM_DATE,
            ACD_QUEUE_ID,
            to_date=TO_DATE,
            report=REPORT,
            aggregation=AGGREGATION)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
