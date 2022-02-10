import serial
import time
import csv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
matplotlib.use("TkAgg")
os.system('clear')

subjectName = input("Enter the Subject's name:\n")
f = open(subjectName+'.csv', 'w')
writer = csv.writer(f)
header = ['Time(s)', 'Frequency(Hz)']
writer.writerow(header)

serialPort = serial.Serial('/dev/tty.usbmodem14201', 9600)

fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
global dataTemp
dataTemp = 0
# This function is called periodically from FuncAnimation
def current_milli_time():
    return round(time.time() * 1000)

def animate(i, xs, ys, timeStart):
    global dataTemp
    # Read temperature (Celsius) from TMP102
    try:
        dataRealTime = int(serialPort.readline())
        dataTemp = dataRealTime
    except:
        dataRealTime = dataTemp
    finally:
        timeNow = (current_milli_time()-timeStart)/1000
    # Add x and y to lists
    writer.writerow([timeNow, dataRealTime])
    xs.append(timeNow)
    ys.append(dataRealTime)

    # Limit x and y lists to 200 items
    xs = xs[-100:]
    ys = ys[-100:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    LimitD = 10000
    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Frequency Vs Time')
    plt.ylabel('Frequency')
    plt.ylim(dataRealTime-LimitD,dataRealTime+LimitD)
    plt.xlabel('Time')

# Set up plot to call animate() function periodically
timeStart = current_milli_time()
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, timeStart), interval=20)
plt.show()
f.close()





