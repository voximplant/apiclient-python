from voximplant.apiclient import VoximplantAPI, VoximplantException
import pytz
import datetime

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the three transactions record from the 2012-01-01 00:00:00 UTC to
    # the 2014-01-01 00:00:00 UTC with the 'gift' or 'money_distribution'
    # types.

    FROM_DATE = datetime.datetime(2012, 1, 1, 0, 0, 0, pytz.utc)
    TO_DATE = datetime.datetime(2014, 1, 1, 0, 0, 0, pytz.utc)
    COUNT = 3
    TRANSACTION_TYPE = ["gift", "money_distribution"]
    
    try:
        res = voxapi.get_transaction_history(FROM_DATE,
            TO_DATE,
            count=COUNT,
            transaction_type=TRANSACTION_TYPE)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
