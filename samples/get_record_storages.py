from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the record storage with name = ru1.

    RECORD_STORAGE_NAME = "ru1"
    
    res = voxapi.get_record_storages(record_storage_name=RECORD_STORAGE_NAME)
    print(res)
