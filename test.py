from pyfirmata2 import Arduino
import time

onTime = 1
board = Arduino(Arduino.AUTODETECT)


for i in [8,9,10, 11 ,12, 7]:
    board.digital[i].write(1)
    board.digital[6].write(1)
    time.sleep(onTime)
    board.digital[i].write(0)
    board.digital[6].write(0)
    time.sleep(1)