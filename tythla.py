# for the clear screen function
from os import system, name
from time import sleep

#for doing Tesla API server requests
import requests
import json
import datetime

def clear():
    # Clears the screen. Useful for a pretty interface.

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')

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

        print("\n\nFull response body: \n" + response.text)



def obtainAccessToken():
    # Ask user for email and password and submit to other method for getting access_token

    print("[Obtain a Tesla API access_token]\n")

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

    while (True):

        # prints a really simple menu for now
        # will be more complex as new features are added

        clear()

        print("Tythla - a Python GUI for Tesla's REST owner-API\n")
        # this menu-printing will eventually be a loop
        print("1. Login (obtain access_token)")
        print("2. Select vehicle (specify vehicle_id)")
        print("3. Send vehicle commands")
        print("4. Check vehicle status")
        print("5. Quit")

        selection = input("\nSelect an option from above (1-5): ")

        # quit if the user wants to leave
        if (selection == "5"):
            break

        options = {
            1: obtainAccessToken,
            2: selectVehicleId,
            3: sendCommands,
            4: checkStatus
        }

        # clear screen in anticipation of menu option appearing
        clear()

        try:
            # if option is valid, go to that function
            if int(selection) in options.keys():
                options.get(int(selection))()
                # menu option has been exercised; time for next selection
                input("\nPress enter to continue...")

        except:
            pass





def main():
    # print a basic menu
    menu()

main()
