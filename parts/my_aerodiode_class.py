import matplotlib.pyplot as plt
import numpy as np
from aerodiode import Tombak
import time

# set_freq_divider=100000
# set_delay_pulse=0
# set_pulse_width = 100

class my_tombak():
    
    def __init__(self):
        
        self.INSTRUCT_FUNCTIONING_MODE_OFF = 0
        self.PULSE_IN_PHOTODIODE = 3
        
    def open_my_tombak(self, COM):
        
        self.tombak = Tombak('COM5')
        
    def close_my_tombak(self):
        self.tombak.set_status_instruction(self.tombak.INSTRUCT_FUNCTIONING_MODE, self.INSTRUCT_FUNCTIONING_MODE_OFF)
        self.tombak.apply_all()
        self.tombak.close()

    def read_my_config(self):


        print("Read Configuration")
        print("INSTRUCT_FUNCTIONING_MODE = ",
        self.tombak.read_status_instruction(self.tombak.INSTRUCT_FUNCTIONING_MODE))
        print("INSTRUCT_PULSE_IN_SRC = ", self.tombak.read_status_instruction(self.tombak.INSTRUCT_PULSE_IN_SRC))
        print("INSTRUCT_PULSE_IN_FREQUENCY_DIV = ",
        self.tombak.read_freq_instruction(self.tombak.INSTRUCT_PULSE_IN_FREQUENCY_DIV))
        print("INSTRUCT_SYNC_OUT_1_SRC = ",
        self.tombak.read_status_instruction(self.tombak.INSTRUCT_SYNC_OUT_1_SRC))
        print("INSTRUCT_PULSE_OUT_WIDTH = ",
        self.tombak.read_time_instruction(self.tombak.INSTRUCT_PULSE_OUT_WIDTH))
        
    def pulse_gene_no_gate_trig_clock_sync_1_trigger(self, delay_pulse, width_pulse, divider):
        
        set_functionning_mode = self.tombak.PULSE_GENERATOR
        
        print("Set Configuration")
        
        self.tombak.set_status_instruction(self.tombak.INSTRUCT_FUNCTIONING_MODE, set_functionning_mode)
        self.tombak.set_status_instruction(self.tombak.INSTRUCT_PULSE_IN_SRC, self.tombak.DIRECT)#ok
        self.tombak.set_status_instruction(self.tombak.INSTRUCT_TRIGGER_SRC, self.tombak.INT)#
        self.tombak.set_status_instruction(self.tombak.INSTRUCT_SYNC_OUT_1_SRC, self.tombak.TRIGGER)#ok
        self.tombak.set_status_instruction(self.tombak.INSTRUCT_GATE_CONTROL, self.tombak.NO_GATE)#ok
        self.tombak.set_time_instruction(self.tombak.INSTRUCT_PULSE_OUT_WIDTH, width_pulse)#ok
        self.tombak.set_time_instruction(self.tombak.INSTRUCT_PULSE_OUT_DELAY, delay_pulse)#ok
        self.tombak.set_integer_instruction(self.tombak.INSTRUCT_PULSE_IN_FREQUENCY_DIV, divider)

        self.tombak.apply_all()
        print("Set Configuration terminated")
        
    def pulse_gene_no_gate_trig_PD_sync_1_trigger(self, delay_pulse, width_pulse, divider, threshold):
        
        
        print("Set Configuration")
        
        set_functionning_mode = 1
        
        self.tombak.set_status_instruction(self.tombak.INSTRUCT_FUNCTIONING_MODE, set_functionning_mode)

        self.tombak.set_status_instruction(self.tombak.INSTRUCT_PULSE_IN_SRC, self.PULSE_IN_PHOTODIODE )#ok
        self.tombak.set_status_instruction(self.tombak.INSTRUCT_TRIGGER_SRC, self.tombak.INT)#
        self.tombak.set_status_instruction(self.tombak.INSTRUCT_SYNC_OUT_1_SRC, self.tombak.TRIGGER)#ok
        self.tombak.set_status_instruction(self.tombak.INSTRUCT_GATE_CONTROL, self.tombak.NO_GATE)#ok
        self.tombak.set_time_instruction(self.tombak.INSTRUCT_PULSE_OUT_WIDTH, width_pulse)#ok
        self.tombak.set_time_instruction(self.tombak.INSTRUCT_PULSE_OUT_DELAY, delay_pulse)#ok
        self.tombak.set_integer_instruction(self.tombak.INSTRUCT_PULSE_IN_FREQUENCY_DIV, divider)
        self.tombak.set_voltage_instruction(self.tombak.INSTRUCT_PULSE_IN_THRESHOLD,threshold)

        self.tombak.apply_all()
        print("Set Configuration terminated")
        
    def off_out(self):
        self.tombak.set_status_instruction(self.tombak.INSTRUCT_FUNCTIONING_MODE, self.INSTRUCT_FUNCTIONING_MODE_OFF)
        self.tombak.apply_all()


# print("Read Configuration")
# print("INSTRUCT_FUNCTIONING_MODE = ",
# tombak.read_status_instruction(tombak.INSTRUCT_FUNCTIONING_MODE))
# print("INSTRUCT_PULSE_IN_SRC = ", tombak.read_status_instruction(tombak.INSTRUCT_PULSE_IN_SRC))
# print("INSTRUCT_PULSE_IN_FREQUENCY_DIV = ",
# tombak.read_freq_instruction(tombak.INSTRUCT_PULSE_IN_FREQUENCY_DIV))
# print("INSTRUCT_SYNC_OUT_1_SRC = ",
# tombak.read_status_instruction(tombak.INSTRUCT_SYNC_OUT_1_SRC))
# print("INSTRUCT_PULSE_OUT_WIDTH = ",
# tombak.read_time_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH))

# time.sleep(15)

# tombak.set_status_instruction(tombak.INSTRUCT_FUNCTIONING_MODE, INSTRUCT_FUNCTIONING_MODE_OFF)
# tombak.apply_all()


# tombak.close()

