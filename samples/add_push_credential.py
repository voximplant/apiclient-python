from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # Add new Apple credentials.

    PUSH_PROVIDER_NAME = "APPLE"
    CERT_PASSWORD = "12345678"
    CERT_FILE_NAME = "apple_certificate_name"
    IS_DEV_MODE = False'
    
    try:
        res = voxapi.add_push_credential(push_provider_name=PUSH_PROVIDER_NAME,
            cert_password=CERT_PASSWORD,
            cert_file_name=CERT_FILE_NAME,
            is_dev_mode=IS_DEV_MODE)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
