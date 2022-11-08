import matplotlib.pyplot as plt
import numpy as np
from aerodiode import Tombak
import time
tombak = Tombak('COM5')
INSTRUCT_FUNCTIONING_MODE_OFF = 0
PULSE_IN_PHOTODIODE = 3

set_freq_divider=100000
set_delay_pulse=0
set_functionning_mode = tombak.PULSE_GENERATOR
set_pulse_width = 100



print("Read Configuration")
print("INSTRUCT_FUNCTIONING_MODE = ",
tombak.read_status_instruction(tombak.INSTRUCT_FUNCTIONING_MODE))
print("INSTRUCT_PULSE_IN_SRC = ", tombak.read_status_instruction(tombak.INSTRUCT_PULSE_IN_SRC))
print("INSTRUCT_PULSE_IN_FREQUENCY_DIV = ",
tombak.read_freq_instruction(tombak.INSTRUCT_PULSE_IN_FREQUENCY_DIV))
print("INSTRUCT_SYNC_OUT_1_SRC = ",
tombak.read_status_instruction(tombak.INSTRUCT_SYNC_OUT_1_SRC))
print("INSTRUCT_PULSE_OUT_WIDTH = ",
tombak.read_time_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH))

# print("Set Configuration")

# tombak.set_status_instruction(tombak.INSTRUCT_FUNCTIONING_MODE, set_functionning_mode)
# tombak.set_status_instruction(tombak.INSTRUCT_PULSE_IN_SRC, tombak.DIRECT)#ok
# tombak.set_status_instruction(tombak.INSTRUCT_TRIGGER_SRC, tombak.INT)#
# tombak.set_status_instruction(tombak.INSTRUCT_SYNC_OUT_1_SRC, tombak.DELAY)#ok
# tombak.set_status_instruction(tombak.INSTRUCT_GATE_CONTROL, tombak.NO_GATE)#ok
# tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_WIDTH, set_pulse_width)#ok
# tombak.set_time_instruction(tombak.INSTRUCT_PULSE_OUT_DELAY, set_delay_pulse)#ok
# tombak.apply_all()
# print("Set Configuration terminated")


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


tombak.close()

