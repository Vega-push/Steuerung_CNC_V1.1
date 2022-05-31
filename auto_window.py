import tkinter as tk
import tkinter.scrolledtext
import tkinter.filedialog
import controls
import automatic

def erstelle_auto_window(master, steuerung, antriebsstrang):

    ###################
    # Button Funktionen
    ###################
    def get_back():
        """auto_window zerstoeren und main_window wieder anzeigen"""
        auto_window.destroy()
        master.state("normal")
        master.lift()


    def datei_speichern():
        """speichert den aktuellen Inhalt des Textfeldes in eine .txt Datei"""
        textfeld_inhalt = tf_skriptbox.get("1.0","end")
        datei = tk.filedialog.asksaveasfile(master=auto_window, mode="w", defaultextension="txt", filetypes=[("Text file", "*.txt")])
        datei.write(textfeld_inhalt)
        datei.close()


    def datei_laden():
        """laden einer .txt Datei in das Textfeld"""
        datei = tk.filedialog.askopenfile(master=auto_window, mode="r", filetypes=[("Text file", "*.txt")])
        if datei:
            tf_skriptbox.insert("1.0", datei.read())
            datei.close()


    def starte_programm():
        """gewünschte Datei laden, auf Fehler überprüfen, wenn i.O ausführen"""
        datei = tk.filedialog.askopenfile()
        skript = automatic.skript_laden(datei.name)
        # Schrittmodus ausgewählt ja/nein
        flag_skript, zeile = automatic.skript_ueberpruefen(skript)
        if flag_skript:
            if single_flag.get():
                automatic.skript_ausfuehren(steuerung, antriebsstrang, skript, True)
            else:
                automatic.skript_ausfuehren(steuerung, antriebsstrang, skript, False)
            tf_skriptbox.delete("1.0","end")
            tf_skriptbox.insert("end", "Skript erfolgreich beendet!!\n")
        else:
            tf_skriptbox.insert("end", f"Fehler im Skript in Zeile {zeile}!\n")


    def befehlsliste_anzeigen():
        """Anzeigen von möglichen Befehlen mit Beispielen für das Skript"""
        help_window = tk.Toplevel(auto_window)
        help_window.title("Befehlsliste")
        tf_helpbox = tk.scrolledtext.ScrolledText(help_window, width=80, height=35, state="normal")
        tf_helpbox.grid(column=0, row=0, padx=10, pady=5)
        try:
            with open("Befehlsliste.txt") as f:
                tf_helpbox.insert("end", f.read())
        except FileNotFoundError:
            print("Kein Skript geladen! Ausgewaehlte Datei existiert nicht.")
            exit()
        tf_helpbox.config(state="disabled")


    # verstecke das main_window
    master.state("withdraw")

    #######################
    # auto_window erstellen
    #######################
    auto_window = tk.Toplevel(master)
    auto_window.title("Automatischer Modus")
    # Widgets erstellen
    btn_start = tk.Button(auto_window, bd=3, font="Arial", text="Start", width=15, height=1, command=starte_programm)
    btn_save = tk.Button(auto_window, bd=3, font="Arial", text="Speichern", width=15, height=1, command=datei_speichern)
    btn_load = tk.Button(auto_window, bd=3, font="Arial", text="Laden", width=15, height=1, command=datei_laden)
    btn_help = tk.Button(auto_window, bd=3, font="Arial", text="Hilfe", width=15, height=1, command=befehlsliste_anzeigen)
    single_flag = tk.IntVar()
    check_single = tk.Checkbutton(auto_window, bd=3, font="Arial", text="Schrittmodus", variable=single_flag)
    tf_skriptbox = tk.scrolledtext.ScrolledText(auto_window, width=80, height=35, state="normal")
    # Widgets "packen"
    tf_skriptbox.grid(column=0, columnspan=3, row=0, padx=10, pady=5)
    btn_start.grid(column=0, row=1, padx=10, pady=5)
    btn_save.grid(column=1, row=1, padx=10, pady=5)
    btn_load.grid(column=2, row=1, padx=10, pady=5)
    btn_help.grid(column=1, row=2, padx=10, pady=5)
    check_single.grid(column=0, row=2, padx=10, pady=5)
    # Standard Event-Handling ueberschreiben
    auto_window.protocol("WM_DELETE_WINDOW", get_back)
