# for the clear screen function
from os import system, name
from time import sleep

# for doing Tesla API server requests
import requests
import json
import datetime

# used for verbose output
debug = True

access_token = ""
expiry = ""

def clear():
    # Clears the screen. Useful for a pretty interface.

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')

def saveToken(JSONtext):

    # attempts to save token information from owner-api to local disk

    try:
        print("Saving token...")

        fo = open("oauth.json", "w")
        fo.write(JSONtext)
        fo.close()

        print("Token saved.")
    except:
        print("Unable to save token; unknown error.")

def loadToken():

    # attempts to load previously saved token info from owner-api

    try:
        print("Loading token...")

        with open('oauth.json') as f:
            data = json.load(f)

        f.close()

        print("Token loaded.")

        print("access_token: " + data.get("access_token"))
        print("expiry: " + str(data.get("expires_in")))
    except FileNotFoundError:
        print("oauth.json not found in current directory; new access_token/login required.")


def requestAccessToken(email, password):
    # Does the actual dirty work of requesting an access token from Tesla's API.

    print("\nRequesting access_token from Tesla owner-API...\n")

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



def obtainAccessToken():
    # Ask user for email and password and submit to other method for getting access_token

    print("Enter your Tesla account's email and password.\n")

    teslaEmail = input("Email: ")
    teslaPassword = input("Password: ")

    success = requestAccessToken(teslaEmail, teslaPassword)

def selectVehicleId():
    print("selectVehicleId not yet implemented.")

def sendCommands():
    print("sendCommands not yet implemented.")

def checkStatus():
    print("checkStatus not yet implemented.")

def menu():

    loadToken()

    menuOptionText = {
        1: "Log in: obtain an access_token",
        2: "Select vehicle: specify a vehicle_id",
        3: "Send vehicle commands",
        4: "Check vehicle status",
        5: "Quit Tythla"
    }

    functions = {
        1: obtainAccessToken,
        2: selectVehicleId,
        3: sendCommands,
        4: checkStatus
    }

    while (True):

        # prints a really simple menu for now
        # will be more complex as new features are added

        clear()

        # print menu header
        print("Tythla - a Python GUI for Tesla's REST owner-API\n")

        # this menu-printing will eventually be a loop
        for item in menuOptionText.keys():
            print(str(item) + ". " + menuOptionText.get(item))

        selection = input("\nSelect an option from above (1-5): ")

        # quit if the user wants to leave
        if (selection == "5"):
            break

        # clear screen in anticipation of menu option appearing
        clear()

        try:
            # if option is valid, go to that function
            if int(selection) in functions.keys():

                # print function header
                print("[" + selection + ". " + menuOptionText.get(int(selection)) +"]\n")
                # actually do the function
                functions.get(int(selection))()
                # menu option has been exercised; time for next selection
                input("\nPress enter to continue...")

        except:
            pass





def main():
    # print a basic menu
    menu()

main()
