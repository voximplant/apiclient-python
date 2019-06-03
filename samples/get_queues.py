from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the two queues.

    COUNT = 2
    
    res = voxapi.get_queues(count=COUNT)
    print(res)
