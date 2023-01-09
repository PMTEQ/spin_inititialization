from ctypes import *  
import sys
import time
import matplotlib.pyplot as plt
import numpy as np

class PH: 
    
    def __init__(self):
        self.phdll = cdll.LoadLibrary("phlib.dll") #Chargement de la dll
        
    def open_ph(self):
        #Avec les paramètres trouvés grâce au logiciel constructeur, permet d'ouvrir et de paramétrer le PicoHarp dans python
        self.HISTCHAN  =  65536;	    
        self.MODE_HIST =  c_int(0);
        self.dev_number=c_int(0)
        self.serial=(c_char * 8)()
        print("Opening the picoHarp")

        ret=self.phdll.PH_OpenDevice(self.dev_number,byref(self.serial))
      
        if ret==0:
            print("PicoHarp succesfully opened")
        else:
            print("PicoHarp opening failed")
            sys.exit()

        print("Initializing")
        
        ret=self.phdll.PH_Initialize(self.dev_number,self.MODE_HIST)
        print("Calibrating")
        ret=self.phdll.PH_Calibrate(self.dev_number)
        
        # Settings for the measurement

        self.Offset = 0;       #  you can change this
        self.RES = 4
        self.Stop_of_ok=0 #Dont stop at overflow
        self.Stop_count=65535 
        self.range_res=0

        #Sync chanel:
        self.ZC_sync=10
        self.DISCR_sync=200
        self.DIV_sync=1

        #Channel 1:

        self.ZC_ch1=20
        self.DISCR_ch1=500
        
        print("Setting up channels")
        ret=self.phdll.PH_SetCFDLevel(self.dev_number,c_int(0),self.DISCR_sync)
        ret=self.phdll.PH_SetCFDLevel(self.dev_number,c_int(1),self.DISCR_ch1)
        ret=self.phdll.PH_SetCFDZeroCross(self.dev_number,c_int(0),self.ZC_sync)
        ret=self.phdll.PH_SetCFDZeroCross(self.dev_number,c_int(1),self.ZC_ch1)
        ret=self.phdll.PH_SetSyncDiv(self.dev_number,c_int(1))
        
        ret=self.phdll.PH_SetStopOverflow(self.dev_number,self.Stop_of_ok,self.Stop_count)
        
        ret=self.phdll.PH_SetRange(self.dev_number,self.range_res)
        
        ret=self.phdll.PH_SetOffset(self.dev_number,self.Offset)
                
        ret=self.phdll.PH_ClearHistMem(self.dev_number,0)

        time.sleep(2)
        
        print("Setting up done")

    def set_range(self, user_range):
        #Permet de paramétrer la résolution des mesures
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
        self.range_res=user_range
        ret=self.phdll.PH_SetRange(self.dev_number,c_int(user_range))

    def start_measure_with_plot(self, Tacq):
        #Tacq en millisecondes
        #Réalise une mesure de la statistique temporelle moyennée pendant le temps T_acq. Toute les secondes une visualisation de cette statistique est mise à jour
        #Renvoie un vecteur contenant les valeurs temporelles et un vecteur contenant le nombre de coups associé à ces valeurs temporelles.
        ret=self.phdll.PH_ClearHistMem(self.dev_number,0)

        #in ms
        Counts_c=(c_uint*self.HISTCHAN)()
        Counts=np.zeros(self.HISTCHAN)

        print("Starting measures")
        ret=self.phdll.PH_StartMeas(self.dev_number,Tacq)
        tdeb=time.time()

        plt.ion()


        t = 2**(self.range_res) * np.linspace(0,65535,65536) * 10**-3
        figure, ax = plt.subplots(figsize=(5,5))
        plot1, = ax.plot(t, Counts)
        plt.ylim(0,100)

        plt.show()
        
        while (time.time()-tdeb)<((Tacq/1000)+0.5):
            time.sleep(1)
            count_rate_APD=self.phdll.PH_GetCountRate(self.dev_number,1)
            print('APD count rate (en cps): ' + str(count_rate_APD)+ ' // Time remaining (en sec) : ' + str((Tacq/1000)-(time.time()-tdeb)))
            ret=self.phdll.PH_GetBlock(self.dev_number,byref(Counts_c),0)
            for i in range(self.HISTCHAN):
                Counts[i]=Counts_c[i]
            plot1.set_xdata(t)
            plot1.set_ydata(Counts)
            figure.canvas.draw()
            figure.canvas.flush_events()
        
        ret=self.phdll.PH_StopMeas(self.dev_number,Tacq)
        test = (self.phdll.PH_CTCStatus(self.dev_number))
        plt.close()
        print("End measures")
        return Counts,t
    def start_measure(self, Tacq):
        #Tacq en millisecondes
        #Réalise une mesure de la statistique temporelle moyennée pendant le temps T_acq. Il n'y a pas de visualisation de la statistique
        #Renvoie un vecteur contenant les valeurs temporelles et un vecteur contenant le nombre de coups associé à ces valeurs temporelles.
        
        ret=self.phdll.PH_ClearHistMem(self.dev_number,0)

        Counts_c=(c_uint*self.HISTCHAN)()
        Counts=np.zeros(self.HISTCHAN)

        print("Starting measures")
        ret=self.phdll.PH_StartMeas(self.dev_number,Tacq)
        tdeb=time.time()

        t =  2**(self.range_res) * np.linspace(0,65535,65536) * 10**-3
        
      
        while (time.time()-tdeb)<((Tacq/1000)+0.5):
            time.sleep(1)
            count_rate_APD=self.phdll.PH_GetCountRate(self.dev_number,1)
            print('APD count rate (en cps): ' + str(count_rate_APD)+ ' // Time remaining (en sec) : ' + str((Tacq/1000)-(time.time()-tdeb)))
            
           
        ret=self.phdll.PH_GetBlock(self.dev_number,byref(Counts_c),0)
        for i in range(self.HISTCHAN):
            Counts[i]=Counts_c[i]
            
        ret=self.phdll.PH_StopMeas(self.dev_number,Tacq)
        test = (self.phdll.PH_CTCStatus(self.dev_number))
        print("End measures")
        return Counts,t

    def close_APD(self):
        #Coupe la communication entre Python et le PicoHarp
        self.phdll.PH_CloseDevice(c_int(0))
