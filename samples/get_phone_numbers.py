from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Get the two attached phone numbers.

    COUNT = 2
    
    res = voxapi.get_phone_numbers(count=COUNT)
    print(res)
