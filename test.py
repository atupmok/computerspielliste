import excel, db, crawler, crawler_db
from Spiel import Spiel

# crawler_db.aktualisiere_itad_preise()

# db.update_preis_aktualisierung_mit_jetzt()
# print(db.finde_preis_aktualisierung())

# spiel = Spiel(itad_id="test", in_besitz=True, spieler="1")
# db.insert_spiel(spiel)



# for spiel in db.finde_alle_spiele():
#     print(spiel.get_hat_demo())
#     print(spiel.get_hinzugefuegt_am())

# spiel = db.finde_spiel("cryptofnecrodancer")
# crawler.hole_daten_von_steam(spiel)

crawler_db.aktualisiere_steam_daten_aller_spiele()

# Download DERU - The Art of Cooperation Demo
#            DERU - The Art of Cooperation
    