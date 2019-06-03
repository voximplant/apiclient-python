from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Delete the 92.255.220.0/24 network from all the lists.

    AUTHORIZED_IP = "92.255.220.0/24"
    
    res = voxapi.del_authorized_account_ip(authorized_ip=AUTHORIZED_IP)
    print(res)
