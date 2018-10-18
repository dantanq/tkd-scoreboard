"""
TaeKwonDo Sparring Scoring App

Author: Danica Tanquilut
Last Modified: October 2018
"""

try:
	import serial
	import serial.tools.list_ports
except:
	print("Cannot Import Serial")
try:
    # for Python3
	import tkinter as tk
	from tkinter import *
	from tkinter.ttk import Frame, Style, Button, Label, Entry, Checkbutton, OptionMenu
except ImportError:
	# for Python2
	import Tkinter as tk
	from Tkinter import *
	from ttk import Frame, Style, Button, Label, Entry, Checkbutton, OptionMenu
import time

class Control(Frame):

	def __init__(self):
		# initialize RED and BLUE fighters
		self.RED = 0
		self.BLUE = 1

		# initialize score and kyonggo variables
		self.redPoints = 0
		self.bluePoints = 0
		self.redKyonggo = 0
		self.blueKyonggo = 0
		self.currentRound = 0
		self.display = None
		self.miniDisplay = None
		self.numRounds = 0
		self.timer = None
		self.isSuddenDeath = False
		self.callNextRound = True
		try:
			# for Python3
			super().__init__()
		except:
			# for Python2
			Frame.__init__(self)

		# set title and default style
		self.master.title("TKD Scoring System")
		# create style
		self.s = Style()
		self.s.configure("TButton", padding=10, font=(None, 20))
		self.s.configure("TCheckbutton", padding=10, font=(None, 20))
		self.s.configure("TOptionMenu", padding=10, font=(None, 20))
		self.pack(fill=BOTH, expand=True)
		# create setup frames, labels, and entries
		# time entry frame
		self.setTimeFrame = Frame(self)
		self.timerLabel = Label(self.setTimeFrame, text="Time:", font=(None, 20))
		self.secondsEntry = Entry(self.setTimeFrame, width=3, font=(None, 20))
		self.colonLabel = Label(self.setTimeFrame, text=":", font=(None, 20))
		self.minuteEntry = Entry(self.setTimeFrame, width=3, font=(None, 20))
		# round entry frame
		self.roundsFrame = Frame(self)
		self.roundsLabel = Label(self.roundsFrame, text="Number of Rounds:", font=(None, 20))
		self.roundsEntry = Entry(self.roundsFrame, width=3, font=(None, 20))
		# serial entry frame
		self.serialFrame = Frame(self)
		try:
			self.arduino_ports = ["None"] + [
			    p.device
			    for p in serial.tools.list_ports.comports()
			]
		except:
			# if serial is not installed
			self.arduino_ports = ["None"]
		self.serialEntry = StringVar()
		self.serialEntry.set("None")
		self.serialLabel = Label(self.serialFrame, text="Serial Input:", font=(None, 20))
		self.serialCheck = OptionMenu(self.serialFrame, self.serialEntry, "None", *self.arduino_ports)
		self.createMatchButton = Button(self, text="Create Match", style="TButton",
			command = self.hideSetup)

		# initialize frames for UI
		# red frame and buttons
		self.redFrame = Frame(self)
		self.redScoreButton = Button(self.redFrame, text="Red +", style="TButton",
			command = lambda: self.incrementPoints(self.RED))
		self.redDeletePoint = Button(self.redFrame, text="Red -", style="TButton",
			command = lambda: self.deductPoints(self.RED))
		self.redKyonggoButton = Button(self.redFrame, text="Kyonggo +", style="TButton",
			command = lambda: self.callKyonggo(self.RED))
		self.redKyonggoDelete = Button(self.redFrame, text="Kyonggo -", style="TButton",
			command = lambda: self.deductKyonggo(self.RED))
		# blue frame and buttons
		self.blueFrame = Frame(self)
		self.blueScoreButton = Button(self.blueFrame, text="Blue +", style="TButton",
			command = lambda: self.incrementPoints(self.BLUE))
		self.blueDeletePoint = Button(self.blueFrame, text="Blue -", style="TButton",
			command = lambda:self.deductPoints(self.BLUE))
		self.blueKyonggoButton = Button(self.blueFrame, text="Kyonggo +", style="TButton",
			command = lambda: self.callKyonggo(self.BLUE))
		self.blueKyonggoDelete = Button(self.blueFrame, text="Kyonggo -", style="TButton",
			command = lambda: self.deductKyonggo(self.BLUE))
		# reset and new match frame and buttons
		self.resetFrame = Frame(self)
		self.startStop = StringVar()
		self.timerStartStop = Button(self.resetFrame, textvariable=self.startStop, style="TButton",
			command=self.timerPush)
		self.startStop.set("Start Round 1")
		self.newMatch = Button(self.resetFrame, text="New Match", style="TButton",
			command = self.newMatch)
		self.resetMatch = Button(self.resetFrame, text="Reset Match", style="TButton",
			command = self.resetMatch)

		self.setup()		
	
	# displays setup frames
	def setup(self):
		# timer frame
		self.setTimeFrame.pack(fill=X)
		# timer label and entry
		self.timerLabel.pack(side=LEFT, padx=5, pady=5)
		self.secondsEntry.pack(side=RIGHT)
		self.colonLabel.pack(side=RIGHT)
		self.minuteEntry.pack(side=RIGHT)

		# frame for number of rounds
		self.roundsFrame.pack(fill=X)
		# number of rounds label and entry
		self.roundsLabel.pack(side=LEFT, padx=5, pady=5)
		self.roundsEntry.pack(side=RIGHT)

		# frame for serial entry
		self.serialFrame.pack(fill=X, expand=True)
		# serial entry label and checkbox
		self.serialLabel.pack(side=LEFT, padx=5, pady=5)
		self.serialCheck.pack(side=RIGHT)

		# create match button
		self.createMatchButton.pack(side=BOTTOM)

	# hides setup widgets and initalizes timer and number of rounds
	def hideSetup(self):
		# check if minutes, seconds, and round entries are valid
		if len(self.minuteEntry.get()) < 1:
			minutes = 0
		else:
			try:
				minutes = int(self.minuteEntry.get())
			except:
				minutes = 0
		if len(self.secondsEntry.get()) < 1:
			seconds = 0
		else:
			try:
				seconds = int(self.secondsEntry.get()) % 60
				minutes += int(self.secondsEntry.get()) // 60
			except:
				seconds = 0
		if len(self.roundsEntry.get()) < 1:
			numRounds = 0
		else:
			try:
				numRounds = int(self.roundsEntry.get())
			except:
				numRounds = 0
		# set up serial input if checked
		if self.serialEntry.get() != "None":
			self.serialSetup()
		else:
			self.arduino = False
		# only moves on if entries are valid
		if ((minutes != 0) or (seconds != 0)) and (numRounds != 0):
			self.roundLength = [minutes, seconds]
			self.timer = Timer(self.roundLength)
			self.numRounds = numRounds
			self.currentRound = 1
			self.isSuddenDeath = False
			self.roundsFrame.pack_forget()
			self.setTimeFrame.pack_forget()
			self.createMatchButton.pack_forget()
			self.serialFrame.pack_forget()
			self.initUI()

	# set up serial input
	def serialSetup(self):
		try:
			self.arduino = True
			self.serialPort = self.serialEntry.get()
			self.baudRate = 9600
			self.ser = serial.Serial(self.serialPort, self.baudRate, timeout=0, writeTimeout=0)
			self.ser.flushInput()
		except:
			self.arduino = False
			print("Could Not Complete Serial Port Set Up")

	# creates user interface
	def initUI(self):
		# create display
		if self.display == None:
			self.display = Display(self.timer)
			self.display.attributes('-fullscreen', True)
		else:
			self.display.newTimer(self.timer)
			self.display.updateCurrentRound("R1")
		if self.miniDisplay == None:
			self.miniDisplay = miniDisplay(self.timer)
		else:
			self.miniDisplay.newTimer(self.timer)
			self.miniDisplay.updateCurrentRound("R1")

		# red point and kyonggo buttons
		self.redFrame.pack(fill=BOTH, side=LEFT)
		self.redScoreButton.pack(padx=5, pady=5, fill=X)
		self.redDeletePoint.pack(padx=5, pady=5, fill=X)
		self.redKyonggoButton.pack(padx=5, pady=5, fill=X)
		self.redKyonggoDelete.pack(padx=5, pady=5, fill=X)

		# blue point and kyonggo buttons
		self.blueFrame.pack(fill=BOTH, side=RIGHT)
		self.blueScoreButton.pack(padx=5, pady=5, fill=X)
		self.blueDeletePoint.pack(padx=5, pady=5, fill=X)
		self.blueKyonggoButton.pack(padx=5, pady=5, fill=X)
		self.blueKyonggoDelete.pack(padx=5, pady=5, fill=X)

		# timer start/stop button, reset button, and quit button
		self.resetFrame.pack(side=BOTTOM)
		self.startStop.set("Start Round " + str(self.currentRound))
		self.timerStartStop.pack(side=TOP, pady=5)
		self.newMatch.pack(side=LEFT, padx=5)
		self.resetMatch.pack(side=RIGHT, padx=5)

	def timerPush(self):
		# if round is over, reset time give option to start next round
		if self.timer.timeLeft[0] == self.timer.timeLeft[1] == 0:
			self.timer.reset()
			self.startStop.set("Start Round " + str(self.currentRound))
			self.display.updateCurrentRound("R" + str(self.currentRound))
			self.miniDisplay.updateCurrentRound("R" + str(self.currentRound))
			self.updateDisplayTimer()		
		# pause timer, give option to unpause
		elif self.timer.isRunning():
			self.timer.stop()
			self.startStop.set("Start")
		# unpause timer, give option to pause
		else:
			if self.arduino:
				self.ser.flushInput()
			self.timer.start()
			if self.arduino:
				self.readSerialInput()
			self.startStop.set("Pause")
			if not self.callNextRound:
				self.callNextRound = True
			self.updateDisplayTimer()

	def resetMatch(self):
		if not self.timer.isRunning():
			self.timer.reset()
			self.redPoints = 0
			self.bluePoints = 0
			self.redKyonggo = 0
			self.blueKyonggo = 0
			self.currentRound = 1
			if self.isSuddenDeath:
				self.isSuddenDeath = False
				self.newMatch.pack_forget()
				self.resetMatch.pack_forget()
				self.timerStartStop.pack(side=TOP, pady=5)
				self.newMatch.pack(side=LEFT, padx=5)
				self.resetMatch.pack(side=RIGHT, padx=5)
			self.startStop.set("Start Round 1")
			self.display.reset(self.timer.getTimeString())
			self.miniDisplay.reset(self.timer.getTimeString())

	def updateDisplayTimer(self):
		if self.timer.isElapsed():
			self.timer.stop()
			if self.callNextRound:
				self.nextRound()
			self.display.updateTimer(self.timer.getTimeString())
			self.miniDisplay.updateTimer(self.timer.getTimeString())
		elif self.currentRound > self.numRounds:
			self.suddenDeath()
		else:
			self.display.updateTimer(self.timer.getTimeString())
			self.miniDisplay.updateTimer(self.timer.getTimeString())
			self.after(1000, self.updateDisplayTimer)		

	def nextRound(self):
		self.callNextRound = False
		self.currentRound += 1
		if self.currentRound <= self.numRounds:
			self.startStop.set("Reset Timer")
		else:
			self.startStop.set("Sudden Death")

	def suddenDeath(self):
		self.redPoints = 0
		self.display.updateRedPoints(0)
		self.miniDisplay.updateRedPoints(0)
		self.bluePoints = 0
		self.display.updateBluePoints(0)
		self.miniDisplay.updateBluePoints(0)
		self.display.updateTimer("SUDDEN DEATH")
		self.miniDisplay.updateTimer("SUDDEN DEATH")
		self.display.updateCurrentRound("")
		self.miniDisplay.updateCurrentRound("")
		self.isSuddenDeath = True
		if self.arduino:
			self.readSerialInput()
		self.timerStartStop.pack_forget()

	def readSerialInput(self):
		if self.timer.isRunning() or self.isSuddenDeath:
			output = self.ser.readline()
			if len(output) != 0:
				try:
					fighter = int(output)
					self.incrementPoints(fighter)
				except:
					print("Invalid Serial Input")
			self.after(500, self.readSerialInput)

	def incrementPoints(self, fighter):
		if fighter == self.RED:
			self.redPoints += 1
			self.display.updateRedPoints(self.redPoints)
			self.miniDisplay.updateRedPoints(self.redPoints)
		elif fighter == self.BLUE:
			self.bluePoints += 1
			self.display.updateBluePoints(self.bluePoints)
			self.miniDisplay.updateBluePoints(self.bluePoints)

	def deductPoints(self, fighter):
		if fighter == self.RED and self.redPoints > 0:
			self.redPoints -= 1
			self.display.updateRedPoints(self.redPoints)
			self.miniDisplay.updateRedPoints(self.redPoints)
		elif fighter == self.BLUE and self.bluePoints > 0:
			self.bluePoints -= 1
			self.display.updateBluePoints(self.bluePoints)
			self.miniDisplay.updateBluePoints(self.bluePoints)

	def callKyonggo(self, fighter):
		# Noah said these point deductions are correct
		if fighter == self.RED:
			self.redKyonggo += 1
			self.display.updateRedKyonggo("Kyonggo: " + str(self.redKyonggo))
			self.miniDisplay.updateRedKyonggo("Kyonggo: " + str(self.redKyonggo))
			if self.redKyonggo % 2 == 0 and self.redPoints > 0:
				self.redPoints -= 1
				self.display.updateRedPoints(self.redPoints)
				self.miniDisplay.updateRedPoints(self.redPoints)
		elif fighter == self.BLUE:
			self.blueKyonggo += 1
			self.display.updateBlueKyonggo("Kyonggo: " + str(self.blueKyonggo))
			self.miniDisplay.updateBlueKyonggo("Kyonggo: " + str(self.blueKyonggo))
			if self.blueKyonggo % 2 == 0 and self.bluePoints > 0:
				self.bluePoints -= 1
				self.display.updateBluePoints(self.bluePoints)
				self.miniDisplay.updateBluePoints(self.bluePoints)

	def deductKyonggo(self, fighter):
		if fighter == self.RED and self.redKyonggo > 0:
			self.redKyonggo -= 1
			self.display.updateRedKyonggo("Kyonggo: " + str(self.redKyonggo))
			self.miniDisplay.updateRedKyonggo("Kyonggo: " + str(self.redKyonggo))
			if self.redKyonggo % 2 == 1:
				self.redPoints += 1
				self.display.updateRedPoints(self.redPoints)
				self.miniDisplay.updateRedPoints(self.redPoints)
		elif fighter == self.BLUE and self.blueKyonggo > 0:
			self.blueKyonggo -= 1
			self.display.updateBlueKyonggo("Kyonggo: " + str(self.blueKyonggo))
			self.miniDisplay.updateBlueKyonggo("Kyonggo: " + str(self.blueKyonggo))
			if self.blueKyonggo % 2 == 1:
				self.bluePoints += 1
				self.display.updateBluePoints(self.bluePoints)			
				self.miniDisplay.updateBluePoints(self.bluePoints)			

	def newMatch(self):
		if not self.timer.isRunning():
			self.redPoints = 0
			self.redKyonggo = 0
			self.bluePoints = 0
			self.blueKyonggo = 0
			self.display.reset("0:00")
			self.miniDisplay.reset("0:00")
			self.hideUI()
			self.setup()

	def hideUI(self):
		self.redFrame.pack_forget()
		self.blueFrame.pack_forget()
		self.resetFrame.pack_forget()

class Timer(Frame):

	def __init__(self, inputTime):
		# time is represented as an array of [minutes, seconds]
		try:
			# Python3
			super().__init__()
		except:
			# Python2
			Frame.__init__(self)
		self.timeLeft = inputTime
		self.totalTime = [inputTime[0], inputTime[1]]
		self.running = False
		self.pattern = '{0:02d}:{1:02d}'
		self.elapsed = False
		self.delay = time.time()

	# returns string of time for setting string var
	def getTimeString(self):
		return self.pattern.format(self.timeLeft[0], self.timeLeft[1])

	# returns status of timer
	def isRunning(self):
		return self.running

	def start(self):
		self.running = True
		# delay to ensure updateTime is only called when needed
		if (time.time() - self.delay > 1.5):
				self.updateTime()
				self.delay = time.time()

	def stop(self):
		if self.running:
			self.running = False

	def reset(self):
		self.timeLeft = [self.totalTime[0], self.totalTime[1]]
		self.running = False
		self.elapsed = False

	def isElapsed(self):
		return self.elapsed

	def updateTime(self):
		# if time has elapsed, set running to False
		if self.running:
			# decrease seconds by 1
			if self.timeLeft[1] > 0:
				self.timeLeft[1] -= 1
			# set seconds to 59 and decrease minutes by 1
			elif self.timeLeft[0] > 0:
				self.timeLeft[1] = 59
				self.timeLeft[0] -= 1
			if self.timeLeft[0] == self.timeLeft[1] == 0:
				self.running = False
				self.elapsed = True
			else:
				self.after(1000, self.updateTime)

class Display(Toplevel):

	def __init__(self, timer):
		try:
			# Python3
			super().__init__()
		except:
			# Python2
			Toplevel.__init__(self)
		# initialize score string variables
		self.timer = timer
		self.redScore = StringVar()
		self.blueScore = StringVar()
		self.timeString = StringVar()
		self.redKyonggo = StringVar()
		self.blueKyonggo = StringVar()
		self.currentRound = StringVar()

		# create styles to set background colors
		self.style = Style()
		self.style.configure("red.TLabelframe", background="Red")
		self.style.configure("blue.TLabelframe", background="Blue")
		self.style.configure("black.TLabelframe", background="Black")

		# initialize and pack frame and label for timer
		self.timerFrame = Frame(self, style="black.TLabelframe", borderwidth=0)
		self.timerFrame.pack(side=TOP, fill=X, expand=True)
		self.roundLabel = tk.Label(self.timerFrame, textvariable=self.currentRound,
			font=(None, 70), fg="WHITE", bg="BLACK")
		self.currentRound.set("R1")
		self.roundLabel.pack(side=RIGHT, fill=Y, anchor=S)
		self.timerLabel = tk.Label(self.timerFrame, textvariable=self.timeString,
			font=(None, 160), fg="WHITE", bg="BLACK")
		self.timeString.set(self.timer.getTimeString())
		self.timerLabel.pack(side=BOTTOM, fill=X, expand=True)

		# initialize and pack frames for red and blue
		self.redFrame = Frame(self, style="red.TLabelframe", borderwidth=0)
		self.redFrame.pack(side=LEFT, fill=BOTH, expand=True)
		self.blueFrame = Frame(self, style="blue.TLabelframe", borderwidth=0)
		self.blueFrame.pack(side=RIGHT, fill=BOTH, expand=True)

		# initialize and pack kyonggo labels
		self.redKyonggoLabel = tk.Label(self.redFrame, textvariable=self.redKyonggo,
			font=(None, 50), bg="RED", anchor=W)
		self.redKyonggoLabel.pack(side=BOTTOM, fill=X, expand=True)
		self.redKyonggo.set("Kyonggo: 0")
		self.blueKyonggoLabel = tk.Label(self.blueFrame, textvariable=self.blueKyonggo,
			font=(None, 50), bg="BLUE", anchor=E)
		self.blueKyonggoLabel.pack(side=BOTTOM, fill=X, expand=True)
		self.blueKyonggo.set("Kyonggo: 0")

		# initialize and pack score labels using string variables
		self.redScoreLabel = tk.Label(self.redFrame, textvariable=self.redScore, 
			font=(None, 740), bg="RED")
		self.redScoreLabel.pack(side=TOP, fill=X, expand=True)
		self.redScore.set("0")
		self.blueScoreLabel = tk.Label(self.blueFrame, textvariable=self.blueScore, 
			font=(None, 740), bg="BLUE")
		self.blueScoreLabel.pack(side=TOP, fill=X, expand=True)
		self.blueScore.set("0")

	def updateRedPoints(self, points):
		self.redScore.set(str(points))

	def updateBluePoints(self, points):
		self.blueScore.set(str(points))

	def updateTimer(self, time):
		self.timeString.set(time)

	def updateRedKyonggo(self, kyonggo):
		self.redKyonggo.set(str(kyonggo))

	def updateBlueKyonggo(self, kyonggo):
		self.blueKyonggo.set(str(kyonggo))

	def updateCurrentRound(self, round):
		self.currentRound.set(round)

	def newTimer(self, timer):
		self.timer = timer
		self.timeString.set(self.timer.getTimeString())

	def reset(self, time):
		self.updateRedPoints(0)
		self.updateBluePoints(0)
		self.updateTimer(time)
		self.updateRedKyonggo("Kyonggo: 0")
		self.updateBlueKyonggo("Kyonggo: 0")
		self.updateCurrentRound("R1")
	
class miniDisplay(Display):

	def __init__(self, timer):
		try:
			# Python3
			super().__init__(timer)
		except:
			# Python2
			Display.__init__(self, timer)
		self.timerLabel['font'] = (None, 50)
		self.redScoreLabel['font'] = (None, 50)
		self.blueScoreLabel['font'] = (None, 50)
		self.redKyonggoLabel['font'] = (None, 15)
		self.blueKyonggoLabel['font'] = (None, 15)
		self.roundLabel['font'] = (None, 20)

	def updateTimer(self, time):
		if time == "SUDDEN DEATH":
			self.timerLabel['font'] = (None, 25)
		else:
			self.timerLabel['font'] = (None, 50)
		self.timeString.set(time)

def main():
	root = Tk()
	app = Control()
	root.mainloop()

if __name__ == '__main__':
	main()
