from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")
    
    # 

    
    try:
        res = voxapi.get_resource_price()
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    
