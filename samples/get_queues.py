from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the two queues.

    COUNT = 2
    
    try:
        res = voxapi.get_queues(count=COUNT)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
