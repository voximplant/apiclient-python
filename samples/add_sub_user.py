from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Create a new subuser for account_id = 1

    NEW_SUBUSER_NAME = "John_McClane"
    NEW_SUBUSER_PASSWORD = "pssw0rd"
    
    try:
        res = voxapi.add_sub_user(NEW_SUBUSER_NAME,
            NEW_SUBUSER_PASSWORD)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
