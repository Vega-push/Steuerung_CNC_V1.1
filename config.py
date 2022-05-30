import configparser

# parser objekt wird erstellt
parser = configparser.ConfigParser()
# daten werden in parser objekt geladen
parser.read("config.ini")

def ausgabe_ap(steuerung):
    """Ausgabe aller eingestellten Achsparameter für alle Achsen"""
    ind_aps = get_ind_aps(parser)
    for i in range(steuerung.MOTORS):
        print(liste_achsen[i] + ":")
        for index in ind_aps:
            print(steuerung.getAxisParameter(index, i))


def get_ind_aps(config):
    """erstelle Liste mit Indizes der Achsenparameter, die gesetzt werden sollen"""
    index_aps = []
    for key in config["Achsenparameter"]:
        index_aps.append(int(key))
    return index_aps


def load_config(steuerung):
    """laden, setzen der Achsenparameter und der Daten des Antriebsstranges"""
    ind_aps = get_ind_aps(parser) # erzeugen einer index Liste
    antriebsstrang = {}

    # laden und setzen der Achsparameter
    for i in range(steuerung.MOTORS):
        # print(f"fuer die {liste_achsen[i]}: ")
        for ind in ind_aps:
            value = int(parser["Achsenparameter"][str(ind)])
            # print(f"Achsenparameter {ind}, Wert {value}.")
            steuerung.setAxisParameter(apType=ind, motor=i, value=value)

    # laden und speichern der Antriebsstrang Parameter in einem dic
    for key in parser["Antriebsstrang"]:
        # print(key + "=" + parser["Antriebsstrang"][key])
        antriebsstrang[key] = parser["Antriebsstrang"][key]

    return antriebsstrang
