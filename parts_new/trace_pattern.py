import matplotlib.pyplot as plt
import numpy as np

##Param physique
time_unit="us"
time_multi=1e-6
length_pump = 50
larg_sonde = 5
delay_pump_probe = 10
larg_PH=8.389
wait_gate_APD=0.02
larg_gate_APD = larg_sonde + (2*wait_gate_APD)
wait_after_end=0.1
time_between_PH_probe = (larg_PH-larg_sonde)/2


##times for DG645

beg_probe=delay_pump_probe+length_pump
beg_PH=beg_probe - time_between_PH_probe
beg_APD = beg_PH-wait_gate_APD

end_probe = beg_probe + larg_sonde
end_PH=beg_probe+(larg_PH+larg_sonde)/2
end_APD = end_PH + wait_gate_APD

period_mes=end_APD+wait_after_end
f_pump = 1/(period_mes * time_multi)

## Param tracé
time_step=1e-3
time_vec_per=np.arange(0, period_mes,time_step)
pump_vec_per=np.zeros(len(time_vec_per))
pump_vec_per[0:np.where(time_vec_per>length_pump)[0][0]-1]=4
probe_vec_per=np.zeros(len(time_vec_per))
probe_vec_per[np.where(time_vec_per>beg_probe)[0][0]-1:np.where(time_vec_per>end_probe)[0][0]-1]=4
APD_gate_vec_per=np.zeros(len(time_vec_per))
APD_gate_vec_per[np.where(time_vec_per>beg_APD)[0][0]-1:np.where(time_vec_per>end_APD)[0][0]-1]=4
PH_vec_per=np.zeros(len(time_vec_per))
PH_vec_per[np.where(time_vec_per>beg_PH)[0][0]-1:np.where(time_vec_per>end_PH)[0][0]-1]=4


plt.plot(time_vec_per,pump_vec_per,label="Pompe")
plt.plot(time_vec_per,probe_vec_per,label="Sonde")
plt.plot(time_vec_per,APD_gate_vec_per,label="Gate APD")
plt.plot(time_vec_per,PH_vec_per,label="Fenêtre PH")
plt.legend()
