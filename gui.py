import tkinter as tk
import tkinter.scrolledtext
import controls

def erstelle_main_window(master, steuerung, antriebsstrang):
    btn_ref = tk.Button(master, bd=3, font="Arial", text="Referenzfahrt", width=30, height=2, command= lambda: controls.np_referenzfahrt(steuerung, antriebsstrang))
    btn_auto = tk.Button(master, bd=3, font="Arial", text="Auto-Mode", width=30, height=2)
    mainframe = tk.Frame(master)
    tf_infobox = tk.scrolledtext.ScrolledText(master, undo=True)

    # Achsenauswahl erstellen
    axis = tk.IntVar(mainframe, 2)
    btn_x = tk.Radiobutton(mainframe, text='X-Achse', variable=axis, value=1, width=30, height=2, command= lambda: controls.get_stringVar(axis))
    btn_y = tk.Radiobutton(mainframe, text='Y-Achse', variable=axis, value=0, width=30, height=2, command= lambda: controls.get_stringVar(axis))
    btn_z = tk.Radiobutton(mainframe, text='Z-Achse', variable=axis, value=2, width=30, height=2, command= lambda: controls.get_stringVar(axis))

    # Geschwindigkeitsauswahl erstellen
    weg = tk.IntVar(value=1)
    btn_01 = tk.Radiobutton(mainframe, text='1 mm', variable=weg, value=1, command= lambda: controls.get_intVar(weg))
    btn_1 = tk.Radiobutton(mainframe, text='10 mm', variable=weg, value=10, command= lambda: controls.get_intVar(weg))
    btn_10 = tk.Radiobutton(mainframe, text='50 mm', variable=weg, value=50, command= lambda: controls.get_intVar(weg))

    # Richtungs-Buttons erstellen main_window
    btn_plus = tk.Button(mainframe, bd=3, font="Arial", text=" + ", width=10, height=2, command= lambda: controls.gui_verfahre_achse(steuerung, antriebsstrang, axis, weg))
    btn_minus = tk.Button(mainframe, bd=3, font="Arial", text=" - ", width=10, height=2)

    # Widgets ins Grid von root "packen"
    btn_ref.grid(column=0, row=0, padx=30, pady=15)
    btn_auto.grid(column=1, row=0, padx=30, pady=15)
    tf_infobox.grid(column=0, columnspan=2, row=2, rowspan=5, padx=30, pady=15)
    # Widgets in mainframe "packen"
    mainframe.grid(column=0, columnspan=2, row=1, padx=30, pady=15)
    btn_x.grid(column=0, columnspan=2, row=0)
    btn_y.grid(column=2, columnspan=2, row=0)
    btn_z.grid(column=4, columnspan=2, row=0)
    btn_01.grid(column=0, columnspan=2, row=1)
    btn_1.grid(column=2, columnspan=2, row=1)
    btn_10.grid(column=4, columnspan=2, row=1)
    btn_plus.grid(column=0, columnspan=3, row=2, padx=30, pady=15)
    btn_minus.grid(column=3, columnspan=3, row=2, padx=30, pady=15)
