from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the record storage with name = ru1.

    RECORD_STORAGE_NAME = "ru1"
    
    try:
        res = voxapi.get_record_storages(record_storage_name=RECORD_STORAGE_NAME)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
