import sys
# import os
# import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from pyfirmata2 import Arduino  # import library from pyfirmata2 to detect Arduino
import time  # time library to be able setup lenght of led lighting
import numpy as np
import pickle
from datetime import date
import webbrowser
import matplotlib.pylab as plt
import matplotlib.animation as animation
import matplotlib.figure as mpl_fig
from matplotlib.backends.backend_qt5agg import FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import serial

from ui_main import *
from Login import *
from save_load import *
from Marker import *


############################################################    Logic and UI
board = None
DeviceConnected = None
SensorConnected = None
SensorDeviceAddr = None

def DeviceInit():
    global board
    global sensor_board
    global DeviceConnected
    global SensorConnected
    global SensorDeviceAddr
    ports = list(serial.tools.list_ports.comports())
    for p in ports[1:]:
        # try:
            serialPort = serial.Serial(p.device, 9600, timeout=2)
            if len(serialPort.readline()) != 0:
                sensor_board = Arduino(p.device)
                SensorConnected = True
                SensorDeviceAddr = p.device
                print("Sensor")
            else:
                board = Arduino(p.device)
                DeviceConnected = True
                print("Ofalctometer")
        # except:
        #     pass

DeviceInit()

#### َQTFiles
qtcreator_file = "ui_main.ui"
qtlogin_file = "Login.ui"
qtsaveload_file = "save_load.ui"
qtmarker_file = "Marker.ui"

# Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)
# Ui_LoginWindow, QtBaseClass2 = uic.loadUiType(qtlogin_file)
# Ui_SaveLoad, QtBaseClass3 = uic.loadUiType(qtsaveload_file)
# Ui_Marker, QtBaseClass4 = uic.loadUiType(qtmarker_file)


UserManualURL = "http://ee.sharif.ir/~airlab/BioarmaUserManual.pdf"
Valve_times = ([0, 0, 0, 0, 0, ])
Rest_times = ([0, 0, 0, 0, 0, 0])
Priorities = [0, 0, 0, 0, 0, 0]
FirstRest = 0
Stop = False
DialText = ''
DialText2 = ''
DialText1 = ''
Login = True
Worker_always_on = True
LastRestValve = "Valve1"
TaskList = []
TaskListTab1 = []
Rest_Time = 0
Shir_Time = 0
RestValve = 0
RepeatTimes = 0
Rest_TimeTab1 = 0
Shir_TimeTab1 = 0
RestValveTab1 = 0
RepeatTimesNumberTab3 = 1
RepeatTimesTab1 = 0
Tab1_TimeLine = []
Valve1_Marker = False
Valve2_Marker = False
Valve3_Marker = False
Valve4_Marker = False
Valve5_Marker = False
Valve6_Marker = False
BOT_Marker = True
LoadBool = False
SubjectName = "Subject1"
Valves_list_Tab3 = ["Valve2", "Valve3", "Valve4", "Valve5", "Valve6"]
V1S = 0
V2S = 0
V3S = 0
V4S = 0
V5S = 0
V6S = 0
MS = 0

def TurnValvesOnOff(valve, Shir_Time):
    global board
    global Valve1_Marker, Valve2_Marker, Valve3_Marker, Valve4_Marker, Valve5_Marker, Valve6_Marker
    global V1S, V2S, V3S, V4S, V5S, V6S, MS
    LedPin = 6
    try:

        if valve == "Marker":
            MS = 1
            board.digital[LedPin].write(1)
            ValvesStatus()
            time.sleep(Shir_Time)
            board.digital[LedPin].write(1)
            MS = 0
            ValvesStatus()

        if valve == "Valve1" or valve == "Valve 1":
            V1S = 1
            board.digital[8].write(1)
            if Valve1_Marker:
                MS = 1
                board.digital[LedPin].write(1)
            ValvesStatus()
            time.sleep(Shir_Time)
            board.digital[8].write(0)
            board.digital[LedPin].write(0)
            V1S = 0
            MS = 0
            ValvesStatus()

        if valve == "Valve2" or valve == "Valve 2":
            V2S = 1
            board.digital[9].write(1)
            if Valve2_Marker:
                MS = 1
                board.digital[LedPin].write(1)
            ValvesStatus()
            time.sleep(Shir_Time)
            board.digital[9].write(0)
            board.digital[LedPin].write(0)
            V2S = 0
            MS = 0
            ValvesStatus()

        if valve == "Valve3" or valve == "Valve 3":
            V3S = 1
            board.digital[10].write(1)
            if Valve3_Marker:
                MS = 1
                board.digital[LedPin].write(1)
            ValvesStatus()
            time.sleep(Shir_Time)
            board.digital[10].write(0)
            board.digital[LedPin].write(0)
            V3S = 0
            MS = 0
            ValvesStatus()

        if valve == "Valve4" or valve == "Valve 4":
            V4S = 1
            board.digital[11].write(1)
            if Valve4_Marker:
                MS = 1
                board.digital[LedPin].write(1)
            ValvesStatus()
            time.sleep(Shir_Time)
            board.digital[11].write(0)
            board.digital[LedPin].write(0)
            V4S = 0
            MS = 0
            ValvesStatus()

        if valve == "Valve5" or valve == "Valve 5":
            V5S = 1
            board.digital[12].write(1)
            if Valve5_Marker:
                MS = 1
                board.digital[LedPin].write(1)
            ValvesStatus()
            time.sleep(Shir_Time)
            board.digital[12].write(0)
            board.digital[LedPin].write(0)
            V5S = 0
            MS = 0
            ValvesStatus()

        if valve == "Valve6" or valve == "Valve 6":
            V6S = 1
            board.digital[7].write(1)
            if Valve6_Marker:
                MS = 1
                board.digital[LedPin].write(1)
            ValvesStatus()
            time.sleep(Shir_Time)
            board.digital[7].write(0)
            board.digital[LedPin].write(0)
            V6S = 0
            MS = 0
            ValvesStatus()


    except:
        board = None

def UserValidate(name, passwoed):
    if name == "Admin" and passwoed == "Admin":
        return True
    else:
        return False

def TurnAllOff():
    if board == None:
        DeviceInit()
    try:
        for i in [6, 7, 8, 9, 10, 11, 12]:
            board.digital[i].write(0)
    except:
        MyWindow.DeviceError(window)

def ValvesStatus():
    global V1S, V2S, V3S, V4S, V5S, V6S, MS
    OFF = "off"
    ON = "ON"
    if (1):

        if V1S == 0:
            window.V1S.setText(OFF)
            window.V1S_2.setText(OFF)
            window.V1S_3.setText(OFF)


        else:
            window.V1S.setText(ON)
            window.V1S_2.setText(ON)
            window.V1S_3.setText(ON)

        if V2S == 0:
            window.V2S.setText(OFF)
            window.V2S_2.setText(OFF)
            window.V2S_3.setText(OFF)


        else:
            window.V2S.setText(ON)
            window.V2S_2.setText(ON)
            window.V2S_3.setText(ON)

        if V3S == 0:
            window.V3S.setText(OFF)
            window.V3S_2.setText(OFF)
            window.V3S_3.setText(OFF)


        else:
            window.V3S.setText(ON)
            window.V3S_2.setText(ON)
            window.V3S_3.setText(ON)

        if V4S == 0:
            window.V4S.setText(OFF)
            window.V4S_2.setText(OFF)
            window.V4S_3.setText(OFF)


        else:
            window.V4S.setText(ON)
            window.V4S_2.setText(ON)
            window.V4S_3.setText(ON)

        if V5S == 0:
            window.V5S.setText(OFF)
            window.V5S_2.setText(OFF)
            window.V5S_3.setText(OFF)


        else:
            window.V5S.setText(ON)
            window.V5S_2.setText(ON)
            window.V5S_3.setText(ON)

        if V6S == 0:
            window.V6S.setText(OFF)
            window.V6S_2.setText(OFF)
            window.V6S_3.setText(OFF)

        else:
            window.V6S.setText(ON)
            window.V6S_2.setText(ON)
            window.V6S_3.setText(ON)

        if MS == 0:
            window.MS.setText(OFF)
            window.MS_2.setText(OFF)
            window.MS_3.setText(OFF)


        else:
            window.MS.setText(ON)
            window.MS_2.setText(ON)
            window.MS_3.setText(ON)
class Timer(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def Timing1(self):
        global DialText1, TaskListTab1, Rest_TimeTab1, Shir_TimeTab1, RestValveTab1, RepeatTimesTab1, Stop
        NumberOfRests = TaskListTab1.count("Rest")
        NumberOfValves = len(TaskListTab1) - NumberOfRests
        Total_Time = RepeatTimesTab1 * (NumberOfRests * Rest_TimeTab1 + NumberOfValves * Shir_TimeTab1)

        for i in range(int(Total_Time)):
            if Stop:
                break
            window.TimePassed.display(i)
            window.TimeLeft.display(Total_Time - i)
            time.sleep(1)
        if Stop == False:
            window.TimePassed.display(Total_Time)
            window.TimeLeft.display(0)

        self.finished.emit()

    def Timing2(self):
        global DialText2, TaskList, Rest_Time, Shir_Time, RestValve, RepeatTimes, Stop
        NumberOfRests = TaskList.count("Rest")
        NumberOfValves = len(TaskList) - NumberOfRests
        Total_Time = RepeatTimes * (NumberOfRests * Rest_Time + NumberOfValves * Shir_Time)

        for i in range(int(Total_Time)):
            if Stop:
                break
            window.TimePassed_Tab2.display(i)
            window.TimeLeft_Tab2.display(Total_Time - i)
            time.sleep(1)
        if Stop == False:
            window.TimePassed_Tab2.display(Total_Time)
            window.TimeLeft_Tab2.display(0)

        self.finished.emit()

    def Timing3(self):
        global Valve_times, Rest_times, Priorities, FirstRest, Stop, RepeatTimesNumberTab3
        TotalTime = 0
        self.progress.emit(0)
        for priority in Priorities:
            if (priority[0] == 0):
                continue
            TotalTime = TotalTime + priority[1]
            TotalTime = TotalTime + priority[2]

        Total_Time = RepeatTimesNumberTab3 * TotalTime

        for i in range(int(Total_Time)):
            if Stop:
                break
            window.TimePassed_Tab3.display(i)
            window.TimeLeft_Tab3.display(Total_Time - i)
            time.sleep(1)
        if Stop == False:
            window.TimePassed_Tab3.display(Total_Time)
            window.TimeLeft_Tab3.display(0)

        self.finished.emit()

class MarkerThread(QObject):
    finished = pyqtSignal()

    def Marker(self):
        TurnValvesOnOff("Marker", 0.5)
        self.finished.emit()

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run1(self):
        TurnAllOff()
        self.progress.emit(0)
        global DialText1, TaskListTab1, Rest_TimeTab1, Shir_TimeTab1, RestValveTab1, RepeatTimesTab1, Stop
        NumberOfRests = TaskListTab1.count("Rest")
        NumberOfValves = len(TaskListTab1) - NumberOfRests
        Total_Time = RepeatTimesTab1 * (NumberOfRests * Rest_TimeTab1 + NumberOfValves * Shir_TimeTab1)
        Temp_Time = 0
        for i in range(RepeatTimesTab1):
            if (Stop == True):
                break
            for valve in TaskListTab1:
                if (Stop == True):
                    break
                if valve == "Rest":
                    TurnValvesOnOff(RestValveTab1, Rest_TimeTab1)
                    Temp_Time = Temp_Time + Rest_TimeTab1
                else:
                    TurnValvesOnOff(valve, Shir_TimeTab1)
                    Temp_Time = Temp_Time + Shir_TimeTab1
                self.progress.emit(int(Temp_Time / Total_Time * 100))
                if (Stop == True):
                    break
            if (Stop == True):
                break

        self.finished.emit()

    def run2(self):
        TurnAllOff()
        self.progress.emit(0)
        global DialText2, TaskList, Rest_Time, Shir_Time, RestValve, RepeatTimes, Stop
        NumberOfRests = TaskList.count("Rest")
        NumberOfValves = len(TaskList) - NumberOfRests
        Total_Time = RepeatTimes * (NumberOfRests * Rest_Time + NumberOfValves * Shir_Time)
        Temp_Time = 0
        for i in range(RepeatTimes):
            if (Stop == True):
                break
            for valve in TaskList:
                if (Stop == True):
                    break
                if valve == "Rest":
                    TurnValvesOnOff(RestValve, Rest_Time)
                    Temp_Time = Temp_Time + Rest_Time
                else:
                    TurnValvesOnOff(valve, Shir_Time)
                    Temp_Time = Temp_Time + Shir_Time
                self.progress.emit(int(Temp_Time / Total_Time * 100))
                if (Stop == True):
                    break
            if (Stop == True):
                break

        self.finished.emit()

    def run3(self):
        global Valve_times, Rest_times, Priorities, FirstRest, Stop, RepeatTimesNumberTab3
        Stop = False
        TurnAllOff()
        RestValve = window.RestValveTab3.currentText()
        Priorities.sort()
        TimePast = 0
        TotalTime = 0
        self.progress.emit(0)
        for priority in Priorities:
            if (priority[0] == 0):
                continue
            TotalTime = TotalTime + priority[1]
            TotalTime = TotalTime + priority[2]

        TotalTime = RepeatTimesNumberTab3 * TotalTime
        # first element is priority
        #   # second element is open time
        #   #   # third element is rest time
        #   #   #   # fourth third element is valve number
        for i in range(RepeatTimesNumberTab3):
            for priority in Priorities:
                if (priority[0] == 0):
                    continue
                if (Stop == True):
                    break
                    # First Rest
                if (priority[0] == -1):
                    TurnValvesOnOff(RestValve, priority[1])
                else:
                    TurnValvesOnOff(priority[3], priority[1])
                    TurnValvesOnOff(RestValve, priority[2])
                TimePast = TimePast + priority[2]
                TimePast = TimePast + priority[1]
                self.progress.emit(int(TimePast * 100 / TotalTime))

        self.finished.emit()

class SaveLoadWindow(QtWidgets.QMainWindow, Ui_SaveLoad):

    def __init__(self, parent=None):

        QtWidgets.QMainWindow.__init__(self)
        Ui_SaveLoad.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.size())
        global SubjectName
        self.Save_windowButt.clicked.connect(self.SaveFile)
        self.Load_windowButt.clicked.connect(self.LoadFile)
        self.SubjectName.textChanged.connect(self.UpdateSubjectName)
        temp = SubjectName
        self.SubjectName.clear()
        self.SubjectName.insertPlainText(temp)

    def UpdateSubjectName(self):
        global SubjectName
        SubjectName = self.SubjectName.toPlainText()

    def SaveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        global DialText, DialText2, DialText1, SubjectName
        SubjectName = self.SubjectName.toPlainText()
        today = date.today()
        today = today.strftime("%b-%d-%Y")
        try:
            fileName, _ = QFileDialog.getSaveFileName(self, "Save File", SubjectName + "-" + today + ".pkl",
                                                      "PKL Files (*.pkl)", options=options)
            self.Save(fileName, window)
            DialText = DialText + '\n' + "File saved successfully."
            DialText = DialText + '\n'
            window.Dialtxt.setText(DialText)

            DialText1 = DialText1 + '\n' + "File saved successfully."
            DialText1 = DialText1 + '\n'
            window.Dialtxt1.setText(DialText1)

            DialText2 = DialText2 + '\n' + "File saved successfully."
            DialText2 = DialText2 + '\n'
            window.Dialtxt2.setText(DialText2)

        except:
            DialText = DialText + '\n' + "Saving file failed."
            DialText = DialText + '\n'
            window.Dialtxt.setText(DialText)

            DialText1 = DialText1 + '\n' + "Saving file failed."
            DialText1 = DialText1 + '\n'
            window.Dialtxt1.setText(DialText1)

            DialText2 = DialText2 + '\n' + "Saving file failed."
            DialText2 = DialText2 + '\n'
            window.Dialtxt2.setText(DialText2)

    def LoadFile(self):
        global DialText, DialText2, DialText1
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        try:
            files, _ = QFileDialog.getOpenFileNames(self, "Load File", "", "PKL Files (*.pkl)", options=options)
            self.Load(files[-1], window)
            DialText = DialText + '\n' + "File loaded successfully."
            DialText = DialText + '\n'
            window.Dialtxt.setText(DialText)

            DialText1 = DialText1 + '\n' + "File loaded successfully."
            DialText1 = DialText1 + '\n'
            window.Dialtxt1.setText(DialText1)

            DialText2 = DialText2 + '\n' + "File loaded successfully."
            DialText2 = DialText2 + '\n'
            window.Dialtxt2.setText(DialText2)
        except:
            DialText = DialText + '\n' + "Loading file failed."
            DialText = DialText + '\n'
            window.Dialtxt.setText(DialText)

            DialText1 = DialText1 + '\n' + "Loading file failed."
            DialText1 = DialText1 + '\n'
            window.Dialtxt1.setText(DialText1)

            DialText2 = DialText2 + '\n' + "Loading file failed."
            DialText2 = DialText2 + '\n'
            window.Dialtxt2.setText(DialText2)

    def Save(self, path, window):
        global TaskListTab1, TaskList, Valve1_Marker, Valve2_Marker, Valve3_Marker, Valve4_Marker, Valve5_Marker, Valve6_Marker
        with open(path, 'wb') as f:  # Python 3: open(..., 'wb')
            # General
            pickle.dump(self.SubjectName.toPlainText(), f)
            pickle.dump(Valve1_Marker, f)
            pickle.dump(Valve2_Marker, f)
            pickle.dump(Valve3_Marker, f)
            pickle.dump(Valve4_Marker, f)
            pickle.dump(Valve5_Marker, f)
            pickle.dump(Valve6_Marker, f)
            # Tab1
            if 1:
                pickle.dump(TaskListTab1, f)
                pickle.dump(window.StandardProb.value(), f)
                pickle.dump(window.ValveM3Prob.value(), f)
                pickle.dump(window.ValveM4Prob.value(), f)
                pickle.dump(window.ValveM5Prob.value(), f)
                pickle.dump(window.ValveM6Prob.value(), f)
                pickle.dump(window.StandardValve.currentText(), f)
                pickle.dump(window.RestValveTab1.currentText(), f)
                pickle.dump(window.StimuliTime.value(), f)
                pickle.dump(window.RestTime.value(), f)
                pickle.dump(window.NumberOfTrials.value(), f)
            # Tab2
            if 1:
                pickle.dump(TaskList, f)
                pickle.dump(window.RestValveValue.currentText(), f)
                pickle.dump(window.RestTime_tab2.value(), f)
                pickle.dump(window.ShirTime_tab2.value(), f)
                pickle.dump(window.RepeatTimesNumber.value(), f)
            # Tab3
            if 1:
                pickle.dump(window.R0.value(), f)
                pickle.dump(window.V1.value(), f)
                pickle.dump(window.R1.value(), f)
                pickle.dump(window.V2.value(), f)
                pickle.dump(window.R2.value(), f)
                pickle.dump(window.V3.value(), f)
                pickle.dump(window.R3.value(), f)
                pickle.dump(window.V4.value(), f)
                pickle.dump(window.R4.value(), f)
                pickle.dump(window.V5.value(), f)
                pickle.dump(window.R5.value(), f)
                pickle.dump(window.PV1.value(), f)
                pickle.dump(window.PV2.value(), f)
                pickle.dump(window.PV3.value(), f)
                pickle.dump(window.PV4.value(), f)
                pickle.dump(window.PV5.value(), f)
                pickle.dump(window.RestValveTab3.currentText(), f)
                pickle.dump(window.RepeatTimesNumberTab3.value(), f)

    def Load(self, path, window):
        global Valve1_Marker, Valve2_Marker, Valve3_Marker, Valve4_Marker, Valve5_Marker, Valve6_Marker
        with open(path, 'rb') as f:  # Python 3: open(..., 'rb')
            # General
            window.listOrderTab1.clear()
            temp = pickle.load(f)
            self.SubjectName.clear()
            self.SubjectName.insertPlainText(temp)
            Valve1_Marker = pickle.load(f)
            Valve2_Marker = pickle.load(f)
            Valve3_Marker = pickle.load(f)
            Valve4_Marker = pickle.load(f)
            Valve5_Marker = pickle.load(f)
            Valve6_Marker = pickle.load(f)
            # Tab1
            if 1:
                TaskListTab1 = pickle.load(f)
                for text in TaskListTab1:
                    window.listOrderTab1.addItem(text)
                temp = pickle.load(f)
                window.StandardProb.setValue(temp)
                temp = pickle.load(f)
                window.ValveM3Prob.setValue(temp)
                temp = pickle.load(f)
                window.ValveM4Prob.setValue(temp)
                temp = pickle.load(f)
                window.ValveM5Prob.setValue(temp)
                temp = pickle.load(f)
                window.ValveM6Prob.setValue(temp)
                temp = pickle.load(f)
                window.StandardValve.setCurrentText(temp)
                temp = pickle.load(f)
                window.RestValveTab1.setCurrentText(temp)
                temp = pickle.load(f)
                window.StimuliTime.setValue(temp)
                temp = pickle.load(f)
                window.RestTime.setValue(temp)
                temp = pickle.load(f)
                window.NumberOfTrials.setValue(temp)
            # Tab2
            if 1:
                TaskList = pickle.load(f)
                for text in TaskList:
                    window.listOrder.addItem(text)
                temp = pickle.load(f)
                window.RestValveValue.setCurrentText(temp)
                temp = pickle.load(f)
                window.RestTime_tab2.setValue(temp)
                temp = pickle.load(f)
                window.ShirTime_tab2.setValue(temp)
                temp = pickle.load(f)
                window.RepeatTimesNumber.setValue(temp)
            # Tab3
            if 1:
                temp = pickle.load(f)
                window.R0.setValue(temp)
                temp = pickle.load(f)
                window.V1.setValue(temp)
                temp = pickle.load(f)
                window.R1.setValue(temp)
                temp = pickle.load(f)
                window.V2.setValue(temp)
                temp = pickle.load(f)
                window.R2.setValue(temp)
                temp = pickle.load(f)
                window.V3.setValue(temp)
                temp = pickle.load(f)
                window.R3.setValue(temp)
                temp = pickle.load(f)
                window.V4.setValue(temp)
                temp = pickle.load(f)
                window.R4.setValue(temp)
                temp = pickle.load(f)
                window.V5.setValue(temp)
                temp = pickle.load(f)
                window.R5.setValue(temp)
                temp = pickle.load(f)
                window.PV1.setValue(temp)
                temp = pickle.load(f)
                window.PV2.setValue(temp)
                temp = pickle.load(f)
                window.PV3.setValue(temp)
                temp = pickle.load(f)
                window.PV4.setValue(temp)
                temp = pickle.load(f)
                window.PV5.setValue(temp)
                temp = pickle.load(f)
                window.RestValveTab3.setCurrentText(temp)
                temp = pickle.load(f)
                window.RepeatTimesNumberTab3.setValue(temp)

class MarkerWindow(QtWidgets.QMainWindow, Ui_Marker):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        Ui_Marker.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.size())
        global Valve1_Marker, Valve2_Marker, Valve3_Marker, Valve4_Marker, Valve5_Marker, Valve6_Marker, BOT_Marker

        self.valve1.setChecked(Valve1_Marker)
        self.valve2.setChecked(Valve2_Marker)
        self.valve3.setChecked(Valve3_Marker)
        self.valve4.setChecked(Valve4_Marker)
        self.valve5.setChecked(Valve5_Marker)
        self.valve6.setChecked(Valve6_Marker)
        self.BOT.setChecked(BOT_Marker)

        self.valve1.stateChanged.connect(self.UpdateCheckBox)
        self.valve2.stateChanged.connect(self.UpdateCheckBox)
        self.valve3.stateChanged.connect(self.UpdateCheckBox)
        self.valve4.stateChanged.connect(self.UpdateCheckBox)
        self.valve5.stateChanged.connect(self.UpdateCheckBox)
        self.valve6.stateChanged.connect(self.UpdateCheckBox)
        self.BOT.stateChanged.connect(self.UpdateCheckBox)

    def UpdateCheckBox(self):
        global Valve1_Marker, Valve2_Marker, Valve3_Marker, Valve4_Marker, Valve5_Marker, Valve6_Marker, BOT_Marker
        Valve1_Marker = self.valve1.isChecked()
        Valve2_Marker = self.valve2.isChecked()
        Valve3_Marker = self.valve3.isChecked()
        Valve4_Marker = self.valve4.isChecked()
        Valve5_Marker = self.valve5.isChecked()
        Valve6_Marker = self.valve6.isChecked()
        BOT_Marker = self.BOT.isChecked()



class MyFigureCanvas(FigureCanvas, animation.FuncAnimation):

    def __init__(self, x_len, y_range, interval):
        FigureCanvas.__init__(self)
        super(MyFigureCanvas, self).__init__()
        super().__init__(mpl_fig.Figure())
        self.serialPort = serial.Serial(SensorDeviceAddr, 9600)
        self._x_len_ = x_len
        self._y_range_ = y_range

        x = list(range(0, x_len))
        y = [0] * x_len

        self._ax_  = self.figure.subplots()
        self._line_, = self._ax_.plot(x, y)
        self.dataTemp = 0
        animation.FuncAnimation.__init__(self, self.figure, self._update_canvas_, fargs=(x,y,), interval=interval, blit=True)
        return

    def current_milli_time(self):
        return round(time.time() * 1000)

    def _update_canvas_(self, i, x, y):

        try:
            dataRealTime = int(self.serialPort.readline())
            self.dataTemp = dataRealTime
        except:
            dataRealTime = self.dataTemp
        finally:
            timeNow = (self.current_milli_time())/1000

        y.append(dataRealTime) 
        x.append(timeNow)
        y = y[-self._x_len_:] 
        x = x[-self._x_len_:]  
        self._line_.set_ydata(y)
        LimitD = 10000
        self._ax_.set_ylim(dataRealTime-LimitD,dataRealTime+LimitD)
        return self._line_,
    
class LoginWindow(QtWidgets.QMainWindow, Ui_LoginWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        Ui_LoginWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.login.clicked.connect(self.UserLogin)
        self.login.setDisabled(False)

    def UserLogin(self):
        global Login
        global DialText, DialText1, DialText2
        Usrname = self.username.text()
        Pass = self.password.text()
        if UserValidate(Usrname, Pass):
            self.LoginStatus.setText("Acces Granted!")
            Login = True
            self.login.setDisabled(True)
            DialText = DialText + "Acces Granted!" + '\n'
            DialText1 = DialText1 + "Acces Granted!" + '\n'
            DialText2 = DialText2 + "Acces Granted!" + '\n'
        else:
            Login = False
            self.LoginStatus.setText("Acces Denied.")
            DialText = DialText + "Acces Denied." + '\n'
            DialText1 = DialText1 + "Acces Denied." + '\n'
            DialText2 = DialText2 + "Acces Denied." + '\n'

        MyWindow.LoginReport(window)

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        global Login
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.progressBar.setValue(0)
        self.progressBar_1.setValue(0)
        self.progressBar_2.setValue(0)
        self.start.clicked.connect(self.startall3)
        self.start2.clicked.connect(self.startall2)
        self.start1.clicked.connect(self.startall1)
        self.stop.clicked.connect(self.stop_all)
        self.stop1.clicked.connect(self.stop_all1)
        self.stop2.clicked.connect(self.stop_all2)
        self.saveload1.clicked.connect(self.SaveLoadWinodw)
        self.saveload2.clicked.connect(self.SaveLoadWinodw)
        self.saveload3.clicked.connect(self.SaveLoadWinodw)
        self.markertab1.clicked.connect(self.MarkerWindow)
        self.markertab2.clicked.connect(self.MarkerWindow)
        self.markertab3.clicked.connect(self.MarkerWindow)
        self.TimeLineGenarateTab1.clicked.connect(self.GenerateTimeLine)
        self.UserManualTab1.clicked.connect(self.OpenUserManualWeb)
        self.UserManualTab2.clicked.connect(self.OpenUserManualWeb)
        self.UserManualTab3.clicked.connect(self.OpenUserManualWeb)
        self.stop.setDisabled(True)
        self.stop2.setDisabled(True)
        self.stop1.setDisabled(True)

        #### Combobox change handler

        self.StandardValve.currentIndexChanged.connect(self.UpdateStandardandRestValve)
        self.RestValveTab1.currentIndexChanged.connect(self.UpdateStandardandRestValve)
        self.RestValveValue.currentIndexChanged.connect(self.UpdateRestValveValue)
        self.RestValveTab3.currentIndexChanged.connect(self.UpdateRestValveTab3)
        # self.ValvesStatusStart()
        print(DeviceConnected, SensorConnected)
        if DeviceConnected:
            self.olfactometer_check.setText("Connected")
        else:
            self.olfactometer_check.setText("Not Connected")
        if SensorConnected:

            self.SensorWindow()
            self.sensor_check.setText("Connected")
        else:
            self.olfactometer_check.setText("Not Connected")    

    def OpenUserManualWeb(self):
        global UserManualURL
        try:
            webbrowser.open(UserManualURL, new=0, autoraise=True)
        except:
            x = 1

    def UpdateRestValveTab3(self):
        global Valves_list_Tab3
        Valves_list_Tab3 = []
        Valves_list = ["Valve1", "Valve2", "Valve3", "Valve4", "Valve5", "Valve6"]
        for label in [self.label, self.label_2, self.label_3, self.label_6, self.label_5]:
            for valve in Valves_list:
                if (valve != self.RestValveTab3.currentText()):
                    if valve == "Valve1":
                        label.setText("Valve 1")
                    if valve == "Valve2":
                        label.setText("Valve 2")
                    if valve == "Valve3":
                        label.setText("Valve 3")
                    if valve == "Valve4":
                        label.setText("Valve 4")
                    if valve == "Valve5":
                        label.setText("Valve 5")
                    if valve == "Valve6":
                        label.setText("Valve 6")
                    Valves_list.remove(valve)
                    Valves_list_Tab3.append(valve)
                    break

    def UpdateStandardandRestValve(self):
        global DialText1
        Valves_list = ['Valve1', 'Valve2', 'Valve3', 'Valve4', 'Valve5', 'Valve6']
        if (self.RestValveTab1.currentText() == self.StandardValve.currentText()):
            self.StandardValve.setCurrentText('Valve1')
            self.RestValveTab1.setCurrentText('Valve2')
            DialText1 = DialText1 + '\n' + "Error: Standard Valve and Rest Valve can't be same."
            DialText1 = DialText1 + '\n'
            self.Dialtxt1.setText(DialText1)
        for label in [self.ValveM3, self.ValveM4, self.ValveM5, self.ValveM6]:
            for valve in Valves_list:
                if (valve != self.RestValveTab1.currentText() and valve != self.StandardValve.currentText()):
                    if valve == "Valve1":
                        label.setText("Valve 1 Probability")
                    if valve == "Valve2":
                        label.setText("Valve 2 Probability")
                    if valve == "Valve3":
                        label.setText("Valve 3 Probability")
                    if valve == "Valve4":
                        label.setText("Valve 4 Probability")
                    if valve == "Valve5":
                        label.setText("Valve 5 Probability")
                    if valve == "Valve6":
                        label.setText("Valve 6 Probability")
                    Valves_list.remove(valve)
                    break

    def UpdateRestValveValue(self):
        global LastRestValve
        RestValve = self.RestValveValue.currentText()
        Valves_list = []
        for i in range(self.listOrder.count()):
            if self.listOrder.item(i).text() == "Rest":
                self.listOrder.item(i).setText(LastRestValve)
            if self.listOrder.item(i).text() == RestValve:
                self.listOrder.item(i).setText("Rest")

        if RestValve == "Valve1":
            Valves_list = ['Rest', 'Valve2', 'Valve3', 'Valve4', 'Valve5', 'Valve6']
        if RestValve == "Valve2":
            Valves_list = ['Rest', 'Valve1', 'Valve3', 'Valve4', 'Valve5', 'Valve6']
        if RestValve == "Valve3":
            Valves_list = ['Rest', 'Valve1', 'Valve2', 'Valve4', 'Valve5', 'Valve6']
        if RestValve == "Valve4":
            Valves_list = ['Rest', 'Valve1', 'Valve2', 'Valve3', 'Valve5', 'Valve6']
        if RestValve == "Valve5":
            Valves_list = ['Rest', 'Valve1', 'Valve2', 'Valve3', 'Valve4', 'Valve6']
        if RestValve == "Valve6":
            Valves_list = ['Rest', 'Valve1', 'Valve2', 'Valve3', 'Valve4', 'Valve5']
        for i in range(self.ValvesList.count()):
            self.ValvesList.item(i).setText(Valves_list[i])
        LastRestValve = RestValve

    def LoginReport(self):
        self.Dialtxt.setText(DialText)
        self.Dialtxt1.setText(DialText)
        self.Dialtxt2.setText(DialText)

    def SaveLoadWinodw(self):
        self.window3 = SaveLoadWindow()
        self.window3.show()

    def MarkerWindow(self):
        self.window4 = MarkerWindow()
        self.window4.show()

    def SensorWindow(self):
        self.myFig = MyFigureCanvas(x_len=200, y_range=[0, 100], interval=20)
        self.lay = QtWidgets.QVBoxLayout(self.content_plot)        
        self.lay.addWidget(self.myFig)

    def UserLogin(self):
        self.window2 = LoginWindow()
        self.window2.show()

    def stop_all(self):
        TurnAllOff()
        global Stop
        global DialText, DialText1, DialText2
        Stop = True
        self.ResetAll()
        DialText = DialText + '\n' + "The Progress Stoped."
        DialText = DialText + '\n'
        self.Dialtxt.setText(DialText)
        self.Label.setText("Progress Terminated by Stop")
        DialText1 = DialText1 + '\n' + "The Progress Stoped."
        DialText1 = DialText1 + '\n'
        self.Dialtxt1.setText(DialText1)
        self.Label_3.setText("Progress Terminated by Stop")
        DialText2 = DialText2 + '\n' + "The Progress Stoped."
        DialText2 = DialText2 + '\n'
        self.Dialtxt2.setText(DialText2)
        self.Label_2.setText("Progress Terminated by Stop")

    def stop_all1(self):
        TurnAllOff()
        global Stop
        global DialText, DialText1, DialText2
        Stop = True
        self.ResetAll1()
        DialText = DialText + '\n' + "The Progress Stoped."
        DialText = DialText + '\n'
        self.Dialtxt.setText(DialText)
        self.Label.setText("Progress Terminated by Stop")
        DialText1 = DialText1 + '\n' + "The Progress Stoped."
        DialText1 = DialText1 + '\n'
        self.Dialtxt1.setText(DialText1)
        self.Label_3.setText("Progress Terminated by Stop")
        DialText2 = DialText2 + '\n' + "The Progress Stoped."
        DialText2 = DialText2 + '\n'
        self.Dialtxt2.setText(DialText2)
        self.Label_2.setText("Progress Terminated by Stop")

    def stop_all2(self):
        TurnAllOff()
        global Stop
        global DialText, DialText1, DialText2
        Stop = True
        self.ResetAll2()
        DialText = DialText + '\n' + "The Progress Stoped."
        DialText = DialText + '\n'
        self.Dialtxt.setText(DialText)
        self.Label.setText("Progress Terminated by Stop")
        DialText1 = DialText1 + '\n' + "The Progress Stoped."
        DialText1 = DialText1 + '\n'
        self.Dialtxt1.setText(DialText1)
        self.Label_3.setText("Progress Terminated by Stop")
        DialText2 = DialText2 + '\n' + "The Progress Stoped."
        DialText2 = DialText2 + '\n'
        self.Dialtxt2.setText(DialText2)
        self.Label_2.setText("Progress Terminated by Stop")

    def reportProgress3(self, val):
        self.progressBar.setValue(val)
        self.Label.setText("Progress: " + str(val) + "% Complete")

        if val >= 100:
            MyWindow.ResetAll(self)

    def reportProgress2(self, val):
        self.progressBar_2.setValue(val)
        self.Label_2.setText("Progress: " + str(val) + "% Complete")
        if val >= 100:
            MyWindow.ResetAll2(self)

    def reportProgress1(self, val):
        self.progressBar_1.setValue(val)
        self.Label_3.setText("Progress: " + str(val) + "% Complete")
        if val >= 100:
            MyWindow.ResetAll1(self)

    def ResetAll(self):
        global DialText
        global Stop
        # Enabling input fileds
        self.EnableAll()

        if Stop == False:
            DialText = DialText + '\n' + "The Progress Done Successfully!"
            DialText = DialText + '\n'
            self.Dialtxt.setText(DialText)

    def ResetAll1(self):
        global DialText
        global Stop
        # Enabling input fileds
        self.EnableAll()

        if Stop == False:
            DialText = DialText + '\n' + "The Progress Done Successfully!"
            DialText = DialText + '\n'
            self.Dialtxt.setText(DialText)

    def ResetAll2(self):
        global DialText2
        global Stop
        # Enabling input fileds
        self.EnableAll()

        if Stop == False:
            DialText2 = DialText2 + '\n' + "The Progress Done Successfully!"
            DialText2 = DialText2 + '\n'
            self.Dialtxt2.setText(DialText2)

    def DeviceError(self):
        global DialText
        DialText = DialText + '\n' + "Device isn't connected. Please check connection and then try again."
        DialText = DialText + '\n'
        self.Dialtxt.setText(DialText)

    def DeviceError2(self):
        global DialText2
        DialText2 = DialText2 + '\n' + "Device isn't connected. Please check connection and then try again."
        DialText2 = DialText2 + '\n'
        self.Dialtxt2.setText(DialText2)

    def DeviceError1(self):
        global DialText1
        DialText1 = DialText1 + '\n' + "Device isn't connected. Please check connection and then try again."
        DialText1 = DialText1 + '\n'
        self.Dialtxt1.setText(DialText1)

    def startall1(self):
        global DialText1
        global Login
        global DeviceConnected
        global TaskListTab1, Rest_TimeTab1, Shir_TimeTab1, RestValveTab1, RepeatTimesTab1, board, Stop
        Stop = False
        if board == None:
            DeviceInit()
        if Login == False:
            DialText1 = DialText1 + '\n' + "Please fist Login."
            DialText1 = DialText1 + '\n'
            self.Dialtxt1.setText(DialText1)
        else:

            if DeviceConnected:
                if len(TaskListTab1) >= 1:
                    self.DisableAll()

                    DialText1 = DialText1 + '\n' + "Device connected."
                    DialText1 = DialText1 + '\n'
                    DialText1 = DialText1 + '\n' + "EveryThing Ok, Starting Task"
                    DialText1 = DialText1 + '\n'
                    self.Dialtxt1.setText(DialText1)

                    Rest_TimeTab1 = self.RestTime.value()
                    Shir_TimeTab1 = self.StimuliTime.value()
                    RestValveTab1 = self.RestValveTab1.currentText()
                    RepeatTimesTab1 = 1
                    self.FirstMarker()

                    self.thread = QThread(parent=self)
                    self.worker = Worker()
                    self.worker.moveToThread(self.thread)
                    self.thread.started.connect(self.worker.run1)
                    self.worker.finished.connect(self.thread.quit)
                    self.worker.finished.connect(self.worker.deleteLater)
                    self.thread.finished.connect(self.thread.deleteLater)
                    self.worker.progress.connect(self.reportProgress1)
                    self.thread.start()

                    self.threadTimer = QThread(parent=self)
                    self.Timer = Timer()
                    self.Timer.moveToThread(self.threadTimer)
                    self.threadTimer.started.connect(self.Timer.Timing1)
                    self.worker.finished.connect(self.threadTimer.quit)
                    self.worker.finished.connect(self.Timer.deleteLater)
                    self.thread.finished.connect(self.threadTimer.deleteLater)
                    self.threadTimer.start()

                else:
                    DialText1 = DialText1 + '\n' + "Error: Time Line is empty"
                    DialText1 = DialText1 + '\n'
                    self.Dialtxt1.setText(DialText1)

            else:
                self.DeviceError1()

    def startall2(self):
        global LastRestValve
        global DialText, DialText2
        global Login
        global DeviceConnected
        global TaskList, Rest_Time, Shir_Time, RestValve, RepeatTimes, board, Stop
        Stop = False
        if board == None:
            DeviceInit()
        TaskList = []
        RepeatTimes = self.RepeatTimesNumber.value()
        for i in range(self.listOrder.count()):
            if self.listOrder.item(i).text() == "Rest":
                TaskList.append(LastRestValve)
            else:
                TaskList.append(self.listOrder.item(i).text())
        if Login == False:
            DialText2 = DialText2 + '\n' + "Please fist Login."
            DialText2 = DialText2 + '\n'
            self.Dialtxt2.setText(DialText2)
        else:
            if (len(TaskList) >= 1):
                if DeviceConnected:
                    self.DisableAll()

                    DialText2 = DialText2 + '\n' + "Device connected."
                    DialText2 = DialText2 + '\n'
                    DialText2 = DialText2 + '\n' + "EveryThing Ok, Starting Task"
                    DialText2 = DialText2 + '\n'
                    self.Dialtxt2.setText(DialText2)
                    Rest_Time = self.RestTime_tab2.value()
                    Shir_Time = self.ShirTime_tab2.value()
                    RestValve = self.RestValveValue.currentText()
                    self.FirstMarker()

                    self.thread = QThread(parent=self)
                    self.worker = Worker()
                    self.worker.moveToThread(self.thread)
                    self.thread.started.connect(self.worker.run2)
                    self.worker.finished.connect(self.thread.quit)
                    self.worker.finished.connect(self.worker.deleteLater)
                    self.thread.finished.connect(self.thread.deleteLater)
                    self.worker.progress.connect(self.reportProgress2)
                    self.thread.start()

                    self.threadTimer = QThread(parent=self)
                    self.Timer = Timer()
                    self.Timer.moveToThread(self.threadTimer)
                    self.threadTimer.started.connect(self.Timer.Timing2)
                    self.worker.finished.connect(self.threadTimer.quit)
                    self.worker.finished.connect(self.Timer.deleteLater)
                    self.thread.finished.connect(self.threadTimer.deleteLater)
                    self.threadTimer.start()
                else:
                    self.DeviceError2()

            else:
                DialText2 = DialText2 + '\n' + "TimeLine is empty; start aborted."
                DialText2 = DialText2 + '\n'
                self.Dialtxt2.setText(DialText2)

    def startall3(self):
        global Valves_list_Tab3, Valve_times, Rest_times, Priorities, FirstRest, DialText, Login, DeviceConnected, RepeatTimesNumberTab3, Stop
        Stop = False
        if board == None:
            DeviceInit()

        if Login == False:
            DialText = DialText + '\n' + "Please fist Login."
            DialText = DialText + '\n'
            self.Dialtxt.setText(DialText)
        else:
            if DeviceConnected == True:
                RepeatTimesNumberTab3 = self.RepeatTimesNumberTab3.value()
                DialText = DialText + '\n' + "Device connected."
                DialText = DialText + '\n'
                self.Dialtxt.setText(DialText)
                # initializing priorities
                Priorities[0] = [-1, self.R0.value(), 0, "Rest"]
                Priorities[1] = [self.PV1.value(), (self.V1.value()), (self.R1.value()), Valves_list_Tab3[0]]
                Priorities[2] = [self.PV2.value(), (self.V2.value()), (self.R2.value()), Valves_list_Tab3[1]]
                Priorities[3] = [self.PV3.value(), (self.V3.value()), (self.R3.value()), Valves_list_Tab3[2]]
                Priorities[4] = [self.PV4.value(), (self.V4.value()), (self.R4.value()), Valves_list_Tab3[3]]
                Priorities[5] = [self.PV5.value(), (self.V5.value()), (self.R5.value()), Valves_list_Tab3[4]]
                ones = 0
                twos = 0
                threes = 0
                fours = 0
                fives = 0
                sixs = 0
                for i in Priorities:
                    if i[0] == 1:
                        ones = ones + 1
                    if i[0] == 2:
                        twos = twos + 1
                    if i[0] == 3:
                        threes = threes + 1
                    if i[0] == 4:
                        fours = fours + 1
                    if i[0] == 5:
                        fives = fives + 1
                    if i[0] == 6:
                        sixs = sixs + 1
                # priority check
                if (ones > 1 or twos > 1 or threes > 1 or fours > 1 or fives > 1 or sixs > 1):
                    DialText = DialText + '\n' + "ERROR!" + '\n' + "- Error message: Check Priorities, there are some priorities which are same."
                    DialText = DialText + '\n'
                    self.Dialtxt.setText(DialText)
                    self.Label.setText("Progress Terminated by ERROR")
                else:
                    DialText = DialText + '\n' + "Parameters Initialized."
                    DialText = DialText + '\n' + "Starting  Progress ..."
                    DialText = DialText + '\n' + "Progress Started."
                    DialText = DialText + '\n' + "The Progress is Running  ..."
                    DialText = DialText + '\n'
                    self.Dialtxt.setText(DialText)
                    self.DisableAll()

                    self.FirstMarker()

                    self.thread = QThread(parent=self)
                    self.worker = Worker()
                    self.worker.moveToThread(self.thread)
                    self.thread.started.connect(self.worker.run3)
                    self.worker.finished.connect(self.thread.quit)
                    self.worker.finished.connect(self.worker.deleteLater)
                    self.thread.finished.connect(self.thread.deleteLater)
                    self.worker.progress.connect(self.reportProgress3)
                    self.thread.start()

                    self.threadTimer = QThread(parent=self)
                    self.Timer = Timer()
                    self.Timer.moveToThread(self.threadTimer)
                    self.threadTimer.started.connect(self.Timer.Timing3)
                    self.worker.finished.connect(self.threadTimer.quit)
                    self.worker.finished.connect(self.Timer.deleteLater)
                    self.thread.finished.connect(self.threadTimer.deleteLater)
                    self.threadTimer.start()
            else:
                self.DeviceError()

    def GenerateTimeLine(self):

        global DialText1
        global TaskListTab1
        StandardProb = self.StandardProb.value()
        ValveM3Prob = self.ValveM3Prob.value()
        ValveM4Prob = self.ValveM4Prob.value()
        ValveM5Prob = self.ValveM5Prob.value()
        ValveM6Prob = self.ValveM6Prob.value()
        if (StandardProb + ValveM3Prob + ValveM4Prob + ValveM5Prob + ValveM6Prob != 1):
            DialText1 = DialText1 + '\n' + "Error: Sum of probabilities is not one."
            DialText1 = DialText1 + '\n'
            self.Dialtxt1.setText(DialText1)
        else:
            NumberOfTrials = self.NumberOfTrials.value()
            StimuliTime = self.StimuliTime.value()
            RestTime = self.RestTime.value()
            StandardValve = self.StandardValve.currentText()
            RestValveTab1 = self.RestValveTab1.currentText()
            valveTemp = StandardValve
            if valveTemp == "Valve1":
                valveTemp = "Valve 1"
            if valveTemp == "Valve2":
                valveTemp = "Valve 2"
            if valveTemp == "Valve3":
                valveTemp = "Valve 3"
            if valveTemp == "Valve4":
                valveTemp = "Valve 4"
            if valveTemp == "Valve5":
                valveTemp = "Valve 5"
            if valveTemp == "Valve6":
                valveTemp = "Valve 6"
            StandardValve = valveTemp

            valveTemp = RestValveTab1
            if valveTemp == "Valve1":
                valveTemp = "Valve 1"
            if valveTemp == "Valve2":
                valveTemp = "Valve 2"
            if valveTemp == "Valve3":
                valveTemp = "Valve 3"
            if valveTemp == "Valve4":
                valveTemp = "Valve 4"
            if valveTemp == "Valve5":
                valveTemp = "Valve 5"
            if valveTemp == "Valve6":
                valveTemp = "Valve 6"
            RestValveTab1 = valveTemp

            Probabilities = [0, 0, 0, 0, 0]
            Probabilities[0] = [StandardProb, "Standard"]
            Probabilities[1] = [ValveM3Prob, "ValveM3"]
            Probabilities[2] = [ValveM4Prob, "ValveM4"]
            Probabilities[3] = [ValveM5Prob, "ValveM5"]
            Probabilities[4] = [ValveM6Prob, "ValveM6"]
            ValveNames = []
            Probability = []

            for valve in Probabilities:
                if valve[0] != 0:
                    ValveNames.append(valve[1])
                    Probability.append(valve[0])
            list = np.random.choice(ValveNames, NumberOfTrials, p=Probability)
            TaskList = []
            self.listOrderTab1.clear()
            for i in list:
                if i == "Standard":
                    self.listOrderTab1.addItem("Standard")
                    self.listOrderTab1.addItem("Rest")
                    TaskList.append(StandardValve)
                    TaskList.append("Rest")
                if i == "ValveM3":
                    temp = self.ValveM3.text()
                    self.listOrderTab1.addItem(temp[0:7])
                    self.listOrderTab1.addItem("Rest")
                    TaskList.append(temp[0:7])
                    TaskList.append("Rest")
                if i == "ValveM4":
                    temp = self.ValveM4.text()
                    self.listOrderTab1.addItem(temp[0:7])
                    self.listOrderTab1.addItem("Rest")
                    TaskList.append(temp[0:7])
                    TaskList.append("Rest")
                if i == "ValveM5":
                    temp = self.ValveM5.text()
                    self.listOrderTab1.addItem(temp[0:7])
                    self.listOrderTab1.addItem("Rest")
                    TaskList.append(temp[0:7])
                    TaskList.append("Rest")
                if i == "ValveM6":
                    temp = self.ValveM6.text()
                    self.listOrderTab1.addItem(temp[0:7])
                    self.listOrderTab1.addItem("Rest")
                    TaskList.append(temp[0:7])
                    TaskList.append("Rest")

            TaskListTab1 = TaskList

    def DisableAll(self):
        # Disabling input fileds
        self.PV1.setDisabled(True)
        self.PV2.setDisabled(True)
        self.PV3.setDisabled(True)
        self.PV4.setDisabled(True)
        self.PV5.setDisabled(True)
        self.V1.setDisabled(True)
        self.V2.setDisabled(True)
        self.V3.setDisabled(True)
        self.V4.setDisabled(True)
        self.V5.setDisabled(True)
        self.R0.setDisabled(True)
        self.R1.setDisabled(True)
        self.R2.setDisabled(True)
        self.R3.setDisabled(True)
        self.R4.setDisabled(True)
        self.R5.setDisabled(True)
        self.RestValveTab3.setDisabled(True)
        self.RepeatTimesNumberTab3.setDisabled(True)
        self.start.setDisabled(True)
        # self.login.setDisabled(True)
        self.stop.setDisabled(False)
        self.markertab1.setDisabled(True)
        self.saveload1.setDisabled(True)
        self.markertab2.setDisabled(True)
        self.saveload2.setDisabled(True)
        self.markertab3.setDisabled(True)
        self.saveload3.setDisabled(True)
        self.StimuliTime.setDisabled(True)
        self.RestTime.setDisabled(True)
        self.listOrderTab1.setDisabled(True)

        self.ValvesList.setDisabled(True)
        self.listOrder.setDisabled(True)
        self.RecycleBin.setDisabled(True)
        self.RestValveValue.setDisabled(True)
        self.ShirTime_tab2.setDisabled(True)
        self.RestTime_tab2.setDisabled(True)
        self.RepeatTimesNumber.setDisabled(True)
        # self.login_tab2.setDisabled(True)
        self.start2.setDisabled(True)
        self.stop2.setDisabled(False)

        self.StandardProb.setDisabled(True)
        self.ValveM3Prob.setDisabled(True)
        self.ValveM4Prob.setDisabled(True)
        self.ValveM5Prob.setDisabled(True)
        self.ValveM6Prob.setDisabled(True)
        self.TimeLineGenarateTab1.setDisabled(True)
        self.StandardValve.setDisabled(True)
        self.RestValveTab1.setDisabled(True)
        self.NumberOfTrials.setDisabled(True)
        self.markertab1.setDisabled(True)
        self.start1.setDisabled(True)
        # self.login_tab1.setDisabled(True)
        self.stop1.setDisabled(False)

    def EnableAll(self):
        self.PV1.setDisabled(False)
        self.PV2.setDisabled(False)
        self.PV3.setDisabled(False)
        self.PV4.setDisabled(False)
        self.PV5.setDisabled(False)
        self.V1.setDisabled(False)
        self.V2.setDisabled(False)
        self.V3.setDisabled(False)
        self.V4.setDisabled(False)
        self.V5.setDisabled(False)
        self.R0.setDisabled(False)
        self.R1.setDisabled(False)
        self.R2.setDisabled(False)
        self.R3.setDisabled(False)
        self.R4.setDisabled(False)
        self.R5.setDisabled(False)
        self.RestValveTab3.setDisabled(False)
        self.RepeatTimesNumberTab3.setDisabled(False)
        self.start.setDisabled(False)
        # self.login.setDisabled(False)
        self.stop.setDisabled(True)
        self.StimuliTime.setDisabled(False)
        self.RestTime.setDisabled(False)
        self.listOrderTab1.setDisabled(False)

        self.ValvesList.setDisabled(False)
        self.listOrder.setDisabled(False)
        self.RecycleBin.setDisabled(False)
        self.RestValveValue.setDisabled(False)
        self.ShirTime_tab2.setDisabled(False)
        self.RestTime_tab2.setDisabled(False)
        self.RepeatTimesNumber.setDisabled(False)
        # self.login_tab2.setDisabled(False)
        self.start2.setDisabled(False)
        self.stop2.setDisabled(True)
        self.markertab1.setDisabled(False)
        self.saveload1.setDisabled(False)
        self.markertab2.setDisabled(False)
        self.saveload2.setDisabled(False)
        self.markertab3.setDisabled(False)
        self.saveload3.setDisabled(False)

        self.StandardProb.setDisabled(False)
        self.ValveM3Prob.setDisabled(False)
        self.ValveM4Prob.setDisabled(False)
        self.ValveM5Prob.setDisabled(False)
        self.ValveM6Prob.setDisabled(False)
        self.TimeLineGenarateTab1.setDisabled(False)
        self.StandardValve.setDisabled(False)
        self.RestValveTab1.setDisabled(False)
        self.NumberOfTrials.setDisabled(False)
        self.start1.setDisabled(False)
        # self.login_tab1.setDisabled(False)
        self.stop1.setDisabled(True)

    def FirstMarker(self):
        global BOT_Marker
        if(BOT_Marker):
            self.thread = QThread(parent=self)
            self.MarkerThread = MarkerThread()
            self.MarkerThread.moveToThread(self.thread)
            self.thread.started.connect(self.MarkerThread.Marker)
            self.MarkerThread.finished.connect(self.thread.quit)
            self.MarkerThread.finished.connect(self.MarkerThread.deleteLater)
            self.MarkerThread.finished.connect(self.thread.deleteLater)
            self.thread.start()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()

    sys.exit(app.exec_())
