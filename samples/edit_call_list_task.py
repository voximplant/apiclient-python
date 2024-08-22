from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Set attempts_left, start_at, and custom_data the task with id=1 in
    # the call list with id=1.

    LIST_ID = 1
    TASK_ID = 1
    ATTEMPTS_LEFT = 2
    START_AT = datetime.datetime(2023, 11, 13, 18, 0, 0, timezone=pytz.utc)
    CUSTOM_DATA = "{\"phone\":\"555111222333\",\"name\":\"Mr.Fate\"}"
    
    try:
        res = voxapi.edit_call_list_task(LIST_ID,
            task_id=TASK_ID,
            attempts_left=ATTEMPTS_LEFT,
            start_at=START_AT,
            custom_data=CUSTOM_DATA)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
