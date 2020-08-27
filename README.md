# Description
Tyhtla: a Python GUI for Tesla's REST owner-API.

# Backstory
I always loved the fact that you can interact with a Tesla vehicle using a mobile app on either iOS or Android. 
After making several [Tasker](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm&hl=en_US) apps using Tesla's REST owner-api, I figured it would be a great exercise to create a simple Python tool that interfaces with said API.
Thus, "Tythla" was born (think "Tesla", but with a lisp, making Python part of the name).

(pssst, that's just the primary goal; the tertiary goal is to impress some Tesla software engineers, and ultimatley, land a job working at Tesla full-time.)

# Intended featureset

I think the best way to implement Tythla will be to create a command-line GUI with Python. At first, I thought a command-line argument setup would be best, but after realizing the amount of session-specific information that needs to be stored (such as `access_token` and `vehicle_id`s) I think it would be best to save some information locally (like an `access_token`) and to temporarily store some other items (like `vehicle_id`) in RAM during runtime.

Basic commands will be as follows, subject to change as the project progresses:

### 1. Obtaining an access token
To interact with a Tesla car, one must firstly obtain an API authorization key, known as an `access_token`. This token is provided by the owner-api in exchange for a valid username and password of a Tesla owner account, and is used in every command sent to Tesla's vehicle network. To obtain an access_token, Tythla's GUI will offer this as an option (to "log in") in the GUI's main menu.

After obtaining an access_token, Tythla might ask for permission to save the access token locally in a plaintext file -- this way, the token isn't unnecessarily pasted into the command-line for every subsequent command sent to a vehicle.

### 2. Selecting a vehicle
Next, to make a specific car do a specific thing, one needs to specify which vehicle they're trying to command. After automatically obtaining a list of vehicles in the Tesla owner's garage from the API, Tythla's GUI will require users to select a default vehicle in the GUI to send commands to.

### 3. Submitting commands / obtaining vitals
Now that there exists a valid `access_token` and a `vehicle_id` that can be sent commands, the user can get information about a car or submit commands to it. If the vehicle isn't awake, Tythla will ask the user if they want to wake the car or not. Either way, the last valid timestamp for the reuqested command or vitals info will be displayed to the user.

# Credit
Most, if not all, of the API information used to create this tool will be from the unofficial API sources for Tesla's Owner API. These include:
["Tesla API" by Joe Blau](https://www.teslaapi.io/), and [this other source](https://tesla-api.timdorr.com/), who's credited name I couldn't find. 
