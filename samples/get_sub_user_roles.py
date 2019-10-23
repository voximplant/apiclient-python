from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get subuser's roles.

    SUBUSER_ID = 12
    
    try:
        res = voxapi.get_sub_user_roles(SUBUSER_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
