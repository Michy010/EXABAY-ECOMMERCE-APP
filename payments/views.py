import requests
import json
import uuid
import time
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from requests_oauthlib import OAuth1
from urllib.parse import parse_qsl

def get_request_token(request):
    # OAuth parameters
    oauth_params = {
        'oauth_callback': 'http://localhost:8000/auth/callback', 
        'oauth_consumer_key': settings.NMB_API_KEY,
        'oauth_signature_method': 'HMAC-SHA256',
        'oauth_timestamp': str(int(time.time())),
        'oauth_nonce': uuid.uuid4().hex,
        'oauth_version': '1.0',
    }

    # Creating an OAuth1 object
    oauth = OAuth1(
        settings.NMB_API_KEY,
        client_secret=settings.NMB_API_SECRET,
        callback_uri='http://localhost:8000/auth/callback',  # Replace with your callback URL
        signature_method='HMAC-SHA256'
    )

    # Making a request to obtain the request token
    response = requests.post(
        'https://obp-api-sandbox.nmbbank.co.tz/oauth/initiate',
        auth=oauth,
        data=oauth_params
    )

    # Parsing the response
    if response.status_code == 200:
        # Parsing the response content and extract oauth_token and oauth_token_secret
        response_data = dict(parse_qsl(response.text))
        oauth_token = response_data.get('oauth_token')
        oauth_token_secret = response_data.get('oauth_token_secret')

        # Store these values for the next steps in the authentication process
        request.session['oauth_token'] = oauth_token
        request.session['oauth_token_secret'] = oauth_token_secret

        # Redirect the user to the authorization URL
        authorization_url = f'https://obp-api-sandbox.nmbbank.co.tz/oauth/authorize?oauth_token={oauth_token}'
        return redirect(authorization_url)
    else:
        # Handling the case where obtaining the request token fails
        return HttpResponse(f"Failed to obtain request token. Status code: {response.status_code}")
    

def direct_login(request):
    # Retrieve the request token and secret from the session
    oauth_token = request.session.get('oauth_token')
    oauth_token_secret = request.session.get('oauth_token_secret')

    # Construct the OAuth1 object for Direct Login
    oauth = OAuth1(
        settings.NMB_API_KEY,
        client_secret=settings.NMB_API_SECRET,
        resource_owner_key=oauth_token,
        resource_owner_secret=oauth_token_secret,
        signature_method='HMAC-SHA256'
    )

    # Preparing headers for Direct Login
    headers = {
        'Content-Type': 'application/json',
        'directlogin': 'username=janeburel,password=the-password-of-jane,consumer_key=' + settings.NMB_API_KEY
    }

    # Making a request to the Direct Login endpoint
    response = requests.post('https://obp-api-sandbox.nmbbank.co.tz/my/logins/direct', auth=oauth, headers=headers)

    # Parse the response
    if response.status_code == 200:
        # Extracting the user token from the response
        user_token = response.json().get('token')
        return HttpResponse(f"Direct Login successful. User Token: {user_token}")
    else:
        # Handling the case where Direct Login fails
        return HttpResponse(f"Direct Login failed. Status code: {response.status_code}")
    

def initiate_oauth2(request):
    authorization_url = 'https://obp-api-sandbox.nmbbank.co.tz/oauth/authorize'

    # OAuth 2.0 parameters
    oauth2_params = {
        'client_id': settings.OAUTH2_CLIENT_ID,
        'redirect_uri': settings.OAUTH2_REDIRECT_URI,
        'scope': settings.OAUTH2_CLIENT_SCOPE,
        'response_type': 'code',
    }

    # Redirecting the user to the authorization URL
    redirect_url = f"{authorization_url}?{'&'.join([f'{key}={value}' for key, value in oauth2_params.items()])}"
    return redirect(redirect_url)

def make_authenticated_api_call(request):
    authorization_code = request.GET.get('code')

    # Exchange authorization code for access token

    
    token_params = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri':'http://localhost:8000/auth/callback',
        'client_id' : 'shk5h3d4m2xre2f0w01vsujlqwpgfksrhyfr5qxk',
        'client_secret':'crwscqzhmi5owvvwgz03l0oyhblibqs4o4sekyti',
    }

    token_url = 'https://obp-api-sandbox.nmbbank.co.tz/oauth/token'
    token_response = requests.post(token_url, data=token_params)

    if token_response.status_code == 200:
        access_token = token_response.json().get('access_token')

    # API endpoint and payload
    api_url = 'https://obp-api-sandbox.nmbbank.co.tz/obp/v2.0.0/banks/obp-bankx-n/accounts/my-new-account-id'
    payload = {
        "type": "CURRENT",
        "balance": {
            "currency": "USD",
            "amount": "0"
        }
    }

    # Headers for the authenticated request
    headers = {
        'Content-Type': 'application/json',
        'directlogin': f'token={access_token}'
    }

    # Making the authenticated API call
    response = requests.put(api_url, data=json.dumps(payload), headers=headers)

    # Checking the response status and handle accordingly
    if response.status_code == 200:
        return HttpResponse(f"API call successful. Response: {response.text}")
    else:
        return HttpResponse(f"API call failed. Status code: {response.status_code}, Response: {response.text}")