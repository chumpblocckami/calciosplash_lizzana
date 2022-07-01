import pymongo
import pandas as pd
import itertools
from collections import Counter
import json

anno = 2021
password = input("Insert Password")
client = pymongo.MongoClient(f"mongodb+srv://gsp:{password}@gsp.pfv6c.mongodb.net/?retryWrites=true&w=majority")
db = client.test

def make_giocatori():
    matches = pd.DataFrame().from_records([x for x in client.GSP.matches.find({})])
    matches.columns = ["id", "squadra_1", "squadra_2", "gol_squadra_1", "gol_squadra_2", "data", "orario", "genere_gironi",
                       "id", "tempo", "goal", "best_giocatore", "gialli1", "team"]
    matches = matches.drop(columns=["id"])
    goleador = [x.rstrip().lstrip() for x in ",".join(list(itertools.chain(
        matches["goal"].fillna("[]").apply(lambda x: ''.join(e for e in x if e.isalnum() or e == "," or e == " "))))).split(
        ",")]
    goals = Counter(goleador)

    players = pd.DataFrame().from_records([x for x in client.GSP.player.find({})])
    players.set_index("name", inplace=True)
    data = {"calciosplash_2021": {}}
    n = 0

    # QUA BISOGNEREBBE LEGGERE TUTTI I SOPRANNOMI
    nicknames = {}
    for anno in [2014, 2015, 2016, 2017, 2018, 2019, 2021]:
        with open(f"./../_legacy/calciosplash_{anno}/giocatori_{anno}.json", "r") as file:
            old_player_data = json.load(file)
        old_player_data = {v["nominativo"].rstrip(): v["soprannome"].rstrip() for v in
                           old_player_data[f"calciosplash_{anno}"].values()}
        nicknames.update(old_player_data)

    for idx, row in players.iterrows():
        nominativo = f"{idx.split(' ')[-1].capitalize()} {''.join([x.capitalize() for x in idx.split(' ')[:-1]])}"
        player_data = {}
        player_data["nome"] = idx.split(" ")[-1]
        player_data["cognome"] = "".join(idx.split(" ")[:-1])
        player_data["soprannome"] = nicknames[nominativo] if nominativo in nicknames else ""
        player_data["nominativo"] = nominativo
        player_data["squadra"] = "".join([x.capitalize() for x in row["2021_team"].split(" ")]) if pd.isna(
            row["2021_team"]) == False else ""
        player_data["gialli"] = len([x for x in matches["gialli1"].values if x == idx])
        player_data["rossi"] = 0
        player_data["n_best"] = len([x for x in matches["best_giocatore"].values if x == idx])
        player_data["punteggio"] = len([x for x in matches["best_giocatore"].values if x == idx]) * 2
        player_data["gol"] = goals[idx] if idx in goals else 0
        player_data["autogol"] = 0
        data["calciosplash_2021"][str(n)] = player_data
        n = n + 1

    with open(f"./../_legacy/calciosplash_{anno}/giocatori_{anno}.json", "w") as file:
        json.dump(data, file)
    with open(f"./../_legacy/nicknames.json", "w") as file:
        json.dump(nicknames, file)

    ##save soprannomi
    nicknames = pd.DataFrame(nicknames, index=[1]).T
    nicknames.columns = ["Soprannome"]
    non_anonimi = nicknames.loc[nicknames["Soprannome"] != ""]
    anonimi = nicknames.loc[nicknames["Soprannome"] == ""]
    writer = pd.ExcelWriter("./../_legacy/nicknames.xlsx", engine='xlsxwriter')
    non_anonimi.to_excel(writer, sheet_name="giocatori_con_soprannome")
    anonimi.to_excel(writer, sheet_name="giocatori_senza_soprannome")
    writer.save()

def make_torneo():
    matches = pd.DataFrame().from_records([x for x in client.GSP.matches.find({})])
    matches.columns = ["id", "squadra_1", "squadra_2", "gol_squadra_1", "gol_squadra_2", "data", "orario", "genere_gironi",
                       "id", "tempo", "goal", "best_giocatore", "gialli1", "team"]
    matches = matches.drop(columns=["id"])

    data = [f"calciosplash_{anno}"]
    n = 0
    for idx,row in matches.iterrows():
        match_data = {}
        match_data["gol_squadra_1"] = row["gol_squadra_1"]
        match_data["gol_squadra_2"] = row["gol_squadra_2"]
        match_data["falli_squadra_1"] = row["gol_squadra_1"]
        match_data["falli_squadra_2"] = row["gol_squadra_2"]
        match_data["squadra_1"] = row["squadra_1"]
        match_data["squadra_2"] = row["squadra_2"]
        match_data["gironi"] = ""
        match_data["genere_gironi"] = row["genere_gironi"]
        match_data["gialli1"] = row["gialli1"]
        match_data["gialli2"] = ""
        match_data["rossi1"] =  ""
        match_data["rossi2"] =  ""
        match_data["goleador1"] = {x:len(x) for x in row["goal"]} #qua devo parsare e prendere tutto e bla bla bla
        match_data["goleador2"] = ""
        match_data["data"] = row["tempo"]
        match_data["autogol1"] =  "{}"
        match_data["autogol2"] =  "{}"
        match_data["best_giocatore_1"] =  { },
        match_data["best_giocatore_2"] =  {},
        match_data["best_portiere_1"] =  {},
        match_data["best_portiere_2"] =  {}
        data[f"calciosplash_anno"][str(n)] = match_data
        n = n+1

if __name__ == "__main__":
    #make_giocatori()
    make_torneo()