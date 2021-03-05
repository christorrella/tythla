import requests
import json

debug = True

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

def requestVehicleStatus(access_token, selected_vehicle_id):

    print("\nRequesting vehicle status from Tesla owner-API...")

    oauthUrl = "https://owner-api.teslamotors.com/api/1/vehicles/" + selected_vehicle_id + "/vehicle_data"
    headers = {
        "Authorization": "Bearer " + access_token
    }
    body = {}

    print(selected_vehicle_id)



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
