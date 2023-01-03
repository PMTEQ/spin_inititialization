from DG645 import dg645
from PicoHarp_Coding_class import PH
from my_aerodiode_class import my_tombak
from ctypes import *  
import sys
import time
import matplotlib.pyplot as plt
from scipy.io import savemat
import numpy as np

#%% Important informations for the code

HOST_DG645 = b"192.168.1.103" #DG645 IP addres
COM_tombak = 'COM5'
#%% Set the cycles options

N_samples = 1000
vect_delay = [1,10,20,30,40,50]

#%% Opening the devices

mydg=dg645() 
myph=PH()
mytombak = my_tombak()

myph.open_ph()
mydg.open_ip(HOST_DG645)
mytombak.open_my_tombak(COM_tombak)

#%% Set the resolution of the PH

#Range:
    # 0, Resolution 4ps, Time span ; 262.1 ns
    # 1, Resolution 8ps, Time span ; 524.3 ns
    # 2, Resolution 16ps, Time span ; 1.049 us
    # 3, Resolution 32ps, Time span ; 2.097 us
    # 4, Resolution 64ps, Time span ; 4.194 us
    # 5, Resolution 128ps, Time span ; 8.389 us
    # 6, Resolution 256ps, Time span ; 16.777 us
    # 7, Resolution 512ps, Time span ; 33.554 us
#/!\ Default range is 0

#Pour des sondes de 5us pourquoi pas une reso de 128ps? 

myph.set_range(0)

#%% Larger of the pulses

larg_sonde = 5 * 1e-6

larg_gate = larg_sonde + (2*20)*1e-9 #Larger of the gate for the APD
mydg.set_larg_gate(larg_gate) #Setting the larger of the gate

larg_pump = 50 * 1e-6

#%% Physical cable delays

delay_sync_trig=84*1e-9 
delay_sync_gate=-67.5*1e-9


#%% Boucle de mesure


a = np.arange(20)
mdic = {"a": a, "label": "experiment"}
mdic
{'a': array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
    17, 18, 19]),
'label': 'experiment'}
savemat("matlab_matrix.mat", mdic)

#%% Close all

mytombak.off_out()
myph.close_APD()
mydg.close()
