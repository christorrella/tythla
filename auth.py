import requests
import datetime
import json
import time

debug = False

def getTimeUTC(timestamp):

    # useful for printing dates

    return str(datetime.datetime.fromtimestamp(timestamp)) + " UTC"

def obtainAccessToken():

    # Ask user for email and password and submit to other method for getting access_token

    print("Enter your Tesla account's email and password.\n")

    teslaEmail = input("Email: ")
    teslaPassword = input("Password: ")

    success = requestAccessToken(teslaEmail, teslaPassword)

def saveToken(JSONtext):

    # attempts to save token information from owner-api to local disk

    try:
        print("Saving token...")

        fo = open("oauth.json", "w")
        fo.write(JSONtext)
        fo.close()

        print("Token saved.")

        return True

    except:
        print("Unable to save token; unknown error.")

        return False

def loadToken():

    # attempts to load previously saved token info from owner-api

    try:
        print("Loading token...")

        with open('oauth.json') as f:
            data = json.load(f)

        f.close()

        print("Token file loaded...")

        expiry = data.get("expires_in") + data.get("created_at")

        if debug:
            print("access_token: " + data.get("access_token"))
            print("expiry: " + getTimeUTC(expiry))

        if isTokenValid(expiry):
            return data.get("access_token")
        else:
            return ""

    except FileNotFoundError:
        print("oauth.json not found in current directory; new access_token/login required.")

        return ""

def isTokenValid(expiry):

    # checks if loaded token information is valid based on timestamp

    print("Checking the token's validity...")

    if time.time() > expiry :
        print("The token in oauth.json has expired. Request a new one from the main menu.")
        return False
    else:
        print("Token not expired.")
        return True

def requestAccessToken(email, password):

    # Requests an access token from Tesla's API

    print("\nRequesting access_token from Tesla owner-API...")

    oauthUrl = "https://owner-api.teslamotors.com/oauth/token"
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "password": password,
        "email": email,
        "client_secret": "c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3",
        "client_id": "81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384",
        "grant_type": "password"
    }

    # do the POST request
    response = requests.post(oauthUrl, data=json.dumps(body), headers=headers)

    # obtain the server response code from response
    status_code = response.status_code
    responseJSON = response.json()

    # let the user know if anything went wrong
    if not (status_code == 200):
        print("Failure.")
        print("HTTP Status Code = " + str(status_code))
        print("Server response body: " + response.text)
        return False
    else:
        print("Success.")

        access_token = responseJSON.get("access_token")
        created_at = responseJSON.get("created_at")
        expires_in = responseJSON.get("expires_in")

        creation_date_UTC = str(datetime.datetime.fromtimestamp(created_at))
        expiration_date_UTC = str(datetime.datetime.fromtimestamp(expires_in + created_at))

        print("access_token: " + access_token)
        print("creation date: " + creation_date_UTC)
        print("expiry date: " + expiration_date_UTC)

        if debug:
            print("\n\nFull response body: \n" + response.text)

        saveToken(response.text)
