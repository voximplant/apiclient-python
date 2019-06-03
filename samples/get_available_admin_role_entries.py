from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the all available admin role entries.

    
    res = voxapi.get_available_admin_role_entries()
    print(res)
