from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    WITH_DETAILS = True
    
    try:
        res = voxapi.get_account_documents(with_details=WITH_DETAILS)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
