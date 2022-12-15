import u3
import time

####Creation d'un front montant
d = u3.U3()
DAC0_VALUE = d.voltageToDACBits(4.5, dacNumber = 0, is16Bits = False)
d.getFeedback(u3.DAC0_8(DAC0_VALUE))
time.sleep(0.1)

DAC0_VALUE = d.voltageToDACBits(0, dacNumber = 0, is16Bits = False)
d.getFeedback(u3.DAC0_8(DAC0_VALUE))
###


ainValue = d.getAIN(0)#Lecture de la valeur de la sortie du symphony. Quand elle sera à 0, cela voudra dire que la CCD est en train detre lue

while (ainValue>2): #Attente d'un front descendant (Lecture de la CCD)
    ainValue = d.getAIN(0) 
while (ainValue<2): #Attente d'un front montant (Expérience prete a tourner)
    ainValue = d.getAIN(0) 
# time.sleep(5)

# DAC0_VALUE = d.voltageToDACBits(4.5, dacNumber = 0, is16Bits = False)
# d.getFeedback(u3.DAC0_8(DAC0_VALUE))
# time.sleep(0.1)

# DAC0_VALUE = d.voltageToDACBits(0, dacNumber = 0, is16Bits = False)
# d.getFeedback(u3.DAC0_8(DAC0_VALUE))
# ainValue = d.getAIN(0)
# print('here')

# while (ainValue>2):
#     ainValue = d.getAIN(0) 
# while (ainValue<2):
#     ainValue = d.getAIN(0) 
# # time.sleep(1)

# # time.sleep(5)

# DAC0_VALUE = d.voltageToDACBits(4.5, dacNumber = 0, is16Bits = False)
# d.getFeedback(u3.DAC0_8(DAC0_VALUE))

# time.sleep(0.1)

# DAC0_VALUE = d.voltageToDACBits(0, dacNumber = 0, is16Bits = False)
# d.getFeedback(u3.DAC0_8(DAC0_VALUE))
# ainValue = d.getAIN(0)


# print('end')