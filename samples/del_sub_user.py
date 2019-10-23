from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Delete the subuser with id = 12 from account_id = 1

    SUBUSER_ID = 12
    
    try:
        res = voxapi.del_sub_user(SUBUSER_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
