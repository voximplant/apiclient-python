from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get subusers info

    
    try:
        res = voxapi.get_sub_users()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
