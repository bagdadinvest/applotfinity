import os
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi

def initialize_sdk():
    load_dotenv()

    app_id = os.getenv('APP_ID')
    app_secret = os.getenv('APP_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    account_id = os.getenv('ACCOUNT_ID')

    if not all([app_id, app_secret, access_token, account_id]):
        raise EnvironmentError("One or more required environment variables are missing.")

    FacebookAdsApi.init(app_id=app_id, app_secret=app_secret, access_token=access_token)
    print(f"SDK initialized for account ID: {account_id}")

if __name__ == "__main__":
    initialize_sdk()
