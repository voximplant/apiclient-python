from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get the brief call session history from the 2020-02-25 00:00:00 UTC
    # to the 2020-02-26 00:00:00 UTC.

    OUTPUT = "cvs"
    FROM_DATE = datetime.datetime(2020, 2, 25, 0, 0, 0, timezone=pytz.utc)
    TO_DATE = datetime.datetime(2020, 2, 26, 0, 0, 0, timezone=pytz.utc)
    
    try:
        res = voxapi.get_brief_call_history(OUTPUT,
            from_date=FROM_DATE,
            to_date=TO_DATE)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
