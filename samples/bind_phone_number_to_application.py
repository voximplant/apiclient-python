from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Bind the phone 1 to the application 1.

    PHONE_ID = 1
    APPLICATION_ID = 1
    
    res = voxapi.bind_phone_number_to_application(phone_id=PHONE_ID, application_id=APPLICATION_ID)
    print(res)
