from voximplant.apiclient import VoximplantAPI, VoximplantException
import datetime
import pytz

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the three transactions record from the 2012-01-01 00:00:00 UTC to
    # the 2014-01-01 00:00:00 UTC with the 'gift' or 'money_distribution'
    # types.

    FROM_DATE = datetime.datetime(2012, 1, 1, 0, 0, 0, timezone=pytz.utc)
    TO_DATE = datetime.datetime(2014, 1, 1, 0, 0, 0, timezone=pytz.utc)
    TRANSACTION_TYPE = ["gift", "money_distribution"]
    OUTPUT = "csv"
    
    try:
        res = voxapi.get_transaction_history_async(FROM_DATE,
            TO_DATE,
            transaction_type=TRANSACTION_TYPE,
            output=OUTPUT)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
