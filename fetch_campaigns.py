import os
import csv
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
from dotenv import load_dotenv

load_dotenv()

app_id = os.getenv('APP_ID')
app_secret = os.getenv('APP_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
account_id = os.getenv('ACCOUNT_ID')

FacebookAdsApi.init(app_id=app_id, app_secret=app_secret, access_token=access_token)

ad_account = AdAccount(account_id)
campaigns = ad_account.get_campaigns(fields=['id', 'name', 'status'])

with open('campaigns_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Campaign ID', 'Name', 'Status'])
    for campaign in campaigns:
        writer.writerow([campaign['id'], campaign['name'], campaign['status']])

print('Data fetched and written to campaigns_data.csv')
