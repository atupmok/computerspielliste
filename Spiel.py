from datetime import date, datetime
from soupsieve import select_one
from Ausnahme import Ausnahme
import math

class Spiel():
    def __init__(self, id = None, itad_id = None, name = None, plattform_id = None, plattform = None, in_besitz = None, spieler = None, genres = None, tags = None, mehrspielermodi = None, itad_preis = None, info = None, hat_demo = None, hinzugefuegt_am = None):
        self.set_id(id)
        self.set_itad_id(itad_id)
        self.set_name(name)
        self.set_plattform_id(plattform_id)
        self.set_plattform(plattform)
        self.set_in_besitz(in_besitz)
        self.set_spieler(spieler)
        self.set_genres(genres)
        self.set_tags(tags)
        self.set_mehrspielermodi(mehrspielermodi)
        self.set_itad_preis(itad_preis)
        self.set_info(info)
        self.set_hat_demo(hat_demo)
        self.set_hinzugefuegt_am(hinzugefuegt_am)

        self._kosten_inkl_demo = self.get_kosten_inkl_demo()
        self._kosten_exkl_demo = self.get_kosten_exkl_demo()

    def set_id(self, id):        
        if type(id) == int:
            self.__id = id
        elif id is None or math.isnan(id):
            self.__id = None
        else:
            raise Ausnahme("Fehler: ID ungültig (" + id +  ")")
    
    def set_itad_id(self, itad_id):
        if type(itad_id) == str:
            if len(itad_id.strip()) == 0:
                self.__itad_id = None        
            else:
                self.__itad_id = itad_id.strip()        
        elif itad_id is None or math.isnan(itad_id):
            self.__itad_id = None
        else:
            raise Ausnahme("Fehler: ITAD-ID ungültig (" + itad_id +  ")")

    def set_name(self, name):
        if type(name) == str or name is None:
            self.__name = name
        else:
            raise Ausnahme("Fehler: Name ungültig")
    
    def set_plattform_id(self, plattform_id):
        if type(plattform_id) == str and len(plattform_id) > 0 and len(plattform_id) < 100:
            self.__plattform_id = plattform_id
        elif plattform_id is None or math.isnan(plattform_id):
            self.__plattform_id = None
        elif type(plattform_id) == float or type(plattform_id) == int:
            self.__plattform_id = str(int(plattform_id))
        else:
            raise Ausnahme("Fehler: Plattform-ID ungültig")
    
    def set_plattform(self, plattform):
        if plattform is None or plattform in ("Epic", "Steam"):
            self.__plattform = plattform
        else:
            raise Ausnahme("Fehler: Plattform ungültig")

    def set_in_besitz(self, in_besitz):
        if in_besitz or in_besitz == "ja":
            self.__in_besitz = True
        elif not in_besitz or in_besitz == "nein":
            self.__in_besitz = False
        else:
            raise Ausnahme("Fehler: 'In Besitz' ungültig.")
    
    def set_spieler(self, spieler):
        if spieler is None:
            self.__spieler = None
        elif spieler in ("2+", "2", "1", 2, 1):
            self.__spieler = str(spieler)
        else:
            raise Ausnahme("Fehler: Spieler ungültig (" + str(spieler) + ")")
    
    def set_genres(self, genres):
        if genres is None or (type(genres) == list and len(genres) > 0 and len(genres) < 1000):
           self.__genres = genres
        elif type(genres) == str:
            self.__genres = [g.strip() for g in genres.split(",")]

        else:
            raise Ausnahme("Fehler: Genres ungültig")
    
    def set_tags(self, tags):
        if tags is None or (type(tags) == list and len(tags) > 0 and len(tags) < 1000):
           self.__tags = tags
        elif type(tags) == str:
            self.__tags = [g.strip() for g in tags.split(",")]
        else:
            raise Ausnahme("Fehler: Genres ungültig")
    
    def set_mehrspielermodi(self, mehrspielermodi):
        if mehrspielermodi is None or mehrspielermodi == "NA" or (type(mehrspielermodi) == list and len(mehrspielermodi) == 0):
            self.__mehrspielermodi = None
        elif type(mehrspielermodi) == str:
            self.__mehrspielermodi = [m.strip() for m in mehrspielermodi.split(",")]
        elif type(mehrspielermodi) == list and len(mehrspielermodi) > 0:
            self.__mehrspielermodi = mehrspielermodi
        elif math.isnan(mehrspielermodi):
            self.__mehrspielermodi = None        
        else:
            raise Ausnahme("Fehler: Mehrspielermodi ungültig für " + self.__name + " (" + str(mehrspielermodi) + ")")
    
    def set_itad_preis(self, itad_preis):
        if itad_preis is None:
            self.__itad_preis = None
        elif type(itad_preis) == float:
            self.__itad_preis = itad_preis
        elif type(itad_preis) == str:
            try:
                self.__itad_preis = float(itad_preis.replace(",", "."))                
            except:
                raise Ausnahme("Fehler: ITAD-Preis (" + str(itad_preis) + ")" + "ist keine Zahl.")    
        else:
            raise Ausnahme("Fehler: ITAD-Preis ungültig")

    def set_info(self, info):        
        if type(info) == str:
            if len(info.strip()) == 0:
                self.__info = None
            else:
                self.__info = info.strip()        
        elif info is None or math.isnan(info):
            self.__info = None
        else:
            raise Ausnahme("Fehler: info ungültig")

    def set_hat_demo(self, hat_demo):
        if type(hat_demo) == bool or hat_demo is None:
            self.__hat_demo = hat_demo
        elif hat_demo == 1:
            self.__hat_demo = True
        elif hat_demo == 0:
            self.__hat_demo = False
        else:
            raise Ausnahme("Fehler: »hat Demo« ungültig (" + str(hat_demo) + ")")
    
    def set_hinzugefuegt_am(self, hinzugefuegt_am):
        if type(hinzugefuegt_am) == str:
            try:                
                self.__hinzugefuegt_am = datetime.strptime(hinzugefuegt_am, "%Y-%m-%d").date()
            except:
                raise Ausnahme("Fehler: »hinzugefügt am« ungültig")
        elif type(hinzugefuegt_am) == date or hinzugefuegt_am is None:
                self.__hinzugefuegt_am = hinzugefuegt_am
        else:
            raise Ausnahme("Fehler: »hinzugefügt am« ungültig")

    def __str__(self):
        name = self.__name
        itad_id = self.__itad_id

        if self.__name is None:
            name = "unbenannt"

        if self.__itad_id is None:
            itad_id = "keine itat_id"

        return name + "(" + itad_id + ")"

    def get_id(self) -> int:
        return self.__id

    def get_id_str(self) -> str:
        return str(self.__id)

    def get_itad_id(self) -> str:
        return self.__id

    def get_itad_id(self) -> str:
        return self.__itad_id

    def get_name(self) -> str:
        return self.__name

    def get_plattform_id(self) -> str:
        return self.__plattform_id
    
    def get_plattform(self) -> str:
        return self.__plattform

    def get_in_besitz(self) -> bool:
        return self.__in_besitz

    def get_spieler(self) -> str:
        return self.__spieler

    def get_genres(self) -> list:
        return self.__genres        

    def get_genres_str(self) -> str:
        if type(self.__genres) == list and len(self.__genres) > 0:
            return ",".join(self.__genres)
        else:
            return None

    def get_tags(self) -> list:
        return self.__tags

    def get_tags_str(self) -> str:
        if type(self.__tags) == list and len(self.__tags) > 0:
            return ",".join(self.__tags)
        else:
            return None

    def get_mehrspielermodi(self) -> list:
        return self.__mehrspielermodi

    def get_mehrspielermodi_str(self) -> str:
        if type(self.__mehrspielermodi) == list and len(self.__mehrspielermodi) > 0:
            return ",".join(self.__mehrspielermodi)
        else:
            return None

    def get_itad_preis(self) -> list:
        return self.__itad_preis

    def get_itad_preis_str(self) -> str:
        return str(self.__itad_preis).replace(".", ",")

    def get_info(self) -> str:
        return self.__info
    
    def get_hat_demo(self) -> bool:
        return self.__hat_demo

    def get_hat_demo_sql(self) -> int:
        return 1 if self.__hat_demo else 0

    def get_hinzugefuegt_am(self) -> date:
        return self.__hinzugefuegt_am
    
    def get_hinzugefuegt_am_str(self) -> str:
        return self.__hinzugefuegt_am.strftime("%d.%m.%Y")

    def get_kosten_inkl_demo(spiel) -> float:
        if (spiel.get_mehrspielermodi() != None and spiel.get_in_besitz() and "Remote Play Together" in spiel.get_mehrspielermodi()) or (spiel.get_in_besitz() and spiel.get_spieler() == "1") or spiel.__hat_demo:
            return 0
        else:
            return spiel.get_itad_preis()
    
    def get_kosten_exkl_demo(spiel) -> float:
        if (spiel.get_mehrspielermodi() != None and spiel.get_in_besitz() and "Remote Play Together" in spiel.get_mehrspielermodi()) or (spiel.get_in_besitz() and spiel.get_spieler() == "1"):
            return 0
        else:
            return spiel.get_itad_preis()
