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
        
    def trig_freq_query(self):
        
        self.tn.write(b'TRAT?\n')
        rep4=self.tn.read_until(b'\r')
        rep4=rep4.decode('ascii')
        rep4=rep4.replace('\n','')
        rep4=rep4.replace('\r','')
        
        return float(rep4)
    
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
       
    def set_delay_AOM(self,delay):
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
        print('Actual AOM delay is '+ rep4 +' s')
        
    def set_larg_AOM(self,delay):
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
        print('Actual AOM larger is '+ rep4 +' s')
        
    def set_delay_sync(self,delay):
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
        print('Actual sync delay is '+ rep4 +' s')
        
    def set_larg_sync(self,delay):
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
        print('Actual sync larger is '+ rep4 +' s')
        
    def set_delay_gate(self,delay):
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
        print('Actual gate delay is '+ rep4 +' s')
        
    def set_larg_gate(self,delay):
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
        print('Actual gate larger is '+ rep4 +' s')
        
    def close(self):
        self.tn.close()

# tn.write(b'*IDN?\n')
# rep3=tn.read_until(b'\r')



# time.sleep(5)




