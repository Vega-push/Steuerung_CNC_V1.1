from config import load_config

def np_referenzfahrt(steuerung, antriebsstrang):
    """setze für alle Achsen den NP"""
    achsen_verfahrwege = {
    "y": int(antriebsstrang["y_max_weg"]),
    "x": int(antriebsstrang["x_max_weg"]),
    "z": int(antriebsstrang["z_max_weg"])
    }
    # fahre jede Achse gegen Referenzschalter und setze NP
    for i, item in enumerate(achsen_verfahrwege):
        steuerung.rotate(i,1500)
        print(f"Fahre {item.upper()}-Achse in rechten Referenzschalter!")
        while not(steuerung.getAxisParameter(10, i)):
            pass
        steuerung.stop(i)
        # fahre max Achsenverfahrweg vom Schalter zurueck
        steuerung.moveBy(i, -1*achsen_verfahrwege[item], 1500)
        print(f"Fahre {item.upper()}-Achse um {achsen_verfahrwege[item]}pps zum NP!")
        in_mm = pps_in_mm(steuerung, antriebsstrang, i, achsen_verfahrwege[item])
        print(in_mm)
        while not(steuerung.positionReached(i)):
            pass
        steuerung.stop(i)
        # NP setzen
        steuerung.setAxisParameter(apType=1, motor=i, value=0)
        print(f"NP der Achse {item.upper()} gesetzt")

    load_config(steuerung)


def pps_in_mm(steuerung, antrieb, achse, pulse):
    """Rotatorische Bewegung (pps) in eine translatorische Bewegung (mm)."""
    vollschritt = float(antrieb["vollschritt"])
    µstepRes = 2**steuerung.getAxisParameter(140, achse)
    steigung = float(antrieb["steigung_mm_pro_u"])
    uebersetzung = float(antrieb["getriebe_uebersetzung"])
    return float("{:.3f}".format((pulse/((360/vollschritt)*µstepRes))*steigung*uebersetzung))


def mm_in_pps(steuerung, antrieb, achse, strecke):
    """Translatorische Bewegung (mm) in rotatorische Bewegung umrechnen(pps)"""
    vollschritt = float(antrieb["vollschritt"])
    µstepRes = 2**steuerung.getAxisParameter(140, achse)
    steigung = float(antrieb["steigung_mm_pro_u"])
    uebersetzung = float(antrieb["getriebe_uebersetzung"])
    return int((strecke*(360/vollschritt)*µstepRes)/(steigung*uebersetzung))
