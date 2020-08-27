from os import system, name
from time import sleep
import requests
import json

def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')

def requestAccessToken(email, password):

    print("\nRequesting access_token from owner-api.teslamotors.com/oauth/token...\n")

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

    response = requests.post(oauthUrl, data=json.dumps(body), headers=headers)

    status_code = response.status_code

    if (status_code == 200):
        print("Success!")
    else:
        print("Failure.")

    print("\nServer response body:")
    print(response.text)


def obtainAccessToken():
    print("Login: obtain Tesla API access_token\n")

    print("Enter your Tesla account's email and password.\n")

    teslaEmail = input("Email: ")
    teslaPassword = input("Password: ")

    success = requestAccessToken(teslaEmail, teslaPassword)

    input()

def selectVehicleId():
    print("selectVehicleId not yet implemented.")
    input()

def sendCommands():
    print("sendCommands not yet implemented.")
    input()

def checkStatus():
    print("checkStatus not yet implemented.")
    input()

def invalidMenuOpt():
    print("invalidMenuOpt not yet implemented.")
    input()

def menu():

    userQuit = False

    while not (userQuit):

        # prints a really simple menu for now
        # will be more complex as new features are added

        clear()

        print("Tythla - a Python GUI for Tesla's REST owner-API\n")
        # this menu-printing will eventually be a loop
        print("1. Login (obtain access_token)")
        print("2. Select vehicle (specify vehicle_id)")
        print("3. Send vehicle commands")
        print("4. Check vehicle status")

        selection = input("\nSelect an option from above (1-4): ")

        options = {
            1: obtainAccessToken,
            2: selectVehicleId,
            3: sendCommands,
            4: checkStatus
        }

        clear()

        try:
            options.get(int(selection), invalidMenuOpt)()
        except ValueError:
            pass



def main():
    # print a basic menu
    menu()

main()
