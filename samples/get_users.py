from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get two first identities.

    APPLICATION_ID = 1
    COUNT = 2
    
    res = voxapi.get_users(application_id=APPLICATION_ID, count=COUNT)
    print(res)
