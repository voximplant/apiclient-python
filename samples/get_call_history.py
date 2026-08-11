from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get the first call session history record with calls and record URLs
    # from the 2020-02-25 00:00:00 UTC to the 2020-02-26 00:00:00 UTC.

    FROM_DATE = datetime.datetime(2020, 2, 25, 0, 0, 0, timezone=pytz.utc)
    TO_DATE = datetime.datetime(2020, 2, 26, 0, 0, 0, timezone=pytz.utc)
    COUNT = 1
    WITH_CALLS = True
    WITH_RECORDS = True
    
    try:
        res = voxapi.get_call_history(from_date=FROM_DATE,
            to_date=TO_DATE,
            count=COUNT,
            with_calls=WITH_CALLS,
            with_records=WITH_RECORDS)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
