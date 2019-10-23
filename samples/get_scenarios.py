from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get two scenarios, but skip the first one.

    OFFSET = 1
    COUNT = 2
    
    try:
        res = voxapi.get_scenarios(offset=OFFSET,
            count=COUNT)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
