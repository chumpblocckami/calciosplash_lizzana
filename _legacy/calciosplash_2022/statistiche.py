import pandas as pd
import datetime as dt
import json

data = pd.read_excel("Iscritti.xlsx", sheet_name="MASCHILE")
data = data.append(pd.read_excel("Iscritti.xlsx", sheet_name="FEMMINILE"))

data["Nascita"] = pd.to_datetime(data["Nascita"])
data["Played"] = data["Played"].apply(lambda x: True if x == "SI" else False)
data["Nominativo"] = data["Cognome"].str.strip().str.capitalize() + " " + data["Nome"].str.strip().str.capitalize()
data["Eta"] = data["Nascita"].apply(lambda x: dt.datetime.now() - x).dt.days / 365

goal = pd.read_csv("./../albo_doro.csv")
goal = goal.set_index("Unnamed: 0")
goal = goal.reset_index().rename(columns={"Unnamed: 0": "Nominativo"})
data = pd.merge(data, goal, how="left", on="Nominativo")

# statistiche per Squadra
squadre = pd.DataFrame()
squadre["eta_media_Squadra"] = ((data.groupby("Squadra")["Eta"].sum()).sort_index() / data.groupby("Squadra").size().sort_index())
squadre["numero_componenti"] = data.groupby("Squadra").count()["Nome"]
squadre["%_Played"] = data.groupby("Squadra")["Played"].sum() / data.groupby("Squadra")["Played"].count()
squadre["totale_goal"] = data.groupby("Squadra")["Totale"].sum()
squadre["Torneo"] = data.groupby("Squadra")["Torneo"].max()
squadre["goleador"] = data.loc[data.groupby(["Squadra"])["Totale"].idxmax().fillna(0)]["Nominativo"].values
squadre["gol_goaleador"] = data.loc[data.groupby(["Squadra"])["Totale"].idxmax().fillna(0)]["Totale"].values
squadre["%_Instagram"] = data.groupby(["Squadra"])["Instagram"].count() / data.groupby(["Squadra"]).count()["Nominativo"]
giocatori = data.drop(columns="Nome,Cognome,Nascita,Instagram".split(","))
giocatori = giocatori.sort_values("Nominativo")
with pd.ExcelWriter('2022_statistiche_1.xlsx') as writer:
    squadre.to_excel(writer, sheet_name='SQUADRE')
    giocatori.to_excel(writer, sheet_name='GIOCATORI')
