import pandas as pd
import json

orari = pd.read_excel("./Orari.xlsx")

tournament = {"torneo_2022": {}}

for idx, rows in orari.iterrows():
    data = {}
    hour, minutes = str(rows["orario"]).split(".")
    orario = rows["giorno"].replace(hour=int(hour), minute=int(minutes) if len(minutes) > 1 else int(minutes + "0"))
    data["data"] = orario.strftime("%m-%d-%Y %H:%M:%S")
    data["gironi"] = rows["girone"]
    data["genere_gironi"] = rows["torneo"]
    data["squadra_1"] = rows["squadra1"]
    data["squadra_2"] = rows["squadra2"]
    data["gol_squadra_1"] = 0
    data["gol_squadra_2"] = 0
    data["falli_squadra_1"] = 0
    data["falli_squadra_2"] = 0
    data["gialli1"] = ""
    data["gialli2"] = ""
    data["rossi1"] = ""
    data["rossi2"] = ""
    data["goleador_1"] = "{}"
    data["goleador_2"] = "{}"
    data["autogol1"] = "{}"
    data["autogol2"] = "{}"
    data["best_giocatore_1"] = {}
    data["best_giocatore_2"] = {}
    data["best_portiere_1"] = {}
    data["best_portiere_2"] = {}
    data["note"] = ""
    tournament["torneo_2022"].update({str(idx): data})
    with open(f"./torneo_2022.json", encoding="UTF-8", mode="w") as file:
        json.dump(tournament, file)
