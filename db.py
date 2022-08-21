from Spiel import Spiel
from Ausnahme import Ausnahme
import traceback, logging, sqlite3
from datetime import datetime
from operator import attrgetter
import pathlib

logging.basicConfig(filename="computerspiele.log")

# print("test")
# print(pathlib.Path(__file__).parent.absolute() + "/files/computerspielliste.db)
db_pfad = None
db_pfad = str(pathlib.Path(__file__).parent.absolute())  + '/files/computerspielliste.db'

print(f"{db_pfad=}")


def insert_spiel(spiel: Spiel):
    try:
        with sqlite3.connect(db_pfad) as  con:
            cur = con.cursor()
            werte = (spiel.get_id(), spiel.get_itad_id(), spiel.get_name(), spiel.get_itad_preis(), spiel.get_plattform_id(),
                spiel.get_plattform(), spiel.get_in_besitz(), spiel.get_spieler(), spiel.get_genres_str(), 
                spiel.get_mehrspielermodi_str(), spiel.get_tags_str(), spiel.get_info(), spiel.get_hat_demo_sql(), datetime.now().strftime("%Y-%m-%d"))
            cur.execute("INSERT INTO spiel (id, itad_id, name, itad_preis, plattform_id, plattform, in_besitz, spieler, genres, mehrspielermodi, tags, info, hat_demo, hinzugefuegt_am) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", werte)
            con.commit()            
    except:
        traceback.print_exc()
        logging.warning(datetime.now().strftime(" %Y-%m-%d %H:%M:%S ") + traceback.format_exc())
        raise Ausnahme("Spiel konnte nicht in die DB eingefügt werden")

def update_spiel(spiel: Spiel) -> None:
    try:
        with sqlite3.connect(db_pfad) as con:
            cur = con.cursor()        
            werte = (spiel.get_name(), spiel.get_itad_preis(), spiel.get_plattform_id(),
                spiel.get_plattform(), spiel.get_in_besitz(), spiel.get_spieler(), spiel.get_genres_str(), 
                spiel.get_mehrspielermodi_str(), spiel.get_tags_str(), spiel.get_info(), spiel.get_hat_demo(), spiel.get_id())
            con.set_trace_callback(print)

            cur.execute("UPDATE spiel SET " +
                            "name = ?, " +
                            "itad_preis = ?, " +
                            "plattform_id = ?, " +
                            "plattform = ?, " +
                            "in_besitz = ?, " +
                            "spieler = ?, " +
                            "genres = ?, " +
                            "mehrspielermodi = ?, " +
                            "tags = ?, " +
                            "info = ?, " +
                            "hat_demo = ? "
                        "WHERE id = ?", werte)
            con.commit()
    except:
        traceback.print_exc()
        logging.warning(datetime.now().strftime(" %Y-%m-%d %H:%M:%S ") + traceback.format_exc())
        raise Ausnahme("Spiel konnte nicht in der DB geändert werden")

def finde_last_insert_rowid()-> id:
    try:
        with sqlite3.connect(db_pfad) as  con:
            cur = con.cursor()
            cur.execute("SELECT seq FROM sqlite_sequence WHERE name = 'spiel'")
            r = cur.fetchone()                

        return r[0]

    except:
        traceback.print_exc()
        logging.warning(datetime.now().strftime(" %Y-%m-%d %H:%M:%S ") + traceback.format_exc())
        raise Ausnahme("last_insert_rowid konnte nicht gefunden werden")        

def finde_spiel(id: str) -> Spiel:
    try:
        with sqlite3.connect(db_pfad) as  con:
            cur = con.cursor()
            cur.execute("SELECT id, itad_id, name, plattform_id, plattform, in_besitz, spieler, genres, tags, mehrspielermodi, itad_preis, info, hat_demo, hinzugefuegt_am " + 
                        "FROM spiel WHERE itad_id = ?", (id,))
            r = cur.fetchone()                

        return tupel_zu_spiel(r)

    except:
        traceback.print_exc()
        logging.warning(datetime.now().strftime(" %Y-%m-%d %H:%M:%S ") + traceback.format_exc())
        raise Ausnahme("Spiel konnte nicht gefrunden werden")

def finde_alle_spiele(sortiert_nach="spieler", aufsteigend=True, filter_nach_spielern=[], filter_nach_in_besitz=False) -> list:
    # -- Filter --
    where_klauseln = []
    where_klausel_sql = ""

    filter_nach_spielern = ["'" + spieler + "'" for spieler in filter_nach_spielern]

    if filter_nach_in_besitz:
        where_klauseln.append(" in_besitz = 1 ")
    
    if filter_nach_spielern is not None and len(filter_nach_spielern) > 0:
        where_klauseln.append(f"spieler in (" + ",".join(filter_nach_spielern) + ")")
    
    if len(where_klauseln) > 0:
        where_klausel_sql = "WHERE " + " and ".join(where_klauseln)

    # -- Sortierung -- 
    sortierung = {
        "name": "name",
        "kosten_mit_demos": "kosten_mit_demos",
        "kosten_ohne_demos": "kosten_ohne_demos",
        "plattform": "plattform",
        "spieler": "spieler",
        "hinzugefuegt_am": "hinzugefuegt_am",
        None: "spieler"}

    if sortiert_nach not in sortierung.keys():
        raise Ausnahme("Alle Spiele konnten nicht abgefragt werden. Ungültige Sortierung.")

    sortiert_nach_sql = sortierung[sortiert_nach]
    aufsteigend_sql = "ASC" if aufsteigend else "DESC"

    if sortiert_nach_sql == "kosten_mit_demos" or sortiert_nach_sql == "kosten_ohne_demos":
        sortiert_nach_sql = "itad_preis"    

    try:
        with sqlite3.connect(db_pfad) as  con:
            cur = con.cursor()
            # con.set_trace_callback(print)
            cur.execute(f"SELECT id, itad_id, name, plattform_id, plattform, in_besitz, spieler, genres, tags, mehrspielermodi, itad_preis, info, hat_demo, hinzugefuegt_am " + 
                f"FROM spiel {where_klausel_sql} ORDER BY {sortiert_nach_sql} {aufsteigend_sql} ")
            r = cur.fetchall()                

        spiele = [tupel_zu_spiel(spiel) for spiel in r]

        if aufsteigend is None:
            aufsteigend = False

        reversed = not aufsteigend            

        if sortiert_nach == "kosten_mit_demos":
            spiele = sorted(spiele, key=attrgetter("_kosten_inkl_demo"), reverse=reversed)
        elif sortiert_nach == "kosten_ohne_demos":
            spiele = sorted(spiele, key=attrgetter("_kosten_exkl_demo"), reverse=reversed)

        return spiele

    except:
        traceback.print_exc()
        logging.warning(datetime.now().strftime(" %Y-%m-%d %H:%M:%S ") + traceback.format_exc())
        raise Ausnahme("Alle Spiele konnten nicht abgefragt werden")

def tupel_zu_spiel(tupel) -> Spiel:
    return Spiel(id=tupel[0], itad_id=tupel[1], name=tupel[2], plattform_id=tupel[3], plattform=tupel[4], in_besitz=tupel[5], spieler=tupel[6], genres=tupel[7], tags=tupel[8], mehrspielermodi=tupel[9], itad_preis=tupel[10], info=tupel[11], hat_demo=tupel[12], hinzugefuegt_am=tupel[13])

def finde_preis_aktualisierung() -> datetime:
    try:
        with sqlite3.connect(db_pfad) as  con:
            cur = con.cursor()
            cur.execute("SELECT letzte_aktualisierung FROM preis_aktualisierung")
            r = cur.fetchone()                
        return datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S")

    except:
        traceback.print_exc()
        logging.warning(datetime.now().strftime(" %Y-%m-%d %H:%M:%S ") + traceback.format_exc())
        raise Ausnahme("Preis-Aktualisierung konnte nicht abgefragt werden")

def update_preis_aktualisierung_mit_jetzt() -> None:
    try:
        with sqlite3.connect(db_pfad) as  con:
            cur = con.cursor()        
            cur.execute('UPDATE preis_aktualisierung SET letzte_aktualisierung = "' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '"')
            con.commit()
    except:
        traceback.print_exc()
        logging.warning(datetime.now().strftime(" %Y-%m-%d %H:%M:%S ") + traceback.format_exc())
        raise Ausnahme("Preis-Aktualisierung konnte nicht in der DB geändert werden")