from math import trunc
from flask import Flask, render_template, request
import db, crawler_db, crawler, traceback
from Spiel import Spiel
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def home():
    meldung = None
    gut_gelaufen = True
    
    # Button btn_preise_aktualisieren wurde gedrückt
    if request.method == 'POST' and "btn_preise_aktualisieren" in request.form.keys():
        try:                           
            crawler_db.aktualisiere_itad_preise()
            db.update_preis_aktualisierung_mit_jetzt()
            meldung = "ITAD-Preise erfolgreich aktualisiert!"
        except:
            gut_gelaufen = False
            meldung = "ITAD-Preise konnten nicht aktualisiert werden!"
    
    sortiert_nach = "hinzugefuegt_am"
    aufsteigend = False
    in_besitz = False
    spieler = {"1": False, "2": False, "2_plus": False}
    
    if request.method == "GET":
        if "chb_in_besitz" in request.args.keys() and request.args["chb_in_besitz"] == "in_besitz":
            in_besitz = True

        if "ddl_sortierung" in request.args.keys():
            sortiert_nach = request.args["ddl_sortierung"]
            aufsteigend = False

        if "chb_aufsteigend" in request.args.keys() and request.args["chb_aufsteigend"] == "aufsteigend":
            aufsteigend = True

        filter_nach_spielern = []
        if "chb_spieler_1" in request.args.keys():
            spieler["1"] = True
            filter_nach_spielern.append("1")

        if "chb_spieler_2" in request.args.keys():
            spieler["2"] = True
            filter_nach_spielern.append("2")
            

        if "chb_spieler_2_plus" in request.args.keys():
            spieler["2_plus"] = True
            filter_nach_spielern.append("2+")
    
    spiele = db.finde_alle_spiele(sortiert_nach, aufsteigend, filter_nach_spielern, in_besitz)

    # letzte_preis_aktualisierung = datetime.strptime(db.finde_preis_aktualisierung(), "%Y-%m-%d %H:%M:%S").datetime().strftime("%d.%m.%Y %H:%M:%S")
    bla = db.finde_preis_aktualisierung()
    letzte_preis_aktualisierung = bla.strftime("%d.%m.%Y %H:%M:%S")
    return render_template("index.html", spiele=spiele, letzte_preis_aktualisierung=letzte_preis_aktualisierung,meldung=meldung,gut_gelaufen=gut_gelaufen,sortiert_nach=sortiert_nach,aufsteigend=aufsteigend, in_besitz=in_besitz, spieler=spieler)

if __name__ == "__main__":
    # app.run(host='0.0.0.0', debug = True)
    app.run(threaded=True, port=5000)

@app.route("/hinzufuegen", methods = ['POST', 'GET'])
def hinzufuegen():
    meldung = None
    gut_gelaufen = True

    if request.method == "POST" and "btn_hinzufuegen"in request.form.keys():
        in_besitz = False
        if "chb_in_besitz" in request.form.keys():
            in_besitz = True

        try:
            last_insert_rowid = db.finde_last_insert_rowid()
            spiel = Spiel(id=last_insert_rowid+1, itad_id=request.form["txt_itad_id"], plattform_id=request.form["txt_plattform_id"], plattform=request.form["ddl_plattform"], spieler=request.form["ddl_spieler"], in_besitz=in_besitz, info=request.form["txt_info"])

            if (spiel.get_id() != None):
                crawler.hole_spielablauf_bild(spiel.get_id(), request.form["txt_bild_url"])
            
            if (spiel.get_itad_id() != None):
                spiel = crawler.hole_bester_preis_von_itad(spiel)            
            
            if spiel.get_plattform() == "Steam":
                crawler.hole_bild_von_steam(spiel.get_id(), spiel.get_plattform_id())
                spiel = crawler.hole_daten_von_steam(spiel)       
            
            db.insert_spiel(spiel)            
            meldung = "Spiel erfolgreich hinzugefügt!"            
        except:
            traceback.print_exc()            
            gut_gelaufen = False
            meldung = "Spiel konnte nicht hinzugefügt werden!"

    return render_template("hinzufuegen.html", meldung=meldung, gut_gelaufen=gut_gelaufen)