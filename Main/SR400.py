import serial

class mySR400():
    
    def open_sr(self,com_string):
        
        self.ser = serial.Serial(com_string, 9600, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
        self.ser.write(b"CR\n") #Reset Counters
        self.ser.write(b"SS \n") #Set counter A and B and Trigger
        self.ser.readlines()

        
    def setup_sr(self):       
        self.ser.write(b"CM 0\n") #Set counter A and B and Trigger
        self.ser.write(b"CI 0,1\n") #Set counter A on input 1
        self.ser.write(b"CI 1,1\n") #Set counter B on input 1
        self.ser.write(b"CI 2,3\n") #Set T on trigger input  
        self.ser.write(b"GM 0,1\n") #Set A counter gate fixed
        self.ser.write(b"GM 1,1\n") #Set B counter gate fixed
        self.ser.write(b"NP 1\n") # Number of counting after trigger value reached = 1
        self.ser.write(b"NE 0\n") #Counting will stop  after trigger value reached
        self.ser.write(b"DT 2E-3\n") #Minimum dwell time
        self.ser.write(b"TS 0\n") #Trigger on rising edge
        self.ser.write(b"TL 0.5\n") #Trigger at 0.5V
        self.ser.write(b"DS 0,0\n") #Rising slope for counter A
        self.ser.write(b"DS 1,0\n") #Rising slope for counter B
        self.ser.write(b"DM 0,0\n") #Discriminator mode fixed
        self.ser.write(b"DM 1,0\n") # //
        self.ser.write(b"DM 2,0\n") # //
        self.ser.write(b"DL 0,0.3\n") #Discriminator levels @ 0.3V (the max)
        self.ser.write(b"DL 1,0.3\n") # //
        self.ser.write(b"DL 2,0.3\n") # //
        self.ser.write(b"SS \n") #Set counter A and B and Trigger
        self.ser.readlines()

    def is_data_ready_query(self):
        self.ser.readlines()
        self.ser.write(b"SS \n") #Set counter A and B and Trigger
        string=self.ser.readline()
        biny=bin(int(string.decode()))[8]
        return biny


    def beg_count(self, n_per,delay_pump,width_pump,delay_probe,width_probe):
        
        self.ser.write(b"CP 2,"+str(n_per).encode()+b"\n") #Set number of trigger counts
        self.ser.write(b"GD 0,"+str(delay_pump).encode()+b"\n") #Set delay for counter A, the pump, should be 0
        self.ser.write(b"GD 1,"+str(delay_probe).encode()+b"\n") #Set delay for counter B, the probe
        self.ser.write(b"GW 0,"+str(width_pump).encode()+b"\n") #Set delay for counter B, the probe
        self.ser.write(b"GW 1,"+str(width_probe).encode()+b"\n") #Set delay for counter B, the probe
  
        self.ser.write(b"CS\n") #Start counting
    
    def recover_count(self):
        self.ser.write(b"XA \n")
        count_A=int(self.ser.readline().decode())
        self.ser.write(b"XB \n")
        count_B=int(self.ser.readline().decode())
        return count_A, count_B
    
    def close_sr(self):
        self.ser.close()
#ser.close()