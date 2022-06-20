import PyTrinamic
import tkinter as tk
import config
from gui import erstelle_main_window
from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamic.modules.TMCM3110.TMCM_3110 import TMCM_3110
from handle_data import Handle_Data

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
# Verbindung trennen - muss am Ende stehen
my_interface.close()
