# tkd-scoreboard
A Taekwondo scoring application. Creates a fullscreen display of score, timer, and kyonggo as well as a mini display and controller. Can accept serial input from three corner judges via arduino controller.
## Installation
The easiest way to install is cloning the repo directly.
```
# clone repo
git clone https://github.com/dantanq/tkd-scoreboard
```
tkd-scoreboard can be run in Python 2 or Python 3. It is recommended you run the application in a virtual environment to avoid dependency issues with other projects.
```
# create virtual environment in tkd-scoreboard directory
python -m venv ~/tkd-scoreboard
# navigate to directory if not there already
cd ~/tkd-scoreboard
# activate virtual environment
source bin/activate
```
To exit the virtual environment, simply run
```
deactivate
```
The application uses [pySerial](https://github.com/pyserial/pyserial) to read the arduino's serial output. If you plan on using an arduino to accept input from corner judges, pySerial is required. To install (while in virtual environment, if applicable), run:
```
python -m pip install pyserial
```
## Usage
To open the application, run:
```
python display.py
```
This opens the application to the screen:

![createMatch](/screenshots/create-match.png)

Here, the user inputs the length of each round (in the format MIN:SEC), the number of rounds per match, and select the serial port to be used. (Simply select "None" if you will only be using the computer interface). Creating a match then opens the fullscreen display (usually to be shown on a separate monitor facing the ring). The display shows the points and kyonggo for each fighter, a timer, and the current round.

![fullscreen](/screenshots/fullscreen-display.png)

Creating a match also opens the controller, which can be used to manually award/deduct points or kyonggo for each fighter and start/pause the application's timer. At the end of each round, the timer can be reset and the next round can be started using the start/pause button. At the conclusion of the match (when the pre-determined number of rounds have elapsed), the start/pause button can be used to enable Sudden Death if necessary. During Sudden Death, the timer is deactivated.

![controller](/screenshots/computer-interface.png)

Additionally, the "Reset Match" button can be used to start a new match with the same time limit and number of rounds, while the "New Match" button can be used to create a new match with different time and round constraints by bringing the user back to the Create Match screen.

A miniature display mirroring the fullscreen display (to be used by the side-by-side with the controller) is also opened when a match is created. Similarly to the fullscreen display, it shows the points and kyonggo for each fighter, a timer, and the current round.

![miniDisplay](/screenshots/minidisplay.png)
