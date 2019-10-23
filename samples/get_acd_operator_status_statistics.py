from voximplant.apiclient import VoximplantAPI, VoximplantException
import pytz
import datetime

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get statistics for the 'READY' and 'ONLINE' statuses of all
    # operators; grouped by operators.

    FROM_DATE = datetime.datetime(2019, 5, 20, 11, 0, 0, pytz.utc)
    USER_ID = "all"
    TO_DATE = datetime.datetime(2019, 5, 20, 13, 0, 0, pytz.utc)
    ACD_STATUS = ["READY", "ONLINE"]
    AGGREGATION = "hour"
    GROUP = "user"
    
    try:
        res = voxapi.get_acd_operator_status_statistics(FROM_DATE,
            USER_ID,
            to_date=TO_DATE,
            acd_status=ACD_STATUS,
            aggregation=AGGREGATION,
            group=GROUP)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
