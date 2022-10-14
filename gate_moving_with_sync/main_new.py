from DG645 import dg645
from PicoHarp_Coding_class import PH
from ctypes import *  
import sys
import time
import matplotlib.pyplot as plt
import numpy as np

HOST = b"192.168.1.103" #DG645 IP addres
t_acquisition=30*1000 #in ms
f_pulse=2e5
T_pulse=1/f_pulse
# try :
#Opening the devices
mydg=dg645() 
myph=PH()

myph.open_ph()
mydg.open_ip(HOST)
delay_sync_trig=84*1e-9#150*1e-9 #(-8.80000000000001e-08)
delay_sync_gate=-67.5*1e-9
delay_gate_beg=delay_sync_gate-20*1e-9 #Delay gate/trigger for the first pulse

delay_syng_beg=(0)+8.80000000000001e-08

larg_gate=(20+263+20)*1e-9 #Larger of the gate for the APD
relative_real_time_trig_beg=(delay_sync_trig+delay_syng_beg)/1e-9

delta_beg_sync=250*1e-9 #Delay between two gates: takes into account the electronic errors
real_t=(relative_real_time_trig_beg*1e-9) #A realive time for stocking the results according to the delay between the gates
t_rel=delay_syng_beg
t_ac=0
t_fin=1*1e-6 #End time of acquisition
i=0 #Indice of the delay

t_one_mes = 4 * np.linspace(0,65535,65536) * 10**-3 #Time vector
ind_beg_next=np.where(t_one_mes==int(delta_beg_sync/1e-9))[0][0]
ind_last=np.where(t_one_mes==round((262.14 - delta_beg_sync/1e-9),3))[0][0]
# larg_gate_bin=int(larg_gate/(t[1]*1e-9)) #Larger of the gate for the APD in units of the picoharp ector
# error_bin=int(15/(t[1])) #Larger of the error done by the APD in units of the picoharp ector

Counts=np.zeros(t_one_mes.size)

plt.ion() #For tracing the figure
figure, ax = plt.subplots(figsize=(10,10))
plot1, = ax.plot(t_one_mes, Counts)
plt.ylim(0,50)
plt.xlim(200,1300)

Counts=[] #Variable where we will stock all the datas
t_beg=[]#Variable where we will stock the relative delays between the gates

mydg.set_larg_gate(larg_gate) #Setting the larger of the gate

plt.show()

mean_cnt=np.zeros(65536) #Initialization of the vector where we will stock the final datas
fst=[] #where non zero cnts
lst=[]

while ((real_t)<t_fin): #Loop for moving the gates
    t_end_ac=real_t+delta_beg_sync
    t_beg.append(real_t/1e-9)
    if t_end_ac<t_fin:
        mydg.set_delay_gate(t_rel + delay_gate_beg) #Moving the gate
        mydg.set_delay_sync(t_rel) #Moving the gate
    else:
        mydg.set_larg_gate(larg_gate-20*1e-9-(t_end_ac-t_fin))
        mydg.set_delay_gate(t_rel + delay_gate_beg) #Moving the gate
        mydg.set_delay_sync(t_rel) #Moving the gate
    [new_counts,new_t]=myph.start_measure_with_plot(t_acquisition) #Taking a measure
    
    # ind=np.where(new_counts!=0) #
    # fst.append(ind[0][0])
    # lst.append(ind[0][np.where(ind[0] < (ind[0][0]+larg_gate_bin))[0][-1]])
    
    if i==0 : #alculating a mean value for the system taking in counts the electronic errors of the APD
        mean_cnt=new_counts
        t=new_t+relative_real_time_trig_beg
    else:
        mean_mean=(mean_cnt[len(mean_cnt)-(65536-ind_beg_next):len(mean_cnt)] + new_counts[0:ind_last+1])/2
        mean_cnt=np.concatenate((mean_cnt[0:len(mean_cnt)-(65536-ind_beg_next)-1],mean_mean,new_counts[ind_last+1:655635]))
        t=np.concatenate((t[0:len(t)-(65536-ind_beg_next)-1],(new_t[0:655635] + real_t/1e-9)))
        # mean_cnt[(fst[i]+error_bin):(lst[i-1]-error_bin)]=(mean_cnt[(fst[i]+error_bin):(lst[i-1]-error_bin)]+new_counts[(fst[i]+error_bin):(lst[i-1]-error_bin)])/2
        # mean_cnt[(lst[i-1]-error_bin + 1) :  (lst[i]-error_bin)]=new_counts[(lst[i-1]-error_bin + 1) :  (lst[i]-error_bin)]

    
    Counts.append(new_counts)
    
    plot1.set_xdata(t)
    plot1.set_ydata(mean_cnt)
    figure.canvas.draw()
    figure.canvas.flush_events()
    
    i+=1
    real_t+=delta_beg_sync
    t_rel+=delta_beg_sync
    t_ac+=delta_beg_sync        
    
myph.close_APD()
mydg.close()
# except:
#     mydg.close()
#     myph.close_APD()
