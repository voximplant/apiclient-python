from voximplant.apiclient import VoximplantAPI, VoximplantException
import datetime
import pytz

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get statistics for all operators and all queues from the specified
    # date

    FROM_DATE = datetime.datetime(2017, 1, 1, 0, 0, 0, pytz.utc)
    USER_ID = "all"
    
    try:
        res = voxapi.get_acd_operator_statistics(FROM_DATE,
            USER_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
