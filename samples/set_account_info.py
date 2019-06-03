from voximplant.apiclient import VoximplantAPI

if __name__ == "__main__":
    voxapi = VoximplantAPI("credentials.json")

    # Set the notification settings.

    LANGUAGE_CODE = "en"
    LOCATION = "GMT-8"
    MIN_BALANCE_TO_NOTIFY = "1.50"
    TARIFF_CHANGING_NOTIFICATIONS = True
    NEWS_NOTIFICATIONS = True
    
    res = voxapi.set_account_info(language_code=LANGUAGE_CODE, location=LOCATION, min_balance_to_notify=MIN_BALANCE_TO_NOTIFY, tariff_changing_notifications=TARIFF_CHANGING_NOTIFICATIONS, news_notifications=NEWS_NOTIFICATIONS)
    print(res)
