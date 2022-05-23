import PyTrinamic
import tkinter as tk
import config
import automatic
import controls
from gui import erstelle_main_window
from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamic.modules.TMCM3110.TMCM_3110 import TMCM_3110
import time

# Verbindung herstellen und Steuerungsobjekt anlegen
PyTrinamic.showInfo()
connectionManager = ConnectionManager()
my_interface = connectionManager.connect()
tmcm_3110 = TMCM_3110(my_interface)

# Config laden und maschine mit Antriebsstrangdaten erzeugen
maschinendaten = config.load_config(tmcm_3110)

# GUI erstellen
root = tk.Tk()
root.title("Steuerung CNC")
erstelle_main_window(root, tmcm_3110, maschinendaten)



tk.mainloop()

# NP setzen
# controls.np_referenzfahrt(tmcm_3110, maschinendaten)
# ein Skript laden
# aktuelles_skript = automatic.skript_laden()
# Skript ueberpruefen, wenn i.O. ausfuehren
# if automatic.skript_ueberpruefen(aktuelles_skript):
#     exit()
# else:
#     automatic.skript_ausfuehren(tmcm_3110, maschinendaten, aktuelles_skript, step=True)

# Verbindung trennen - muss am Ende stehen
my_interface.close()
