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
