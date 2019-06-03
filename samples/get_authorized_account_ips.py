from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Show the all items.

    
    res = voxapi.get_authorized_account_ips()
    print(res)
