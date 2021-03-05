# for the clear screen function
from os import system, name
from time import sleep
import time

# for doing Tesla API server requests
import requests
import json
import datetime

#out own helper methods

from auth import obtainAccessToken, loadToken


# used for verbose output
debug = False

# used for sending commands to specific vehicle
selected_vehicle_id = ""

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

def requestVehicleStatus(access_token):


    # we need this global variable
    global selected_vehicle_id

    print("\nRequesting vehicle status from Tesla owner-API...")

    oauthUrl = "https://owner-api.teslamotors.com/api/1/vehicles/" + selected_vehicle_id + "/vehicle_data"
    headers = {
        "Authorization": "Bearer " + access_token
    }
    body = {}



    # do the POST request
    response = requests.get(oauthUrl, data=json.dumps(body), headers=headers)

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

        if debug:
            print("\n\nFull response body: \n" + response.text)

        return response



#def printVehicleStats(data, depth):

    # we assume that data is a key,value dict pair

    # base case: value (NOT key) of data not a list or dictionary
    #if (not isinstance(data, type(list)) and not isinstance(data, type(dict))):





def selectVehicleId():

    # requests list of vehicles from Tesla's API and displays them to user

    # let python know this is referring to global var

    global selected_vehicle_id

    # load the token from file

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

                selected_vehicle = vehicles.get(int(selection))

                selected_vehicle_id = str(selected_vehicle.get("id"))

                print("\nVehicle selected: \n"
                    "Name: " + selected_vehicle.get("display_name") + ", "
                    "Model: " + selected_vehicle.get("vin")[3] + ", "
                    "VIN: " + selected_vehicle.get("vin") + ", "
                    "id: " + str(selected_vehicle.get("id"))
                )
                break

        except:
            pass




def sendCommands():
    print("sendCommands not yet implemented.")

def checkStatus():

    # asks owner-API for information about the selected vehicle

    # check for valid token file

    access_token = loadToken()

    if not access_token:
        print("Unable to request vehicle status without valid token.")
        return

    # check for valid vehicle ID on file

    # let python know we want the global var
    global selected_vehicle_id

    if not selected_vehicle_id:
        print("Unable to request vehicle status without a selected vehicle.")
        return

    # then request the vehicle list from the API

    response = requestVehicleStatus(access_token)

    resp_dict = json.loads(response.text)

    resp_dict = resp_dict["response"]

    opts = resp_dict["option_codes"]

    print(type(opts))

def menu():

    menuOptionText = {
        1: "Log in: obtain an access_token",
        2: "Select vehicle: specify a vehicle's id",
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
