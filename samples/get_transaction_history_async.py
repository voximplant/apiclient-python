from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get the three transactions record from the 2012-01-01 00:00:00 UTC to
    # the 2014-01-01 00:00:00 UTC with the 'gift' or 'money_distribution'
    # types.

    FROM_DATE = datetime.datetime(2012, 1, 1, 0, 0, 0, timezone=pytz.utc)
    TO_DATE = datetime.datetime(2014, 1, 1, 0, 0, 0, timezone=pytz.utc)
    TRANSACTION_TYPE = ["gift", "money_distribution"]
    OUTPUT = "csv"
    
    try:
        res = voxapi.get_transaction_history_async(from_date=FROM_DATE,
            to_date=TO_DATE,
            transaction_type=TRANSACTION_TYPE,
            output=OUTPUT)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
