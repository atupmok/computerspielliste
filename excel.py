import pandas as pd
from Spiel import Spiel

def hole_spiele_von_excel() -> list[Spiel]:

    df = pd.read_excel("files/computerspielliste.xlsx", engine="openpyxl")

    spiele = []

    for id, ss in df.iterrows():
        spiele.append(Spiel(itad_id=ss["ITAD-ID"], name=ss["Name"], in_besitz=ss["In Besitz"], plattform=ss["Plattform"], bild=ss["Bild"], spieler=ss["Spieler"], info=ss["Info"]))
    return spiele


    