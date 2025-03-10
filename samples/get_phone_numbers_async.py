from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get two attached phone numbers.

    
    try:
        res = voxapi.get_phone_numbers_async()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
