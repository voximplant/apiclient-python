from voximplant.apiclient import VoximplantAPI
import datetime
import pytz

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the three log items from the 2018-02-01 00:00:00 to the 2018-03-01 00:00:00 and filter.

    FROM_DATE = datetime.datetime(2018, 2, 1, 0, 0, 0, pytz.utc)
    TO_DATE = datetime.datetime(2018, 3, 1, 0, 0, 0, pytz.utc)
    FILTERED_CMD = ["BindSkill", "AddSkill", "DelSkill"]
    ADVANCED_FILTERS = "152"
    COUNT = 3
    
    res = voxapi.get_audit_log(FROM_DATE, TO_DATE, filtered_cmd=FILTERED_CMD, advanced_filters=ADVANCED_FILTERS, count=COUNT)
    print(res)
