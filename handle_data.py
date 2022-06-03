import configparser

class Handle_Data:

    def __init__(self):
        self.config_file = configparser.ConfigParser() # parser objekt wird erstellt
        self.config_file.read("config.ini") # daten werden in parser objekt geladen
        self.antrieb = {}
        self.get_antrieb(config=self.config_file)

    def get_antrieb(self, config: object) -> None:
        for key in self.config_file["Antriebsstrang"]:
            # print(key + "=" + parser["Antriebsstrang"][key])
            self.antrieb[key] = self.config_file["Antriebsstrang"][key]



        # steigung = steigung
        # getriebe = int(getriebe)
        # y_max = y_max
        # x_max = x_max
        # z_max = z_max
