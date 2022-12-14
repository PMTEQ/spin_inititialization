import pyvisa as visa
import numpy as np
import time
import matplotlib.pyplot as plt
import sys
import csv
from os.path import exists


#%% /!\ A remplir: 
    
info_datas='commercial_diode'#Informations sur les donnees
V_deb=-0.1 # Tension de d2but de mesure
V_fin=0.5 #Tension de fin de mesure
N_ech=10 # Nomnre de mesures a prendre
#%% Ouverture du Keithley
rm = visa.ResourceManager()
print (rm.list_resources())
with rm. open_resource('COM7') as Keithley:
    Keithley.port = 'COM7'
    Keithley.baudrate = 9600
    Keithley.timeout = 25000
    
Keithley.open()
Keithley.read_termination = '\r'
Keithley.write_termination = '\r'
Keithley.write("*RST")
Keithley.write("*IDN?")
Q=Keithley.read()


#%% Boucle pour prendre les mesures de tensions


volt=np.linspace(V_deb,V_fin,N_ech) #Definition de toutes les tensions a explorer
res_volt=[] #Vecteur qui contiendra la tension appliquee
res_amp=[] #Vecteur qui contiendra le courant mesure

Keithley.write(":SOUR:VOLT:LEV:IMM:AMPL 0") #Mise a 0V de la tension pour etre sur
Keithley.write(":OUTP ON")    #Allumage de loutput

for i in range(len(volt)): #Boucle pour les mesures
    Keithley.write(":SOUR:VOLT:LEV:IMM:AMPL "+str(volt[i]))  #Application de la tension
    Keithley.write(":MEAS:CURR:DC?") #Commande de mesure
    Q=Keithley.read() #La mesure est un tableau, la premiere case est la tension, la seconde le courant
    A=np.array(Q.split(','))
    A=A.astype('float64')
    cur_volt=A[0] #Stockage des donnees
    cur_amp=A[1]
    res_volt.append(cur_volt)#Stockage des donnees
    res_amp.append(cur_amp)
    
plt.plot(res_volt,res_amp)

#%% Enregistrement des donnees
rows=[res_volt,res_amp] #Donnees a enregistrer
file_name='IV_data_'+info_datas #Nom du fichier
file_name_new=file_name

n=1
while  exists(file_name_new+'.csv')==True : #Boucle pour ne pas effacer de donnees
    file_name_new=file_name+'_'+str(n)
    n+=1
file_name=file_name_new+'.csv'
with open(file_name, 'w') as f: #Enregistrement
    write = csv.writer(f, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    write.writerows(rows)
    
#%% Pour lire les donnees
# data=[]
# with open(file_name, newline='') as csvfile:
#     data_read = csv.reader(csvfile, delimiter=',', quotechar='|')
#     for row in data_read:
#         if len(row)>0:
#             data.append(row[0].split(' '))
# data=np.array(data).astype('float64') #Donn2es exploitables
#%%
Keithley.write(":SOUR:VOLT:LEV:IMM:AMPL 0")

Keithley.close()
