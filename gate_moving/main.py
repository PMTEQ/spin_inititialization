from DG645 import dg645
from PicoHarp_Coding_class import PH
from ctypes import *  
import sys
import time
import matplotlib.pyplot as plt
import numpy as np

HOST = b"192.168.1.103" #DG645 IP addres
t_acquisition=5*1000 #in ms

# try :
#Opening the devices
mydg=dg645() 
myph=PH()

myph.open_ph()
mydg.open_ip(HOST)

delay_gate_beg=280*1e-9 #Delay gate/trigger for the first pulse
larg_gate=100*1e-9 #Larger of the gate for the APD

delta_beg=larg_gate-(15+30)*1e-9 #Delay between two gates: takes into account the electronic errors
t_ac=0 #A realive time for stocking the results according to the delay between the gates
t_fin=270*1e-9 #End time of acquisition
i=0 #Indice of the delay

t = 4 * np.linspace(0,65535,65536) * 10**-3 #Time vector
larg_gate_bin=int(larg_gate/(t[1]*1e-9)) #Larger of the gate for the APD in units of the picoharp ector
error_bin=int(15/(t[1])) #Larger of the error done by the APD in units of the picoharp ector

Counts=np.zeros(t.size)

plt.ion() #For tracing the figure
figure, ax = plt.subplots(figsize=(10,10))
plot1, = ax.plot(t, Counts)
plt.ylim(0,50)

Counts=[] #Variable where we will stock all the datas
t_beg=[]#Variable where we will stock the relative delays between the gates

mydg.set_larg_gate(larg_gate) #Setting the larger of the gate

plt.show()

mean_cnt=np.zeros(65536) #Initialization of the vector where we will stock the final datas
fst=[] #where non zero cnts
lst=[]

while ((t_ac)<t_fin): #Loop for moving the gates
    
    t_beg.append(t_ac + delay_gate_beg)
    mydg.set_delay_gate(t_ac + delay_gate_beg) #Moving the gate
    [new_counts,new_t]=myph.start_measure_with_plot(t_acquisition) #Taking a measure
    
    ind=np.where(new_counts!=0) #
    fst.append(ind[0][0])
    lst.append(ind[0][np.where(ind[0] < (ind[0][0]+larg_gate_bin))[0][-1]])
    
    if t_ac==0 : #alculating a mean value for the system taking in counts the electronic errors of the APD
        mean_cnt[(fst[i]+error_bin) : (lst[i]-error_bin)]=new_counts[(fst[i]+error_bin) : (lst[i]-error_bin)]
    else:
        
        mean_cnt[(fst[i]+error_bin):(lst[i-1]-error_bin)]=(mean_cnt[(fst[i]+error_bin):(lst[i-1]-error_bin)]+new_counts[(fst[i]+error_bin):(lst[i-1]-error_bin)])/2
        mean_cnt[(lst[i-1]-error_bin + 1) :  (lst[i]-error_bin)]=new_counts[(lst[i-1]-error_bin + 1) :  (lst[i]-error_bin)]

    
    Counts.append(new_counts)
    
    plot1.set_xdata(t)
    plot1.set_ydata(mean_cnt)
    figure.canvas.draw()
    figure.canvas.flush_events()
    
    i+=1
    t_ac+=delta_beg        
    
myph.close_APD()
mydg.close()
# except:
#     mydg.close()
#     myph.close_APD()
