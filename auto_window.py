import tkinter as tk
import tkinter.scrolledtext
import tkinter.filedialog
import controls

def erstelle_auto_window(master, steuerung, antriebsstrang):

    def get_back():
        auto_window.destroy()
        # main_window anzeigen und auf oberste Ebene heben
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

    # verstecke das main_window
    master.state("withdraw")
    # auto_window erstellen
    auto_window = tk.Toplevel(master)
    auto_window.title("Automatischer Modus")
    # Widgets erstellen
    btn_start = tk.Button(auto_window, bd=3, font="Arial", text="Start", width=15, height=1)
    btn_stop = tk.Button(auto_window, bd=3, font="Arial", text="Stop", width=15, height=1)
    btn_save = tk.Button(auto_window, bd=3, font="Arial", text="Speichern", width=15, height=1, command=datei_speichern)
    btn_load = tk.Button(auto_window, bd=3, font="Arial", text="Laden", width=15, height=1, command=datei_laden)
    btn_reset = tk.Button(auto_window, bd=3, font="Arial", text="Reset", width=15, height=1)
    check_single = tk.Checkbutton(auto_window, bd=3, font="Arial", text="Schrittmodus")
    tf_skriptbox = tk.scrolledtext.ScrolledText(auto_window, width=80, height=35, state="normal")
    # Widgets "packen"
    tf_skriptbox.grid(column=0, columnspan=3, row=0, padx=10, pady=5)
    btn_start.grid(column=0, row=1, padx=10, pady=5)
    btn_stop.grid(column=1, row=1, padx=10, pady=5)
    btn_reset.grid(column=2, row=1, padx=10, pady=5)
    btn_save.grid(column=0, row=2, padx=10, pady=5)
    btn_load.grid(column=1, row=2, padx=10, pady=5)
    check_single.grid(column=2, row=2, padx=10, pady=5)
    # Standard Event-Handling ueberschreiben
    auto_window.protocol("WM_DELETE_WINDOW", get_back)
