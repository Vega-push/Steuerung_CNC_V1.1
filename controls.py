from config import load_config
import csv

##############################
# Maschinen Kontrollfunktionen
##############################
def np_referenzfahrt(steuerung, antriebsstrang, text):
    """setze für alle Achsen den NP"""
    achsen_verfahrwege = {
    "y": int(antriebsstrang["y_max_weg"]),
    "x": int(antriebsstrang["x_max_weg"]),
    "z": int(antriebsstrang["z_max_weg"])
    }
    # fahre jede Achse gegen Referenzschalter und setze NP
    for i, item in enumerate(achsen_verfahrwege):
        steuerung.rotate(i,1500)
        text.insert("end", f"Fahre {item.upper()}-Achse in rechten Referenzschalter!\n")
        text.update()
        text.yview("end")
        while not(steuerung.getAxisParameter(10, i)): # 10 =right limit switch state
            pass
        steuerung.stop(i)
        # fahre max Achsenverfahrweg vom Schalter zurueck
        steuerung.moveBy(i, -1*achsen_verfahrwege[item], 1500)
        text.insert("end", f"Fahre {item.upper()}-Achse um {achsen_verfahrwege[item]}pps zum NP!\n")
        text.update()
        text.yview("end")
        while not(steuerung.positionReached(i)):
            pass
        steuerung.stop(i)
        # NP setzen
        steuerung.setAxisParameter(apType=1, motor=i, value=0)
        text.insert("end", f"NP der Achse {item.upper()} gesetzt.\n")
        text.update()
        text.yview("end")

    load_config(steuerung)
    text.insert("end","Nullpunkte erfolgreich gesetzt!")
    text.update()
    text.yview("end")


def pps_in_mm(steuerung, antrieb, achse, pulse):
    """Rotatorische Bewegung (pps) in eine translatorische Bewegung (mm)."""
    vollschritt = float(antrieb["vollschritt"])
    mic_step_res = 2**steuerung.getAxisParameter(140, achse)
    steigung = float(antrieb["steigung_mm_pro_u"])
    uebersetzung = float(antrieb["getriebe_uebersetzung"])
    return round(((pulse/((360/vollschritt)*mic_step_res))*steigung*uebersetzung),3)


def mm_in_pps(steuerung, antrieb, achse, strecke):
    """Translatorische Bewegung (mm) in rotatorische Bewegung umrechnen(pps)"""
    vollschritt = float(antrieb["vollschritt"])
    mic_step_res = 2**steuerung.getAxisParameter(140, achse)
    steigung = float(antrieb["steigung_mm_pro_u"])
    uebersetzung = float(antrieb["getriebe_uebersetzung"])
    return int((strecke*(360/vollschritt)*mic_step_res)/(steigung*uebersetzung))

########################
# GUI Kontrollfunktionen
########################
def manual_mode(steuerung, achse, richtung, speed):
    """Achse verfährt solange wie der Knopf gedrückt ist"""
    if richtung == "+":
        steuerung.rotate(achse.get(), speed.get())
    elif richtung == "-":
        steuerung.rotate(achse.get(), speed.get()*-1)


def stop_manual_mode(steuerung, achse, text, antriebsstrang):
    """Knopf loslassen um Achse zu stoppen"""
    achsen_verfahrwege = {
    "0": antriebsstrang["y_max_weg"],
    "1": antriebsstrang["x_max_weg"],
    "2": antriebsstrang["z_max_weg"]
    }
    steuerung.stop(achse.get())
    # aktuelle Position und max. Weg je nach Achse im Textfeld anzeigen
    akt_pos = steuerung.getAxisParameter(1, achse.get())
    text.delete(1.0, "end")
    # Ueberlaufproblem mit Achsparameter 1 aktuelle Position
    if akt_pos > 2147483647:
        akt_pos = 0
    text.insert("end", f"aktuelle Position: {akt_pos}pps = {pps_in_mm(steuerung, antriebsstrang, achse.get(), akt_pos)}mm\n" )
    text.insert("end", "maximaler Weg von 0 - " + achsen_verfahrwege[str(achse.get())])


def messdaten_schreiben(data):
    """ Schreiben der Messdaten in eine .csv Datei
        Parameter: Index/ Zeit/ Pos x,y/ Value
    """
    header = ["Index", "Zeit in s", "Pos x in mm", "Pos y in mm", "Value in V"]

    with open("Messdaten.csv", "w", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(header)
        writer.writerows(data)
