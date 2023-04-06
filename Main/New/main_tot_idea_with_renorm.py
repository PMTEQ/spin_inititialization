from DG645 import dg645
from PicoHarp_Coding_class import PH
from my_aerodiode_class import my_tombak
from SR400 import mySR400
from ctypes import *  
import sys
import time
import matplotlib.pyplot as plt
from scipy.io import savemat
import numpy as np

#%% Important informations for the code

HOST_DG645 = b"192.168.1.103" #DG645 IP addres
# COM_tombak = 'COM5' #COM address for the aerodiode
#%% Set the cycles options
wanted_number_of_cycles=100000
vect_delay = [0] # in us


#%% Opening the devices

mydg=dg645() 
myph=PH()
mysr=mySR400()
# mytombak = my_tombak()

myph.open_ph()
mydg.open_ip(HOST_DG645)
mysr.open_sr("COM4")
mysr.setup_sr()
# mytombak.open_my_tombak(COM_tombak)

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
my_range=5
myph.set_range(my_range)
mydg.set_modu_AOM_channel(1)
mydg.set_modu_EOM_channel(4)
mydg.set_synchro_PH_channel(3)
mydg.set_gate_APD_channel(2)
#%% Set the largers of the pulses

time_unit="us"
time_multi=1e-6
length_pump = 50
larg_sonde = 5
larg_PH=t = 2**((my_range)+2) * 65535 * 10**-6
wait_gate_APD=0.1
larg_gate_APD = larg_PH + (2*wait_gate_APD) #Larger of the gate for the APD
wait_after_end=1
time_between_PH_probe = (larg_PH-larg_sonde)/2


mydg.set_larg_APD(larg_gate_APD*time_multi) #Setting the larger of the gate
mydg.set_larg_PH(80e-9)
mydg.set_larg_AOM(length_pump*time_multi) 
mydg.set_larg_EOM(larg_sonde*time_multi)
#%% Physical cable delays
#trig first
#By default the AOM is synchronized with the trigger

cable_PH_trig=0.133
cable_probe_trig=(0)
cable_APD_trig=0.133 #trig first


#%% Boucle de mesure
my_ind=0
 
for i in range(len(vect_delay)):
    ##times for DG645
    delay_pump_probe = vect_delay[i]
    beg_probe=delay_pump_probe+length_pump
    beg_PH=beg_probe - time_between_PH_probe
    beg_APD = beg_PH-wait_gate_APD

    end_probe = beg_probe + larg_sonde
    end_PH=beg_PH+larg_PH
    end_APD = beg_APD + larg_gate_APD
    
    period_mes=end_APD+wait_after_end
    t_acquisition = (period_mes*wanted_number_of_cycles)/1000 #in usec
    f_pump = 1/(period_mes * time_multi)
    
    mydg.set_trig_rate(f_pump)
    mydg.set_delay_APD((beg_APD-cable_APD_trig)*time_multi) #Setting the begining of the gate
    mydg.set_delay_PH((beg_PH-cable_PH_trig)*time_multi)
    mydg.set_delay_AOM(0)
    mydg.set_delay_EOM((beg_probe-cable_probe_trig)*time_multi)
    [new_counts,new_t]=myph.start_measure_with_plot((t_acquisition)) #Taking a measure
    mysr.beg_count(wanted_number_of_cycles, 100E-9, 100E-9, length_pump*time_multi + delay_pump_probe*time_multi + 100E-9, larg_sonde*time_multi - 100E-9)
    
    dark=3000
    duty_cycle_SR400= (larg_sonde*time_multi - 100E-9)*f_pump
    tau_integ=wanted_number_of_cycles*duty_cycle_SR400/f_pump
    total_dark=3000*tau_integ
    
    if (i>1):
        temp_t=np.zeros([1,np.shape((new_t))[0]])
        temp_count=np.zeros([1,np.shape((new_t))[0]])
        temp_value_SR400=np.zeros([1,np.shape((old_value_SR400[0,:]))[0]])
        
        new_t+=(beg_PH-cable_PH_trig )
        temp_t[0,:]=new_t
        temp_count[0,:]=new_counts
        new_t=np.concatenate((old_t, temp_t), axis=0)
        new_counts=np.concatenate((old_count, temp_count), axis=0)
        old_t=new_t
        old_count=new_counts
        
        ready_quer = mysr.is_data_ready_query()
        while ready_quer==0:
            ready_quer = mysr.is_data_ready_query()
        count_SR400=mysr.recover_count()
        new_renormalized_APD_counts=np.concatenate((old_renormalized_APD_counts, temp_count/(count_SR400[1])), axis=0)
        old_renormalized_APD_counts=new_renormalized_APD_counts
        
        new_renormalized_APD_counts_darkless=np.concatenate((old_renormalized_APD_counts_without_dark, temp_count/(count_SR400[1]-total_dark)), axis=0)
        old_renormalized_APD_counts_without_dark=new_renormalized_APD_counts_darkless
        
        temp_value_SR400[0,:]=count_SR400
        new_value_SR400=np.concatenate((old_value_SR400, temp_value_SR400), axis=0)
        old_value_SR400=new_value_SR400
        
        mdic = {"Delays": vect_delay, "Time": new_t, "Counts": new_counts, "Counts_renormalized": old_renormalized_APD_counts, "Counts_renormalized_corrected": old_renormalized_APD_counts_without_dark, "SR400_Counts": old_value_SR400}
        
    elif (i==0): 
        new_t+=(beg_PH-cable_PH_trig)
        old_t=new_t
        old_count=new_counts
        
        ready_quer = mysr.is_data_ready_query()
        while ready_quer==0:
            ready_quer = mysr.is_data_ready_query()
        
        count_SR400=mysr.recover_count()

        old_renormalized_APD_counts=new_counts/(count_SR400[1])
        old_renormalized_APD_counts_without_dark=new_counts/(count_SR400[1]-total_dark)

        old_value_SR400=count_SR400
        
        mdic = {"Delays": vect_delay, "Time": new_t, "Counts": new_counts, "Counts_renormalized": old_renormalized_APD_counts, "Counts_renormalized_corrected": old_renormalized_APD_counts_without_dark, "SR400_Counts": old_value_SR400}
        
    elif (i==1): 
        temp_t=np.zeros([2,np.shape((old_count))[0]])
        temp_count=np.zeros([2,np.shape((old_count))[0]])
        temp_renormalized_APD_counts=np.zeros([2,np.shape((old_renormalized_APD_counts))[0]])
        temp_renormalized_APD_counts_darkless=np.zeros([2,np.shape((old_renormalized_APD_counts))[0]])

        temp_value_SR400=np.zeros([2,np.shape((old_value_SR400))[0]])
        
        temp_t[0,:]=old_t
        temp_count[0,:]=old_count
        temp_renormalized_APD_counts[0,:]=old_renormalized_APD_counts
        temp_renormalized_APD_counts_darkless[0,:]=old_renormalized_APD_counts_without_dark
        temp_value_SR400[0,:]=old_value_SR400
        
        ready_quer = mysr.is_data_ready_query()
        while ready_quer==0:
            ready_quer = mysr.is_data_ready_query()
        
        count_SR400=mysr.recover_count()

        
        new_t+=(beg_PH-cable_PH_trig)
        temp_t[1,:]=new_t
        temp_count[1,:]=new_counts
        temp_renormalized_APD_counts[1,:]=new_counts/(count_SR400[1])
        temp_renormalized_APD_counts_darkless[1,:]=new_counts/(count_SR400[1]-total_dark)
        temp_value_SR400[1,:]=count_SR400
        
        old_t=temp_t
        old_count=temp_count
        old_renormalized_APD_counts=temp_renormalized_APD_counts
        old_renormalized_APD_counts_without_dark=temp_renormalized_APD_counts_darkless
        old_value_SR400=temp_value_SR400
        
        mdic = {"Delays": vect_delay, "Time": new_t, "Counts": new_counts, "Counts_renormalized": old_renormalized_APD_counts,"Counts_renormalized_corrected": old_renormalized_APD_counts_without_dark, "SR400_Counts": old_value_SR400}
    
    savemat("matlab_matrix.mat", mdic)


#%% Close all

# # mytombak.off_out()
myph.close_APD()
mydg.close()
mysr.close_sr()


#%%Param physique

for i in range(len(vect_delay)):
    delay_pump_probe = vect_delay[i]
    plt.plot(new_t[i],new_renormalized_APD_counts_darkless[i]*np.max(old_value_SR400[:,1]))

    plt.plot(new_t[i],new_counts[i])
    ##times for DG645
    
    beg_probe=delay_pump_probe+length_pump
    beg_PH=beg_probe - time_between_PH_probe
    beg_APD = beg_PH-wait_gate_APD
    
    end_probe = beg_probe + larg_sonde
    end_PH=beg_PH+larg_PH
    end_APD = beg_APD + larg_gate_APD
    
    period_mes=end_APD+wait_after_end
    f_pump = 1/(period_mes * time_multi)
    
    ## Param tracé
    time_step=1e-3
    time_vec_per=np.arange(0, period_mes,time_step)
    pump_vec_per=np.zeros(len(time_vec_per))
    pump_vec_per[0:np.where(time_vec_per>length_pump)[0][0]-1]=100
    probe_vec_per=np.zeros(len(time_vec_per))
    probe_vec_per[np.where(time_vec_per>beg_probe)[0][0]-1:np.where(time_vec_per>end_probe)[0][0]-1]=100
    APD_gate_vec_per=np.zeros(len(time_vec_per))
    APD_gate_vec_per[np.where(time_vec_per>beg_APD)[0][0]-1:np.where(time_vec_per>end_APD)[0][0]-1]=100
    PH_vec_per=np.zeros(len(time_vec_per))
    PH_vec_per[np.where(time_vec_per>beg_PH)[0][0]-1:np.where(time_vec_per>end_PH)[0][0]-1]=100
    
    if i==0 :
        plt.plot(time_vec_per,pump_vec_per,'b',label="Pompe")

    plt.plot(time_vec_per,probe_vec_per,'m',label="Sonde")
    plt.plot(time_vec_per,APD_gate_vec_per,'r',label="Gate APD")
    plt.plot(time_vec_per,PH_vec_per,'g--',label="Fenêtre PH")