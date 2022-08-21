from Ausnahme import Ausnahme
from bs4 import BeautifulSoup
from Spiel import Spiel
from datetime import datetime
import traceback, logging, requests

def hole_daten_von_steam(spiel: Spiel) -> Spiel:
    '''Ladet die Steam-Seite des Spiels herunter und setzt genres, tags, name und mehrspielermodi neu.'''
    if spiel.get_plattform_id() is None:
        raise Ausnahme("Fehler: Spiel benötigt eine Plattform-ID.")
    
    if spiel.get_plattform() != "Steam":
        raise Ausnahme("Fehler: Die Plattform des Spiels muss Steam sein.")

    url = "https://store.steampowered.com/app/" + spiel.get_plattform_id()
    r = requests.get(url)
    doc = BeautifulSoup(r.text, "html.parser")
    
    # -- Genres --
    div = doc.select_one(".details_block")  
    genres = []
    element = div.select_one("a")

    while element.name != "div":
        if element.name == "a":
            genres.append(element.text)

        element = element.next_element
    
    spiel.set_genres(genres)
    
    # -- tags --    
    spiel.set_tags([a.text.strip() for a in doc.select(".app_tag")][:5])

    # -- name --
    spiel.set_name(doc.select_one(".apphub_AppName").text)

    # -- mehrspielermodi --
    mehrspielermodi = []
    for div in doc.select(".game_area_details_specs"):
        for a in div.select("a"):
            if a.text in ("Online PvP", "Shared/Split Screen PvP", "Online Co-op", "Shared/Split Screen Co-op", "Remote Play Together"):
                mehrspielermodi.append(a.text)

    spiel.set_mehrspielermodi(mehrspielermodi)

    # -- demo --
    hat_demo = ("Download Demo" in doc.text or f"Download {spiel.get_name()} Demo" in doc.text)
    # print(f"Download {spiel.get_name()} Demo")
    spiel.set_hat_demo(hat_demo)
        
    return spiel

def hole_bild_von_steam(id: int, plattform_id: str) -> None:
    '''Benötigt plattform_id und id'''
    if (plattform_id is None or id is None):
        raise Ausnahme("Fehler: Um das Bild von Steam zu holen wird die ID und die Steam-ID benötigt")
    
    url = "https://cdn.akamai.steamstatic.com/steam/apps/" + str(plattform_id) + "/header.jpg"
    __hole_bild(url, "static/imgs/logo/" + str(id) + ".jpg")
    
def __hole_bild(url: str, dateipfad: str) -> None:
    try:
        r = requests.get(url)    
        with open(dateipfad, "wb") as file:
            file.write(r.content)

    except:
        traceback.print_exc()
        logging.warning(datetime.now().strftime(" %Y-%m-%d %H:%M:%S ") + traceback.format_exc())
        raise Ausnahme("Fehler: Bild (" + url + ") konnte nicht heruntergeladen und gespeichert werden.")

def hole_spielablauf_bild(id: int, url: str) -> None:
    __hole_bild(url, "static/imgs/spielablauf/" + str(id) + ".jpg")

def hole_bester_preis_von_itad(spiel: Spiel) -> Spiel:
    if spiel.get_itad_id() is None:
        raise Ausnahme("Fehler: Spiel benötigt eine ITAD-ID.")

    url = "https://isthereanydeal.com/game/" + spiel.get_itad_id() + "/info/"
    
    r = requests.get(url)
    doc = BeautifulSoup(r.text, "html.parser")

    spiel.set_itad_preis(doc.select_one("#gh-po").select(".gh-po__price")[1].text[:-1])        
    return spiel