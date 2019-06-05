from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get all active sip registrations

    
    try:
        res = voxapi.get_sip_registrations()
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
