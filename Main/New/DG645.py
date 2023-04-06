from ctypes import *  
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
import telnetlib

class dg645():
    
    def open_ip(self,HOST):

        self.tn = telnetlib.Telnet()
        self.dg = self.tn.open(host=HOST, port=5024)
        rep=self.tn.read_until(b'\r')
        rep2=self.tn.read_until(b'\r')
        
        return rep, rep2
        
    def trig_freq_query(self):
        
        self.tn.write(b'TRAT?\n')
        rep4=self.tn.read_until(b'\r')
        rep4=rep4.decode('ascii')
        rep4=rep4.replace('\n','')
        rep4=rep4.replace('\r','')

        return float(rep4)

    
    def set_gate_APD_channel(self, channel):
        
        #1 BNC AB
        #2 BNC CD
        #3 BNC EF
        #4 BNC GH
        
        self.str_channel_gate_APD=channel

        channel=str(channel)
        channel=channel.encode('ascii')
        self.tn.write(b'LAMP '+channel+b',5.0'+b'\n')
        self.tn.write(b'LAMP?'+channel+b'\n')
        rep_amp=self.tn.read_until(b'\r')
        rep_amp=rep_amp.decode('ascii')
        rep_amp=rep_amp.replace('\n','')
        rep_amp=rep_amp.replace('\r','')
        
        self.tn.write(b'LOFF '+channel+b',-2.0'+b'\n')
        self.tn.write(b'LOFF?'+channel+b'\n')
        rep_off=self.tn.read_until(b'\r')
        rep_off=rep_off.decode('ascii')
        rep_off=rep_off.replace('\n','')
        rep_off=rep_off.replace('\r','')
        
        self.tn.write(b'LPOL '+channel+b',1'+b'\n')
        self.tn.write(b'LPOL?'+channel+b'\n')
        rep_pol=self.tn.read_until(b'\r')
        rep_pol=rep_pol.decode('ascii')
        rep_pol=rep_pol.replace('\n','')
        rep_pol=rep_pol.replace('\r','')
        
        if rep_pol=='0':
            polar='negative'
        elif rep_pol=='1':
            polar='positive'
        
        print('Channel '+str(channel)+' amplitude is '+rep_amp+ ' V, offset is '+ rep_off +' V, polarity is ' + polar)
    
    def set_synchro_PH_channel(self, channel):
        
        #1 BNC AB
        #2 BNC CD
        #3 BNC EF
        #4 BNC GH
        
        self.str_channel_synchro_PH=channel
        
        channel=str(channel)
        channel=channel.encode('ascii')
        self.tn.write(b'LAMP '+channel+b',0.6'+b'\n')
        self.tn.write(b'LAMP?'+channel+b'\n')
        rep_amp=self.tn.read_until(b'\r')
        rep_amp=rep_amp.decode('ascii')
        rep_amp=rep_amp.replace('\n','')
        rep_amp=rep_amp.replace('\r','')
        
        self.tn.write(b'LOFF '+channel+b',-0.6'+b'\n')
        self.tn.write(b'LOFF?'+channel+b'\n')
        rep_off=self.tn.read_until(b'\r')
        rep_off=rep_off.decode('ascii')
        rep_off=rep_off.replace('\n','')
        rep_off=rep_off.replace('\r','')
        
        self.tn.write(b'LPOL '+channel+b',0'+b'\n')
        self.tn.write(b'LPOL?'+channel+b'\n')
        rep_pol=self.tn.read_until(b'\r')
        rep_pol=rep_pol.decode('ascii')
        rep_pol=rep_pol.replace('\n','')
        rep_pol=rep_pol.replace('\r','')
        
        if rep_pol=='0':
            polar='negative'
        elif rep_pol=='1':
            polar='positive'
        
        print('Channel '+str(channel)+' amplitude is '+rep_amp+ ' V, offset is '+ rep_off +' V, polarity is ' + polar)
    
     
    def set_modu_AOM_channel(self, channel):
        
        #1 BNC AB
        #2 BNC CD
        #3 BNC EF
        #4 BNC GH
        
        self.str_channel_modu_AOM=channel
        
        channel=str(channel)
        channel=channel.encode('ascii')
        self.tn.write(b'LAMP '+channel+b',1.0'+b'\n')
        self.tn.write(b'LAMP?'+channel+b'\n')
        rep_amp=self.tn.read_until(b'\r')
        rep_amp=rep_amp.decode('ascii')
        rep_amp=rep_amp.replace('\n','')
        rep_amp=rep_amp.replace('\r','')
        
        self.tn.write(b'LOFF '+channel+b',0'+b'\n')
        self.tn.write(b'LOFF?'+channel+b'\n')
        rep_off=self.tn.read_until(b'\r')
        rep_off=rep_off.decode('ascii')
        rep_off=rep_off.replace('\n','')
        rep_off=rep_off.replace('\r','')
        
        self.tn.write(b'LPOL '+channel+b',1'+b'\n')
        self.tn.write(b'LPOL?'+channel+b'\n')
        rep_pol=self.tn.read_until(b'\r')
        rep_pol=rep_pol.decode('ascii')
        rep_pol=rep_pol.replace('\n','')
        rep_pol=rep_pol.replace('\r','')
        
        if rep_pol=='0':
            polar='negative'
        elif rep_pol=='1':
            polar='positive'
        
        print('Channel '+str(channel)+' amplitude is '+rep_amp+ ' V, offset is '+ rep_off +' V, polarity is ' + polar)
    
    
    def set_modu_EOM_channel(self, channel):
        
        #1 BNC AB
        #2 BNC CD
        #3 BNC EF
        #4 BNC GH
        
        self.str_channel_modu_EOM=channel
        
        channel=str(channel)
        channel=channel.encode('ascii')
        self.tn.write(b'LAMP '+channel+b',3.4'+b'\n')
        self.tn.write(b'LAMP?'+channel+b'\n')
        rep_amp=self.tn.read_until(b'\r')
        rep_amp=rep_amp.decode('ascii')
        rep_amp=rep_amp.replace('\n','')
        rep_amp=rep_amp.replace('\r','')
        
        self.tn.write(b'LOFF '+channel+b',0'+b'\n')
        self.tn.write(b'LOFF?'+channel+b'\n')
        rep_off=self.tn.read_until(b'\r')
        rep_off=rep_off.decode('ascii')
        rep_off=rep_off.replace('\n','')
        rep_off=rep_off.replace('\r','')
        
        self.tn.write(b'LPOL '+channel+b',1'+b'\n')
        self.tn.write(b'LPOL?'+channel+b'\n')
        rep_pol=self.tn.read_until(b'\r')
        rep_pol=rep_pol.decode('ascii')
        rep_pol=rep_pol.replace('\n','')
        rep_pol=rep_pol.replace('\r','')
        
        if rep_pol=='0':
            polar='negative'
        elif rep_pol=='1':
            polar='positive'
        
        print('Channel '+str(channel)+' amplitude is '+rep_amp+ ' V, offset is '+ rep_off +' V, polarity is ' + polar)
    
            
    def set_trig_rate(self,trig_rate):
        before=2e5
        trig_rate=str(trig_rate)
        trig_rate=trig_rate.encode('ascii')
        self.tn.write(b'TRAT'+trig_rate+b'\n')
        self.tn.write(b'TRAT?\n')
        rep4=self.tn.read_until(b'\r')
        rep4=rep4.decode('ascii')
        rep4=rep4.replace('\n','')
        rep4=rep4.replace('\r','')
        print('Actual frequency is '+ rep4 +' Hz')
       
    def set_delay_AB(self,delay):
        before=0
        delay=str(delay)
        delay=delay.encode('ascii')
        self.tn.write(b'DLAY 2,0,'+delay+b'\n')
        self.tn.write(b'DLAY? 2\n')
        rep4=self.tn.read_until(b'\r')
        rep4=rep4.decode('ascii')
        rep4=rep4.replace('\n','')
        rep4=rep4.replace('0,','')
        rep4=rep4.replace('\r','')
        print('Actual AB delay is '+ rep4 +' s')
        
    def set_larg_AB(self,delay):
        before=80e-9
        delay=str(delay)
        delay=delay.encode('ascii')
        self.tn.write(b'DLAY 3,2,'+delay+b'\n')
        self.tn.write(b'DLAY? 3\n')
        rep4=self.tn.read_until(b'\r')
        rep4=rep4.decode('ascii')
        rep4=rep4.replace('\n','')
        rep4=rep4.replace('0,','')
        rep4=rep4.replace('\r','')
        print('Actual AB larger is '+ rep4 +' s')
        
    def set_delay_EF(self,delay):
        before=0
        delay=str(delay)
        delay=delay.encode('ascii')
        self.tn.write(b'DLAY 6,0,'+delay+b'\n')
        self.tn.write(b'DLAY? 6\n')
        rep4=self.tn.read_until(b'\r')
        rep4=rep4.decode('ascii')
        rep4=rep4.replace('\n','')
        rep4=rep4.replace('0,','')
        rep4=rep4.replace('\r','')
        print('Actual EF delay is '+ rep4 +' s')
        
    def set_larg_EF(self,delay):
        before=80e-9
        delay=str(delay)
        delay=delay.encode('ascii')
        self.tn.write(b'DLAY 7,6,'+delay+b'\n')
        self.tn.write(b'DLAY? 7\n')
        rep4=self.tn.read_until(b'\r')
        rep4=rep4.decode('ascii')
        rep4=rep4.replace('\n','')
        rep4=rep4.replace('0,','')
        rep4=rep4.replace('\r','')
        print('Actual EF larger is '+ rep4 +' s')
        
    def set_delay_GH(self,delay):
        #In sec
        before=0
        delay=str(delay)
        delay=delay.encode('ascii')
        self.tn.write(b'DLAY 8,0,'+delay+b'\n')
        self.tn.write(b'DLAY? 8\n')
        rep4=self.tn.read_until(b'\r')
        rep4=rep4.decode('ascii')
        rep4=rep4.replace('\n','')
        rep4=rep4.replace('0,','')
        rep4=rep4.replace('\r','')
        print('Actual GH delay is '+ rep4 +' s')
        
    def set_larg_GH(self,delay):
        before=80e-9
        delay=str(delay)
        delay=delay.encode('ascii')
        self.tn.write(b'DLAY 9,8,'+delay+b'\n')
        self.tn.write(b'DLAY? 9\n')
        rep4=self.tn.read_until(b'\r')
        rep4=rep4.decode('ascii')
        rep4=rep4.replace('\n','')
        rep4=rep4.replace('0,','')
        rep4=rep4.replace('\r','')
        print('Actual GH larger is '+ rep4 +' s')
    
    def set_delay_CD(self,delay):
        before=80e-9
        delay=str(delay)
        delay=delay.encode('ascii')
        self.tn.write(b'DLAY 4,0,'+delay+b'\n')
        self.tn.write(b'DLAY? 4\n')
        rep4=self.tn.read_until(b'\r')
        rep4=rep4.decode('ascii')
        rep4=rep4.replace('\n','')
        rep4=rep4.replace('0,','')
        rep4=rep4.replace('\r','')
        print('Actual CD larger is '+ rep4 +' s')
        
    def set_larg_CD(self,delay):
        before=80e-9
        delay=str(delay)
        delay=delay.encode('ascii')
        self.tn.write(b'DLAY 5,4,'+delay+b'\n')
        self.tn.write(b'DLAY? 5\n')
        rep4=self.tn.read_until(b'\r')
        rep4=rep4.decode('ascii')
        rep4=rep4.replace('\n','')
        rep4=rep4.replace('0,','')
        rep4=rep4.replace('\r','')
        print('Actual CD delay is '+ rep4 +' s')
    
    def set_larg_AOM(self,larg):
        
        #1 BNC AB
        if self.str_channel_modu_AOM==1 :
            self.set_larg_AB(larg)
        #2 BNC CD
        elif self.str_channel_modu_AOM==2 :
            self.set_larg_CD(larg)
        #3 BNC EF
        elif self.str_channel_modu_AOM==3 :
            self.set_larg_EF(larg)
        #4 BNC GH
        elif self.str_channel_modu_AOM==4 :
            self.set_larg_GH(larg)
            
    def set_delay_AOM(self,larg):
        
        #1 BNC AB
        if self.str_channel_modu_AOM==1 :
            self.set_delay_AB(larg)
        #2 BNC CD
        elif self.str_channel_modu_AOM==2 :
            self.set_delay_CD(larg)
        #3 BNC EF
        elif self.str_channel_modu_AOM==3 :
            self.set_delay_EF(larg)
        #4 BNC GH
        elif self.str_channel_modu_AOM==4 :
            self.set_delay_GH(larg)
    
    def set_larg_APD(self,larg):
        
        #1 BNC AB
        if self.str_channel_gate_APD==1 :
            self.set_larg_AB(larg)
        #2 BNC CD
        elif self.str_channel_gate_APD==2 :
            self.set_larg_CD(larg)
        #3 BNC EF
        elif self.str_channel_gate_APD==3 :
            self.set_larg_EF(larg)
        #4 BNC GH
        elif self.str_channel_gate_APD==4 :
            self.set_larg_GH(larg)
    
    def set_delay_APD(self,larg):
        
        #1 BNC AB
        if self.str_channel_gate_APD==1 :
            self.set_delay_AB(larg)
        #2 BNC CD
        elif self.str_channel_gate_APD==2 :
            self.set_delay_CD(larg)
        #3 BNC EF
        elif self.str_channel_gate_APD==3 :
            self.set_delay_EF(larg)
        #4 BNC GH
        elif self.str_channel_gate_APD==4 :
            self.set_delay_GH(larg)
    
    def set_larg_PH(self,larg):
        
        #1 BNC AB
        if self.str_channel_synchro_PH==1 :
            self.set_larg_AB(larg)
        #2 BNC CD
        elif self.str_channel_synchro_PH==2 :
            self.set_larg_CD(larg)
        #3 BNC EF
        elif self.str_channel_synchro_PH==3 :
            self.set_larg_EF(larg)
        #4 BNC GH
        elif self.str_channel_synchro_PH==4 :
            self.set_larg_GH(larg)
            
    def set_delay_PH(self,larg):
        
        #1 BNC AB
        if self.str_channel_synchro_PH==1 :
            self.set_delay_AB(larg)
        #2 BNC CD
        elif self.str_channel_synchro_PH==2 :
            self.set_delay_CD(larg)
        #3 BNC EF
        elif self.str_channel_synchro_PH==3 :
            self.set_delay_EF(larg)
        #4 BNC GH
        elif self.str_channel_synchro_PH==4 :
            self.set_delay_GH(larg)
    
    def set_larg_EOM(self,larg):
        
        #1 BNC AB
        if self.str_channel_modu_EOM==1 :
            self.set_larg_AB(larg)
        #2 BNC CD
        elif self.str_channel_modu_EOM==2 :
            self.set_larg_CD(larg)
        #3 BNC EF
        elif self.str_channel_modu_EOM==3 :
            self.set_larg_EF(larg)
        #4 BNC GH
        elif self.str_channel_modu_EOM==4 :
            self.set_larg_GH(larg)
            
    def set_delay_EOM(self,larg):
        
        #1 BNC AB
        if self.str_channel_modu_EOM==1 :
            self.set_delay_AB(larg)
        #2 BNC CD
        elif self.str_channel_modu_EOM==2 :
            self.set_delay_CD(larg)
        #3 BNC EF
        elif self.str_channel_modu_EOM==3 :
            self.set_delay_EF(larg)
        #4 BNC GH
        elif self.str_channel_modu_EOM==4 :
            self.set_delay_GH(larg)
    
    def close(self):
        self.tn.close()