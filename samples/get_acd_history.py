from voximplant.apiclient import VoximplantAPIConfig, VoximplantAPI, VoximplantException

if __name__ == "__main__":
    config = VoximplantAPIConfig(
        credentials_file_path="credentials.json",
    )
    voxapi = VoximplantAPI(config=config)
    
    # Get the two ACD session history records from the 2012-01-01 00:00:00
    # to the 2014-04-01 00:00:00.

    FROM_DATE = datetime.datetime(2012, 1, 1, 0, 0, 0, timezone=pytz.utc)
    TO_DATE = datetime.datetime(2014, 1, 1, 0, 0, 0, timezone=pytz.utc)
    WITH_EVENTS = True
    COUNT = 2
    
    try:
        res = voxapi.get_acd_history(from_date=FROM_DATE,
            to_date=TO_DATE,
            with_events=WITH_EVENTS,
            count=COUNT)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
