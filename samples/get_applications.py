from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get two applications, but skip the first one.

    OFFSET = 1
    COUNT = 2
    
    res = voxapi.get_applications(offset=OFFSET, count=COUNT)
    print(res)
