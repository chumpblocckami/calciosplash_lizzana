import requests
from bs4 import BeautifulSoup
import json 

urls = ["http://calciosplashlizzana.altervista.org/site/index.php?mod=19_Albo_d_oro/01_CLASSIFICA_MARCATORI_MASCHILE",
        "http://calciosplashlizzana.altervista.org/site/index.php?mod=19_Albo_d_oro/02_CLASSIFICA_MARCATORI_FEMMINILE"]

for url in urls:
    doc_name = "maschile" if "MASCHILE" in url else "femminile"
    soup = BeautifulSoup(requests.get(url).text, features="lxml")
    table = soup.find("table")
    albo_doro = [{"GENERE":doc_name}]
    columns = ["GOL","NOMINATIVO","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19"]
    for tr in table.findAll("tr"):
        player_history = {columns[i]:td.text.strip() for i,td in enumerate(tr.findAll("td"))}
        if player_history["NOMINATIVO"] == "" or player_history["NOMINATIVO"] == "COGNOME NOME":
            pass
        else:
            albo_doro.append(player_history)
    with open(f"./_storage/albo_doro/{doc_name}.json","w+") as writer:
        json.dump(albo_doro, writer)