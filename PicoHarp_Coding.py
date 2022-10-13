from ctypes import *  
import sys
import time
import matplotlib.pyplot as plt
import numpy as np

#%% Definition
phdll = cdll.LoadLibrary("phlib.dll") 

REQLIBVER =  '2.3';     
MAXDEVNUM =      8;
HISTCHAN  =  65536;	    
RANGES	  =      8;
MODE_HIST =      c_int(0);
MODE_T2	  =      2;
MODE_T3	  =      3;

# FLAG_OVERFLOW = hex2dec('0040');

ZCMIN		  =          0;		
ZCMAX		  =         20;		
DISCRMIN	  =          0;	    
DISCRMAX	  =        800;	    
OFFSETMIN	  =          0;
OFFSETMAX	  = 1000000000;

ACQTMIN		  =          1;		# ms
ACQTMAX		  =  360000000;	    # ms  (10*60*60*1000ms = 100h)

# Errorcodes from errorcodes.h

PH_ERROR_DEVICE_OPEN_FAIL		 = -1;

# Settings for the measurement

Offset       = 0;       #  you can change this
Tacq         = 1000*60;    #  you can change this      
RES = 4
Stop_of_ok=0 #Dont stop at overflow
Stop_count=65535 
range_res=0

#Sync chanel:
ZC_sync=10
DISCR_sync=200
DIV_sync=1

#Channel 1:

ZC_ch1=20
DISCR_ch1=500


serial = (c_char * 8)()
dev_number=c_int(0)
#%% Open device

print("Opening the picoHarp")
ret=phdll.PH_OpenDevice(dev_number,byref(serial))

if ret==0:
    print("PicoHarp succesfully opened")
else:
    print("PicoHarp opening failed")
    sys.exit()

print("Initializing")
ret2=phdll.PH_Initialize(dev_number,MODE_HIST)


#%% Settings

print("Calibrating")
ret=phdll.PH_Calibrate(dev_number)

print("Setting up channels")
ret=phdll.PH_SetCFDLevel(dev_number,c_int(0),DISCR_sync)
ret=phdll.PH_SetCFDLevel(dev_number,c_int(1),DISCR_ch1)
ret=phdll.PH_SetCFDZeroCross(dev_number,c_int(0),ZC_sync)
ret=phdll.PH_SetCFDZeroCross(dev_number,c_int(1),ZC_ch1)
ret=phdll.PH_SetSyncDiv(dev_number,c_int(1))

ret=phdll.PH_SetStopOverflow(dev_number,Stop_of_ok,Stop_count)

ret=phdll.PH_SetRange(dev_number,range_res)

ret=phdll.PH_SetOffset(dev_number,Offset)

ret=phdll.PH_ClearHistMem(dev_number,0)

time.sleep(5)

print("Setting up done")


#%% Measurements

Counts_c=(c_uint*HISTCHAN)()
Counts=np.zeros(HISTCHAN)

print("Starting measures")
ret=phdll.PH_StartMeas(dev_number,Tacq)
tdeb=time.time()

plt.ion()


t = 4 * np.linspace(0,65535,65536) * 10**-3
figure, ax = plt.subplots(figsize=(5,5))
plot1, = ax.plot(t, Counts)
plt.ylim(0,10)

plt.show()

while (time.time()-tdeb)<((Tacq/1000)+5):
    time.sleep(1)
    count_rate_APD=phdll.PH_GetCountRate(dev_number,1)
    print('APD count rate (en cps): ' + str(count_rate_APD)+ ' // Time remaining (en sec) : ' + str((Tacq/1000)-(time.time()-tdeb)))
    ret=phdll.PH_GetBlock(dev_number,byref(Counts_c),0)
    for i in range(HISTCHAN):
        Counts[i]=Counts_c[i]
    plot1.set_xdata(t)
    plot1.set_ydata(Counts)
    figure.canvas.draw()
    figure.canvas.flush_events()

ret=phdll.PH_StopMeas(dev_number,Tacq)
test = (phdll.PH_CTCStatus(dev_number))
print("End measures")





#%%
phdll.PH_CloseDevice(c_int(0))

