"""
Fichier de test de la communication avec la source de courant
"""

import visa

# Connection a l'appereil
rm = visa.ResourceManager()
rm.list_resources()
my_instrument = rm.open_resource('GPIB0::12::INSTR')

print(my_instrument)

# Prise de controle
my_instrument.control_ren(True)
my_instrument.clear()

# Creation d'un profile memoire (1 mA, 2V max, 10 sec, memoire 1)
my_instrument.write("B1L1I0.001V2W10X")

# Creation d'un profile memoire (2 mA, 3V max, 15 sec, memoire 2)
my_instrument.write("B2L2I0.002V3W15X")

# Mode single
my_instrument.write("P0X")

# Operate
my_instrument.write("F1X")

# Start
my_instrument.write("T4X")

# Info
print(my_instrument.resource_info)

# Relache l'instrument
my_instrument.control_ren(False)
my_instrument.close()