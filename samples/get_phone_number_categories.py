from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get the all phone number categories.

    
    try:
        res = voxapi.get_phone_number_categories()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
