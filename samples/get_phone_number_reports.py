from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Get all the reports.

    
    try:
        res = voxapi.get_phone_number_reports()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
