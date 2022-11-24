from DG645 import dg645
from PicoHarp_Coding_class import PH
from ctypes import *  
import sys
import time
import matplotlib.pyplot as plt
import numpy as np

#%% Important informations for the code

HOST_DG645 = b"192.168.1.103" #DG645 IP addres

#%% Set the cycles options

N_samples = 1000
vect_delay = [1,10,20,30,40,50]

#%% Opening the devices

mydg=dg645() 
myph=PH()

myph.open_ph()
mydg.open_ip(HOST_DG645)

#%% Set the resolution of the PH

#Pour des sondes de 5us pourquoi pas une reso de 128ps? -> Time span du PH de 8.4us

#%% Larger of the pulses

larg_sonde = 5 * 1e-6

larg_gate = larg_sonde + (2*20)*1e-9 #Larger of the gate for the APD
mydg.set_larg_gate(larg_gate) #Setting the larger of the gate

larg_pump = 50 * 1e-6

#%% Physical cable delays

delay_sync_trig=84*1e-9 
delay_sync_gate=-67.5*1e-9


#%% Boucle de mesure

