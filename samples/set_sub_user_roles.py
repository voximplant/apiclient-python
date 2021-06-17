from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Add the roles 1, 2, 3 to the subuser with id = 12.

    SUBUSER_ID = 12
    ROLE_ID = 1
    
    try:
        res = voxapi.set_sub_user_roles(SUBUSER_ID,
            role_id=ROLE_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
