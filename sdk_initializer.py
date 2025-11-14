import os
echo ##active_line2##
from dotenv import load_dotenv
echo ##active_line3##
from facebook_business.api import FacebookAdsApi
echo ##active_line4##

echo ##active_line5##
# Load environment variables
echo ##active_line6##
load_dotenv()
echo ##active_line7##

echo ##active_line8##
# Fetch credentials
echo ##active_line9##
APP_ID = os.getenv('APP_ID')
echo ##active_line10##
APP_SECRET = os.getenv('APP_SECRET')
echo ##active_line11##
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
echo ##active_line12##

echo ##active_line13##
# Initialize Facebook SDK
echo ##active_line14##
FacebookAdsApi.init(APP_ID, APP_SECRET, ACCESS_TOKEN)
echo ##active_line15##

echo ##active_line16##
def get_business_account():
echo ##active_line17##
    print(f'Facebook SDK initialized with App ID: {APP_ID}')
echo ##active_line18##

