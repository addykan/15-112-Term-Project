import requests, requests_oauthlib, webbrowser, random, json
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth

# https://stackoverflow.com/questions/47118598/python-how-to-open-default
# -browser-using-webbrowser-module
# webbrowser.get('windows-default').open('https://youtube.com')


# From Bungie
# API Key: 0cdfb6cae08442709dda79450bdfe07b
# API URL: https://www.bungie.net/en/OAuth/Authorize
# OAuth Client ID: 34708
from requests_oauthlib import OAuth2Session


class apiInfo(object):
    key = '0cdfb6cae08442709dda79450bdfe07b'
    authUrl = 'https://www.bungie.net/en/OAuth/Authorize'
    tokenUrl = 'https://www.bungie.net/platform/app/oauth/token/'
    clientId = '34708'
    random = random.randint(5, 50)
    tempAuthCode = '463b48a29218ee00aa468086b0a816f7'


# https://stackoverflow.com/questions/47118598/python-how-to-open-default
# -browser-using-webbrowser-module
#webbrowser.get('windows-default').open(f'{apiInfo.authUrl}?client_id='
                                       #f'{apiInfo.clientId}&response_type=code&state={apiInfo.random}')

#authCode = input('Please enter the last section of the redirected url here: ')
# print(authCode)
# 1649616b845a84126388919f4d7b14c9

# tokenParams = {'grant_type' : 'authorization_code', 'code' : authCode, 'client_id' : apiInfo.clientId}
# returnedTokenUrl = requests.post(apiInfo.tokenUrl, params = tokenParams)
# print(returnedTokenUrl.status_code)
# print(returnedTokenUrl.content)
# tokenDict = json.loads(returnedTokenUrl.content)

# auth = HTTPBasicAuth(apiInfo.clientId, password = '')
# client = BackendApplicationClient(client_id=apiInfo.clientId)
# bungie = OAuth2Session(client = client)
# token = bungie.fetch_token(token_url=apiInfo.tokenUrl, auth=auth)
# print(token)

# def get_token(authCode):
#     HEADERS = {"X-API-Key": apiInfo.key}
#     post_data = {'code': authCode}
#     response = requests.post(apiInfo.tokenUrl, json=post_data, headers=HEADERS)
#     return response
#
# tokenResponse = get_token(authCode)
# print(tokenResponse)
