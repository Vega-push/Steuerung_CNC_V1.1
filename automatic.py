import csv
import time
import tkinter as tk
import getanaloginput as IO
from tkinter import messagebox
from config import load_config
from controls import messdaten_schreiben, pps_in_mm

messdaten = []
counter = 1

def aps_ausgeben(steuerung, achse):
    """Hilffunktion zum Erkennen von falsch gesetzten AP´s"""
    for i in range(255):
        print(f"{i} = {steuerung.getAxisParameter(i, achse)}")


def skript_laden(datei):
    """laden eines Skripts und Aufbereitung der Daten"""
    aktuelles_skript = []
    try:
        with open(datei) as f:
            data = csv.reader(f)
            # jede Zeile im Skript entspricht einer Liste (row)
            for row in data:
                reihe = []
                # jeden Eintrag (string) der Listen durchgehen und aufbereiten
                for string in row:
                    str = string.strip()
                    str = str.upper()
                    reihe.append(str)
                # die Aufbereiteten Listen zu einer Liste zusammenführen
                aktuelles_skript.append(reihe)
    except FileNotFoundError:
        print("Kein Skript geladen! Ausgewaehlte Datei existiert nicht.")
        exit()
    # TODO : LOOP Eingabe
    return aktuelles_skript

# TODO
def skript_speichern(skript):
    """speichern des Skripts in ausgewähltem Dateipfad"""
    dateiname = input("Bitte Speicherpfad + Name eingeben. ")
    datei = open(dateiname,"w") # r = read, w = write, a = append, r+ = r und w
    for liste in skript:
        for i,string in enumerate(liste):
            # nach letztem "string" einer Zeile kein Komma und kein Leerzeichen
            if i+1 < len(liste):
                datei.write(string + "," + " ")
            else:
                datei.write(string)
        datei.write("\n")
    datei.close()


def skript_ueberpruefen(skript):
    """durchsuche das übergebene Skript nach Fehlern und gebe die Zeile des
    ersten gefunden Fehlers zurück"""
    # konstante Variablen abspeichern
    befehlsliste = ["MVP", "WAIT", "ROR", "ROL", "MST", "SAP", "GAP", "SIO", "GIO", "LOOP"]

    # jeden Befehl jeder Zeile überprüfen, bei Fehler Rückgabe False und Zeilennr.
    for i,zeile in enumerate(skript):
        if zeile[0] in befehlsliste:
            pass
        else:
            return False, i+1
    return True, 0


def verfahrgrenze_ueberpruefen(steuerung, zeile, grenze):
    """Überprüfe ob Verfahrbewegungen möglich sind, abhängig ob die
     Verfahrbewegung absolut, relativ oder per Koordinateneingabe geschieht"""
    typ = zeile[1]
    achse = int(zeile[2])
    weg = int(zeile[3])
    if typ == "ABS":
        if weg >= 0 and weg <= grenze:
            return True
        else:
            tk.messagebox.showerror(message="Absolutwert zu groß!")
            return False
    elif typ =="REL":
        # akt. pos abfragen und max. Verfahrweg in + und - Richtung ausrechnen
        aktuelle_pos = steuerung.getAxisParameter(1,achse)
        max_pos_weg = grenze - aktuelle_pos
        max_neg_weg = aktuelle_pos*-1
        if weg < max_pos_weg and weg > max_neg_weg:
            return True
        else:
            tk.messagebox.showerror(message="Inkrementaler Verfahrweg zu groß!")
            return False
    elif typ == "COORD":
        # TODO
        print("TODO: COORD")
        return False


def skript_ausfuehren(steuerung, maschinendaten, skript, step):
    """Skript ausführen, im Automatischen_ oder im Einzelschrittmodus"""
    if step:
        for zeile in skript:
            MsgBox = tk.messagebox.askquestion("Schrittbetrieb","Fortfahren")
            befehlsauswahl(steuerung, maschinendaten, zeile)
            while not(steuerung.positionReached(int(zeile[2]))):
                pass
            if zeile[0] != "WAIT":
                if MsgBox == "yes":
                    pass
                else:
                    break
            else:
                pass
    else:
        for zeile in skript:
            befehlsauswahl(steuerung, maschinendaten, zeile)
    messdaten_schreiben(messdaten)


def befehlsauswahl(steuerung, maschinendaten, zeile):
    """treffe eine Auswahl was zu tun ist je nach Befehlskette des Skripts"""
    verfahrgrenzen = [
        int(maschinendaten["y_max_weg"]),
        int(maschinendaten["x_max_weg"]),
        int(maschinendaten["z_max_weg"])]
    befehl = zeile[0]

    match befehl:
        case "MVP":
            befehlstyp = zeile[1]
            achse = int(zeile[2])
            verfahrweg = int(zeile[3])
            if befehlstyp == "ABS":
                if verfahrgrenze_ueberpruefen(steuerung, zeile, verfahrgrenzen[achse]):
                    steuerung.moveTo(motor=achse, position=verfahrweg)
                else:
                    print("Verfahrgrenzen nicht eingehalten!")
                    exit()
            elif befehlstyp == "REL":
                if verfahrgrenze_ueberpruefen(steuerung, zeile, verfahrgrenzen[achse]):
                    steuerung.moveBy(motor=achse, difference=verfahrweg)
                else:
                    print("Verfahrgrenzen nicht eingehalten!")
                    exit()
            elif befehlstyp == "COORD":
                print("TODO!!")
                print(f"Fahre mit Achse {achse} auf Koordinate {verfahrweg}")
        case "WAIT":
            befehlstyp = zeile[1]
            achse = int(zeile[2])
            verfahrweg = int(zeile[3])
            while not(steuerung.positionReached(achse)):
                pass
            # wenn Position erreicht, Sensor auslesen, Wartezeit für Sensor
            time.sleep(0.1)
            messdatenliste_erzeugen(steuerung, maschinendaten)
        case "ROR":
            achse = int(zeile[1])
            velocity = int(zeile[2])
            v_pps = (16*10**6*velocity)/(2**steuerung.getAxisParameter(154,achse)*2048*(2**steuerung.getAxisParameter(140,achse)))
            aktuelle_pos = steuerung.getAxisParameter(1,achse)
            max_weg = verfahrgrenzen[achse] - aktuelle_pos
            verfahrzeit = int(max_weg/v_pps)-1 # Sicherheitspuffer
            if verfahrzeit < 0:
                verfahrzeit = 0
            print(verfahrzeit)
            steuerung.rotate(motor=achse, velocity=velocity)
            time.sleep(verfahrzeit)
            steuerung.stop(achse)
            time.sleep(1)
            # wichtig!!! nach ROR sonst kein MVP mehr möglich, überschreiben
            # des AP-s aktuelle Pos
            load_config(steuerung)
            print(f"Motor:{achse}, akt.pos={steuerung.getAxisParameter(1,achse)}!")
        case "ROL":
            achse = int(zeile[1])
            velocity = int(zeile[2])*-1
            v_pps = (16*10**6*velocity*-1)/(2**steuerung.getAxisParameter(154,achse)*2048*(2**steuerung.getAxisParameter(140,achse)))
            aktuelle_pos = steuerung.getAxisParameter(1,achse)
            max_weg = aktuelle_pos*-1
            verfahrzeit = int(aktuelle_pos/v_pps)-1
            if verfahrzeit < 0:
                verfahrzeit = 0
            steuerung.rotate(motor=achse, velocity=velocity)
            time.sleep(verfahrzeit)
            steuerung.stop(achse)
            time.sleep(1)
            load_config(steuerung)
            print(f"Motor:{achse}, akt.pos={steuerung.getAxisParameter(1,achse)}!")
        case "MST":
            achse = int(zeile[1])
            print("Motor stoppt!")
            steuerung.stop(achse)
        case "SAP":
            apType = int(zeile[1])
            achse = int(zeile[2])
            value = int(zeile[3])
            print(f"Setze Achsenparameter {apType}, auf den Wert {value}!")
            steuerung.setAxisParameter(apType, achse, value)
        case "GAP":
            apType = int(zeile[1])
            achse = int(zeile[2])
            value = steuerung.getAxisParameter(apType, achse)
            print(f"Achsenparameter {apType} hat den Wert {value}!")
        case "SIO":
            print("Setze digitalen Output!")
        case "GIO":
            print("Lese digitalen Input!")


def messdatenliste_erzeugen(steuerung, maschinendaten):
    global counter
    global startzeit
    if counter == 1:
        startzeit = time.time()
    messwerte = []
    messwerte.append(counter)
    messwerte.append(round(time.time()-startzeit,3))
    messwerte.append(pps_in_mm(steuerung, maschinendaten, 0, steuerung.getAxisParameter(1, 0)))
    messwerte.append(pps_in_mm(steuerung, maschinendaten, 1, steuerung.getAxisParameter(1, 1)))
    messwerte.append(round(IO.messwert_auslesen(),3))
    messdaten.append(messwerte)
    counter += 1
