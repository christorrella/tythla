from os import system, name
from time import sleep

def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')


def obtainAccessToken():
    print("obtainAccessToken not yet implemented.")
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
