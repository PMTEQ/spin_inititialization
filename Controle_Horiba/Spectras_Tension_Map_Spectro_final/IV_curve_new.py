import pyvisa as visa
import numpy as np
import time
import matplotlib.pyplot as plt
import sys
import csv
from os.path import exists
import u3

#%% /!\ A remplir: 
    
input("Welcome to the program allowing you to take IV curve and spectral datas. Please open synergy, then in the Experiment Setup panel load the IV_Curve_Labjack.xml experiment file. Choose your experimental details (dont forget to modify the accumulation number to the number of samples you want to take) then press Run in Synergy. When done press enter here.")

my_path=input("Enter a path (without the \ at the end) where to record the datas of IV Curve: ")
info_datas=input("Enter a name for the actual experiment: ")
V_deb=float(input("Enter the minimum tension to apply (in Volts): ")) # Tension de d2but de mesure
V_fin=float(input("Enter the maximum tension to apply (in Volts): ")) #Tension de fin de mesure
N_ech=int(input("Enter the number of samples to get (make it match with the Synergy accumulation number): ")) # Nomnre de mesures a prendre
my_time=float(input("Time to wait between the application of the tension and the data recording (in seconds): ")) # Nomnre de mesures a prendre
keithley_model=float(input("Please enter 1 for the Keithley model 2401 or 2 for the Keithley model 2604 then press enter: ")) #1=2401 et 2=2604

if keithley_model==2 :
    channel_meas=input("Enter the letter of the channel you are using A or B (in capital letter) then press enter: ") #A ou B
    
    if (channel_meas=='A'):
        source_str='smua'
    elif (channel_meas=='B'):
        source_str='smub'
    else:
        print("Unknown channel")
        input("Program will abort, please press enter")
        sys.exit()
elif keithley_model==1 :
    pass
else:
    print("Unknown Keithley")
    input("Program will abort, please press enter")
    sys.exit()

print("Initializing the program")

#%% Ouverture du Keithley et du LabJack
try : 
    #Ouverture du LABJACK pour le spectro
    #Le DAC0 envoie l'impulsion pour commencer l'acquisition d'une donnée
    #AIN0 sert a checker le moment actuel de l'acquisiton
    d = u3.U3() #Ouverture du LabJack U3-HV

    
    rm = visa.ResourceManager()
    # print (rm.list_resources())
    
    if keithley_model==1:
        with rm. open_resource('COM3') as Keithley:
            Keithley.port = 'COM3'
            Keithley.baudrate = 9600
            Keithley.timeout = 25000
            Keithley.open()
            Keithley.read_termination = '\r'
            Keithley.write_termination = '\r'
    elif  keithley_model==2:
        Keithley = rm.open_resource('ASRL3::INSTR')
        
        
    
    Keithley.write("*RST")
    Keithley.write("*IDN?")
    Q=Keithley.read()
    print("Devices opened.")
except:
    print("Couldn't open the LabJAck or the Keithley chexk the COM port and go to the python file to check the working of the program")
    input("Press enter to end the program")
    sys.exit()

#%% Boucle pour prendre les mesures de tensions

print("Beginnig data taking")

volt=np.linspace(V_deb,V_fin,N_ech) #Definition de toutes les tensions a explorer
res_volt=[] #Vecteur qui contiendra la tension appliquee
res_amp=[] #Vecteur qui contiendra le courant mesure

if keithley_model==1:
    Keithley.write(":SOUR:VOLT:LEV:IMM:AMPL 0") #Mise a 0V de la tension pour etre sur
    Keithley.write(":OUTP ON")    #Allumage de loutput

    for i in range(len(volt)): #Boucle pour les mesures
        print("Taking datas for "+str(volt[i])+"V")

        Keithley.write(":SOUR:VOLT:LEV:IMM:AMPL "+str(volt[i]))  #Application de la tension
        time.sleep(my_time) #Waiting for a permanent regime
        Keithley.write(":MEAS:CURR:DC?") #Commande de mesure
        Q=Keithley.read() #La mesure est un tableau, la premiere case est la tension, la seconde le courant
        A=np.array(Q.split(','))
        A=A.astype('float64')
        cur_volt=A[0] #Stockage des donnees
        cur_amp=A[1]
        res_volt.append(cur_volt)#Stockage des donnees
        res_amp.append(cur_amp)
    #### Code pour gérer acquisition spectro
        
        DAC0_VALUE = d.voltageToDACBits(4.5, dacNumber = 0, is16Bits = False)
        d.getFeedback(u3.DAC0_8(DAC0_VALUE))
        time.sleep(0.1)

        DAC0_VALUE = d.voltageToDACBits(0, dacNumber = 0, is16Bits = False)
        d.getFeedback(u3.DAC0_8(DAC0_VALUE))

        ainValue = d.getAIN(0)#Lecture de la valeur de la sortie du symphony. Quand elle sera à 0, cela voudra dire que la CCD est en train detre lue
        
        if (volt[i]!=volt[-1]):
            while (ainValue>2): #Attente d'un front descendant (Lecture de la CCD)
                ainValue = d.getAIN(0) 
            while (ainValue<2): #Attente d'un front montant (Expérience prete a tourner)
                ainValue = d.getAIN(0) 
        else:
            while (ainValue>2): #Attente d'un front descendant (Lecture de la CCD)
                ainValue = d.getAIN(0) 
    #####################################################################
        print("Datas for "+str(volt[i])+"V taken")
        
    Keithley.write(":SOUR:VOLT:LEV:IMM:AMPL 0")

elif  keithley_model==2:
    
    Keithley.write(source_str+".source.func="+source_str+".OUTPUT_DCVOLTS")
    Keithley.write(source_str+".source.levelv=0")
    Keithley.write(source_str+".source.output ="+ source_str+".OUTPUT_ON")
                   

    for i in range(len(volt)): #Boucle pour les mesures
        print("Taking datas for "+str(volt[i])+"V")

        Keithley.write(source_str+".source.levelv="+str(volt[i]))  #Application de la tension
        time.sleep(my_time) #Waiting for a permanent regime
        Keithley.write('print('+source_str+".measure.i())") #Commande de mesure
        Q=Keithley.read() #La mesure est un tableau, la premiere case est la tension, la seconde le courant
        A=float((Q.replace('\n','')))
        cur_amp=A
        
        Keithley.write('print('+source_str+".measure.v())") #Commande de mesure
        Q=Keithley.read() #La mesure est un tableau, la premiere case est la tension, la seconde le courant
        A=float((Q.replace('\n','')))
        cur_volt=A
        
        res_volt.append(cur_volt)#Stockage des donnees
        res_amp.append(cur_amp)
    #### Code pour gérer acquisition spectro
        
        DAC0_VALUE = d.voltageToDACBits(4.5, dacNumber = 0, is16Bits = False)
        d.getFeedback(u3.DAC0_8(DAC0_VALUE))
        time.sleep(0.1)

        DAC0_VALUE = d.voltageToDACBits(0, dacNumber = 0, is16Bits = False)
        d.getFeedback(u3.DAC0_8(DAC0_VALUE))

        ainValue = d.getAIN(0)#Lecture de la valeur de la sortie du symphony. Quand elle sera à 0, cela voudra dire que la CCD est en train detre lue

        if (volt[i]!=volt[-1]):
            while (ainValue>2): #Attente d'un front descendant (Lecture de la CCD)
                ainValue = d.getAIN(0) 
            while (ainValue<2): #Attente d'un front montant (Expérience prete a tourner)
                ainValue = d.getAIN(0) 
        else:
            while (ainValue>2): #Attente d'un front descendant (Lecture de la CCD)
                ainValue = d.getAIN(0) 
    #####################################################################
        print("Datas for "+str(volt[i])+"V taken")


    Keithley.write(source_str+".source.output ="+ source_str+".OUTPUT_OFF")


    
plt.plot(res_volt,res_amp)
plt.xlabel("Tension en V")
plt.ylabel("Courant en A")
print("An IV curve will be plotted, close it to end the program")
plt.show()

#%% Enregistrement des donnees
rows=[res_volt,res_amp] #Donnees a enregistrer
file_name=my_path+'\IV_data_'+info_datas #Nom du fichier
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

Keithley.close()
print("Experiment over, please make sure to reload the DefaultExp.xml experiment file in Synergy the next time you use it")
input("Press enter to end the program")
