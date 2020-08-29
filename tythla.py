# for the clear screen function
from os import system, name
from time import sleep
import time

# for doing Tesla API server requests
import requests
import json
import datetime

# used for verbose output
debug = False

# used for sending commands to specific vehicle
id = -1

def clear():

    # Clears the screen. Useful for a pretty interface.

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')


def getTimeUTC(timestamp):

    # useful for printing dates

    return str(datetime.datetime.fromtimestamp(timestamp)) + " UTC"


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

def requestVehicleList(access_token):

    # Requests list of vehicles from Tesla owner's account

    print("\nRequesting vehicle list from Tesla owner-API...")

    oauthUrl = "https://owner-api.teslamotors.com/api/1/vehicles"
    headers = {
        "Authorization": "Bearer " + access_token
    }
    body = {}

    # do the GET request
    response = requests.get(oauthUrl, data=json.dumps(body), headers=headers)

    # obtain the server response code from response
    status_code = response.status_code
    responseJSON = response.json()

    if not (status_code == 200):
        print("Failure.")
        print("HTTP Status Code = " + str(status_code))
        print("Server response body: " + response.text)
        return False
    else:
        print("Success.")

        if debug:
            print("\n\nFull response body: \n" + response.text)

        # parse first layer of response
        response = responseJSON.get("response")
        count = responseJSON.get("count")



        return response


def requestAccessToken(email, password):

    # Does the actual dirty work of requesting an access token from Tesla's API.

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


def obtainAccessToken():

    # Ask user for email and password and submit to other method for getting access_token

    print("Enter your Tesla account's email and password.\n")

    teslaEmail = input("Email: ")
    teslaPassword = input("Password: ")

    success = requestAccessToken(teslaEmail, teslaPassword)

def selectVehicleId():

    # requests list of vehicles from Tesla's API and displays them to user

    # first load the token

    access_token = loadToken()

    if not access_token:
        print("Unable to request vehicle list without valid token.")
        return

    # then request the vehicle list from the API

    response = requestVehicleList(access_token)

    #print(response)

    # turn response into a dict of kv's

    vehicles = {}
    for vehicle in response:
        #print(vehicle)
        vehicles.update({response.index(vehicle) + 1 : vehicle})

    #print(vehicles)


    # print the available vehicles and ask user to select a vehicle

    while (True):
        clear()
        print("[Select Vehicle]\n")
        print("Vehicles found in your Tesla account:\n")

        for vehicle in vehicles:
            print(
                str(vehicle) + ". " +
                "Name: " + vehicles.get(vehicle).get("display_name") + ", "
                "Model: " + vehicles.get(vehicle).get("vin")[3] + ", "
                "VIN: " + vehicles.get(vehicle).get("vin") + ", "
                "id: " + str(vehicles.get(vehicle).get("id"))
            )


        selection = input("\nSelect an vehicle from above (1-" + str(len(response)) + "): ")

        try:
            # if option is valid
            if int(selection) <= len(response) and int(selection) > 0 :

                print("\nVehicle selected: \n"
                    "Name: " + vehicles.get(int(selection)).get("display_name") + ", "
                    "Model: " + vehicles.get(int(selection)).get("vin")[3] + ", "
                    "VIN: " + vehicles.get(int(selection)).get("vin") + ", "
                    "id: " + str(vehicles.get(int(selection)).get("id"))
                )

                break

        except:
            pass




def sendCommands():
    print("sendCommands not yet implemented.")

def checkStatus():
    print("checkStatus not yet implemented.")

def menu():

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

        clear()





def main():

    clear()

    menu()

main()
