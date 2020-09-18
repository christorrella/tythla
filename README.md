# Tythla - Latest Release: Beta 0.1
A simple Python GUI for Tesla's REST owner-API.

# What it does
Tythla lets a Tesla owner log in to their Tesla account, view each of their vehicle's stats, or even send a command or two to their cars.

# How to use it
Run `tythla.py`. To send vehicle commands or obtain vitals, you must first obtain an `access_token` by loging in via Tythla's main menu.


# How it works
### 1. Obtaining an access token
To interact with a Tesla car, one must firstly obtain an API authorization key, known as an `access_token`. This token is provided by the owner-api in exchange for a valid username and password of a Tesla owner account, and is used in every command sent to Tesla's vehicle network. To obtain an access_token, Tythla's GUI will offer this as an option (to "log in") in the GUI's main menu.

After obtaining an access_token, Tythla might ask for permission to save the access token locally in a plaintext file -- this way, the token isn't unnecessarily pasted into the command-line for every subsequent command sent to a vehicle.

### 2. Selecting a vehicle
Next, to make a specific car do a specific thing, one needs to specify which vehicle they're trying to command. After automatically obtaining a list of vehicles in the Tesla owner's garage from the API, Tythla's GUI will require users to select a default vehicle in the GUI to send commands to.

### 3. Submitting commands / obtaining vitals
Now that there exists a valid `access_token` and a `vehicle_id` that can be sent commands, the user can get information about a car or submit commands to it. If the vehicle isn't awake, Tythla will ask the user if they want to wake the car or not. Either way, the last valid timestamp for the reuqested command or vitals info will be displayed to the user.

# Backstory
Interacting with a Tesla vehicle using the Tesla mobile app is mezmerizing.
After making several [Tasker](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm&hl=en_US) apps using Tesla's REST owner-api, I figured it would be a great exercise to create a simple Python tool that interfaces with said API.
Thus, "Tythla" was born (think "Tesla", but with a lisp, making Python part of the name).

(pssst, that's just the primary goal; the tertiary goal is to impress some Tesla software engineers, and ultimatley, land a job working at Tesla full-time.)

# Credit
Most, if not all, of the API information used to create this tool will be from the unofficial API sources for Tesla's Owner API. These include:
["Tesla API" by Joe Blau](https://www.teslaapi.io/), and [this other source](https://tesla-api.timdorr.com/), who's credited name I couldn't find. 
