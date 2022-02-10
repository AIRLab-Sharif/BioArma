%% run this section at the start
clc
clear
serial_port = '/dev/cu.usbmodem14201';
bioarma =  serialport(serial_port,9600);
%% apply your changes here
clc
valve = 1;
time = 2;
pinHandler(bioarma, valve, time)
%% run this section at the end of the experiment
clear bioarma