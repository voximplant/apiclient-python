from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the two attached phone numbers.

    COUNT = 2
    
    try:
        res = voxapi.get_phone_numbers(count=COUNT)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
    print(res)
