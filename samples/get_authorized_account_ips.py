from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Show the all items.

    
    try:
        res = voxapi.get_authorized_account_ips()
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
