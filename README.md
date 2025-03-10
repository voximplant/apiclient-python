# Voximplant API client library

#### Version 2.0.0

## Prerequisites

In order to use the Voximplant Python SDK, you need the following:

1. A developer account. If you don't have one, [sign up here](https://voximplant.com/sign-up/).
1. A private API key. There are 2 options to obtain it:
    1. Either generate it in the [Voximplant Control panel](https://manage.voximplant.com/settings/service_accounts)
    1. Or call the [CreateKey](https://voximplant.com/docs/references/httpapi/managing_role_system#createkey) HTTP API
       method with the
       specified [authentication parameters](https://voximplant.com/docs/references/httpapi/auth_parameters). You'll
       receive a response with the __result__ field in it. Save the __result__ value in a file (since we don't store the
       keys, save it securely on your side).
1. Python 2.x or 3.x runtime with `pip` and `setuptools`>=18.5 installed

## How to use

Go to your project folder and install the SDK using `pip`:

```bash 
python -m pip install --user voximplant-apiclient
```

Then import the SDK in your script

```python
from voximplant.apiclient import VoximplantAPI
```

Next, specify the path to the JSON service account file either in the constructor or using the environment.

__constructor__:

```python
api = VoximplantAPI("/path/to/credentials.json")
```

__env__:

```bash
export VOXIMPLANT_CREDENTIALS=/path/to/credentials.json
```

## Examples

### Start a scenario

```python
from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    api = VoximplantAPI("credentials.json")

    # Start a scenario of the user 1

    RULE_ID = 1
    SCRIPT_CUSTOM_DATA = "mystr"
    USER_ID = 1

    try:
        res = api.start_scenarios(RULE_ID, script_custom_data=SCRIPT_CUSTOM_DATA, user_id=USER_ID)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
```

### Send an SMS

```python
from voximplant.apiclient import VoximplantAPI, VoximplantException

if __name__ == "__main__":
    api = VoximplantAPI("credentials.json")

    # Send the SMS with the "Test message" text from the phone number 447443332211 to the phone number 447443332212

    SOURCE = "447443332211"
    DESTINATION = "447443332212"
    SMS_BODY = "Test message"

    try:
        res = api.send_sms_message(SOURCE, DESTINATION, SMS_BODY)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))
```

### Get a call history item

```python
from voximplant.apiclient import VoximplantAPI, VoximplantException
import pytz
import datetime

if __name__ == "__main__":
    api = VoximplantAPI("credentials.json")

    # Get the first call session history record from the 2012-01-01 00:00:00 UTC to the 2014-01-01 00:00:00 UTC

    FROM_DATE = datetime.datetime(2012, 1, 1, 0, 0, 0, pytz.utc)
    TO_DATE = datetime.datetime(2014, 1, 1, 0, 0, 0, pytz.utc)
    COUNT = 1

    try:
        res = api.get_call_history(FROM_DATE, TO_DATE, count=COUNT)
        print(res)
    except VoximplantException as e:
        print("Error: {}".format(e.message))

```

