from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the all children.

    
    try:
        res = voxapi.get_children_accounts()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
