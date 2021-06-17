from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Edit the password and description for the subuser with id = 12 from
    # account_id = 1.

    SUBUSER_ID = 12
    OLD_SUBUSER_PASSWORD = "old_test_password"
    NEW_SUBUSER_PASSWORD = "test_pass"
    DESCRIPTION = "test_desc"
    
    try:
        res = voxapi.set_sub_user_info(SUBUSER_ID,
            old_subuser_password=OLD_SUBUSER_PASSWORD,
            new_subuser_password=NEW_SUBUSER_PASSWORD,
            description=DESCRIPTION)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
