import os
import requests
from urllib.parse import urlencode

# Ensure these are set in your environment or .env file
CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')
CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
REDIRECT_URI = os.getenv('DISCORD_REDIRECT_URI')
OAUTH2_TOKEN_URL = 'https://discord.com/api/oauth2/token'
OAUTH2_API_URL = 'https://discord.com/api/users/@me'

def get_discord_login_url():
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'identify email'
    }
    return 'https://discord.com/api/oauth2/authorize?' + urlencode(params)

def exchange_code(code):
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    access_token_response = requests.post(OAUTH2_TOKEN_URL, data=data, headers=headers)
    json_response = access_token_response.json()
    access_token = json_response.get('access_token')
    
    # Now that we have the token, make another request to get the user's info
    user_response = requests.get(
        OAUTH2_API_URL,
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    user_json = user_response.json()
    return user_json  # This contains the user's Discord information
