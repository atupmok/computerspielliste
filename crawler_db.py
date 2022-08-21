import db, crawler

def aktualisiere_steam_daten_aller_spiele():
    for spiel in db.finde_alle_spiele():    
        if spiel.get_plattform() == "Steam":            
            db.update_spiel(crawler.hole_daten_von_steam(spiel))

def aktualisiere_itad_preise():
    for spiel in db.finde_alle_spiele():
        if (not spiel.get_itad_id() is None):
            db.update_spiel(crawler.hole_bester_preis_von_itad(spiel))
