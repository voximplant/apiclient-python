from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get all active sip registrations

    
    res = voxapi.get_sip_registrations()
    print(res)
