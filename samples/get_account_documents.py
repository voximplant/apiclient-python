from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    WITH_DETAILS = True
    
    res = voxapi.get_account_documents(with_details=WITH_DETAILS)
    print(res)
