from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get messages that had been sent to number 12345678222 starting from
    # March 1, 2019. Number of resulting rows is limited to 2.

    DESTINATION_NUMBER = "12345678222"
    FROM_DATE = datetime.datetime(2019, 3, 1, 0, 0, 0, timezone=pytz.utc)
    
    try:
        res = voxapi.get_sms_history(destination_number=DESTINATION_NUMBER,
            from_date=FROM_DATE)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
