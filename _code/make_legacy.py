import zipfile
import os
import pandas as pd
import json
from tqdm import tqdm
import warnings

warnings.simplefilter("ignore")


def unzip_folder(read_path, write_path):
    with zipfile.ZipFile(read_path, 'r') as zip_ref:
        zip_ref.extractall(write_path)


def parse_string(string):
    return string.replace("\n\r", "").replace("\r\n", "")


def get_giocatori(read_path):
    squadre = pd.read_excel(f"{read_path}/dbo.anagrafica_squadre.xlsx", engine="openpyxl").set_index("id")
    squadre = json.loads(squadre["nome"].T.to_json())
    # qua voglio: {id: ... , nominativo: ..., nome: ... , cognome: ... , soprannome: ... , squadra: ..., gol: ... , "miglior_giocatore: ..., "gialli": ..., "rossi": ...}
    giocatori = pd.read_excel(f"{read_path}/dbo.anagrafica_giocatori.xlsx", engine="openpyxl").set_index("id")
    giocatori["soprannome"] = giocatori["cognome"].apply(
        lambda x: "".join(x.strip().split("(")[1]).replace(")", "") if "(" in x else "")
    giocatori["cognome"] = giocatori["cognome"].apply(
        lambda x: "".join(x.strip().split("(")[0]).replace("(", "") if "(" in x else x)
    giocatori["nominativo"] = giocatori["nome"] + " " + giocatori["cognome"]
    giocatori["squadra"] = giocatori["id_anagrafica_squadre"].apply(lambda x: squadre[str(x)] if x != 0 else "")

    cartellini = pd.read_excel(f"{read_path}/dbo.cartellini.xlsx", engine="openpyxl").set_index("id")
    cartellini["nome"] = cartellini["id_anagrafica_giocatori"].apply(lambda x: giocatori.loc[x]["nominativo"])
    cartellini["squadra"] = cartellini["id_anagrafica_squadre"].apply(lambda x: squadre[str(x)] if x != 0 else "")
    cartellini_gialli = cartellini.loc[cartellini["tipo"] == "G"]["nome"].value_counts()
    cartellini_rossi = cartellini.loc[cartellini["tipo"] == "R"]["nome"].value_counts()
    giocatori["gialli"] = giocatori["nominativo"].apply(
        lambda x: cartellini_gialli.loc[x] if x in cartellini_gialli else 0)
    giocatori["rossi"] = giocatori["nominativo"].apply(
        lambda x: cartellini_rossi.loc[x] if x in cartellini_rossi else 0)

    miglior_giocatore = pd.read_excel(f"{read_path}/dbo.miglior_giocatore.xlsx", engine="openpyxl").set_index("id")
    miglior_giocatore["nome"] = miglior_giocatore["id_anagrafica_giocatori"].apply(
        lambda x: giocatori.loc[x]["nominativo"])
    migliori_giocatori = miglior_giocatore.groupby(["nome"])["punti"].sum().sort_values()
    numero_volte_miglior_giocatore = miglior_giocatore["nome"].value_counts()
    giocatori["n_best"] = giocatori["nominativo"].apply(
        lambda x: numero_volte_miglior_giocatore.loc[x] if x in numero_volte_miglior_giocatore else 0)
    giocatori["punteggio"] = giocatori["nominativo"].apply(
        lambda x: migliori_giocatori.loc[x] if x in migliori_giocatori else 0)

    gol = pd.read_excel(f"{read_path}/dbo.gol.xlsx", engine="openpyxl")
    gol["nome"] = gol["id_anagrafica_giocatori"].apply(lambda x: giocatori.loc[x]["nominativo"])
    gol["squadra"] = gol["id_anagrafica_squadre"].apply(lambda x: squadre[str(x)] if x != 0 else "")
    gol["tipo"] = gol["tipo"].apply(lambda x: "Gol" if x == 0 else "Autogol")
    gol_fatti = gol.loc[gol["tipo"] == "Gol"]["nome"].value_counts()
    giocatori["gol"] = giocatori["nominativo"].apply(lambda x: gol_fatti.loc[x] if x in gol_fatti else 0)
    autogol_fatti = gol.loc[gol["tipo"] == "Autogol"]["nome"].value_counts()
    giocatori["autogol"] = giocatori["nominativo"].apply(lambda x: autogol_fatti.loc[x] if x in autogol_fatti else 0)
    giocatori = giocatori.loc[giocatori["cognome"] != "Autogol"]
    giocatori_json_output = {f"calciosplash_{anno}": json.loads(giocatori.T.to_json())}
    with open(f"./../legacy/calciosplash_{anno}/giocatori_{anno}.json", "w") as file:
        json.dump(giocatori_json_output, file)
    giocatori.to_excel(f"./../legacy/calciosplash_{anno}/giocatori_{anno}.xlsx")
    return


def parse_gironi(x, gironi):
    if x < len(gironi):
        return gironi[str(x)]
    else:
        return x


def get_torneo(read_path):
    # qua voglio: {id_partita: ... , squadra1: ... , squadra2: ... , gol1: ... , gol2: ... , falli1: ... , falli2: ..., gialli1: ..., gialli2: ..., rossi1: ..., rossi2: ..., miglior_giocatore: ...,}
    partite = pd.read_excel(f"{read_path}/dbo.partite.xlsx", engine="openpyxl").set_index("id")
    partite = partite.drop(columns=["stato", "note"])
    giocatori = pd.read_excel(f"{read_path}/dbo.anagrafica_giocatori.xlsx", engine="openpyxl").set_index("id")
    giocatori["nominativo"] = giocatori["nome"] + " " + giocatori["cognome"]

    squadre = pd.read_excel(f"{read_path}/dbo.anagrafica_squadre.xlsx", engine="openpyxl").set_index("id")
    squadre = json.loads(squadre["nome"].T.to_json())
    gironi = pd.read_excel(f"{read_path}/dbo.anagrafica_gironi.xlsx", engine="openpyxl").set_index("id")
    genere_gironi = json.loads(gironi["id_anagrafica_sessi"].T.to_json())
    gironi = json.loads(gironi["nome"].T.to_json())
    miglior_giocatore = pd.read_excel(f"{read_path}/dbo.miglior_giocatore.xlsx", engine="openpyxl").set_index("id")
    miglior_giocatore["nome"] = miglior_giocatore["id_anagrafica_giocatori"].apply(
        lambda x: giocatori.loc[x]["nominativo"])

    # partite["nome"] = partite["id_anagrafica_giocatori"].apply(lambda x: giocatori.loc[x]["nominativo"])
    partite["squadra_1"] = partite["id_anagrafica_squadre_1"].apply(lambda x: squadre[str(x)] if x != 0 else "")
    partite["squadra_2"] = partite["id_anagrafica_squadre_2"].apply(lambda x: squadre[str(x)] if x != 0 else "")
    partite["gironi"] = partite["id_anagrafica_gironi"].apply(lambda x: parse_gironi(x, gironi))
    partite["genere_gironi"] = partite["id_anagrafica_gironi"].apply(
        lambda x: genere_gironi[str(x)] if x < len(gironi) else x)

    cartellini = pd.read_excel(f"{read_path}/dbo.cartellini.xlsx", engine="openpyxl").set_index("id")
    gol = pd.read_excel(f"{read_path}/dbo.gol.xlsx", engine="openpyxl")
    gol["nome"] = gol["id_anagrafica_giocatori"].apply(lambda x: giocatori.loc[x]["nominativo"])
    arbitraggio = []
    find_best_portiere = True
    for idx, rows in partite.iterrows():
        giallo1 = cartellini.loc[(cartellini["id_partite"] == idx) & (cartellini["tipo"] == "G") & (
                    cartellini["id_anagrafica_squadre"] == rows["id_anagrafica_squadre_1"])][
            "id_anagrafica_giocatori"].values.tolist()
        giallo2 = cartellini.loc[(cartellini["id_partite"] == idx) & (cartellini["tipo"] == "G") & (
                    cartellini["id_anagrafica_squadre"] == rows["id_anagrafica_squadre_2"])][
            "id_anagrafica_giocatori"].values.tolist()
        rosso1 = cartellini.loc[(cartellini["id_partite"] == idx) & (cartellini["tipo"] == "R") & (
                    cartellini["id_anagrafica_squadre"] == rows["id_anagrafica_squadre_1"])][
            "id_anagrafica_giocatori"].values.tolist()
        rosso2 = cartellini.loc[(cartellini["id_partite"] == idx) & (cartellini["tipo"] == "R") & (
                    cartellini["id_anagrafica_squadre"] == rows["id_anagrafica_squadre_2"])][
            "id_anagrafica_giocatori"].values.tolist()
        giallo1 = [giocatori.loc[x]["nominativo"] for x in giallo1] if len(giallo1) > 1 else ""
        giallo2 = [giocatori.loc[x]["nominativo"] for x in giallo2] if len(giallo2) > 1 else ""
        rosso1 = [giocatori.loc[x]["nominativo"] for x in rosso1] if len(rosso1) > 1 else ""
        rosso2 = [giocatori.loc[x]["nominativo"] for x in rosso2] if len(rosso2) > 1 else ""

        goal_squadra_1 = gol.loc[
            (gol["id_partite"] == idx) & (gol["id_anagrafica_squadre"] == rows["id_anagrafica_squadre_1"]) & (
                        gol["tipo"] == 0)]["nome"].value_counts().to_json()
        goal_squadra_2 = gol.loc[
            (gol["id_partite"] == idx) & (gol["id_anagrafica_squadre"] == rows["id_anagrafica_squadre_2"]) & (
                        gol["tipo"] == 0)]["nome"].value_counts().to_json()

        autogoal_squadra_1 = gol.loc[
            (gol["id_partite"] == idx) & (gol["id_anagrafica_squadre"] == rows["id_anagrafica_squadre_1"]) & (
                        gol["tipo"] == 1)]["nome"].value_counts().to_json()
        autogoal_squadra_2 = gol.loc[
            (gol["id_partite"] == idx) & (gol["id_anagrafica_squadre"] == rows["id_anagrafica_squadre_2"]) & (
                        gol["tipo"] == 1)]["nome"].value_counts().to_json()

        if "tipo" in miglior_giocatore.columns:
            best_giocatori = \
            miglior_giocatore.loc[(miglior_giocatore["id_partite"] == idx) & (miglior_giocatore["tipo"] == "G")][
                ["id_anagrafica_giocatori", "punti"]].values.tolist()
        else:
            best_giocatori = miglior_giocatore.loc[(miglior_giocatore["id_partite"] == idx)][
                ["id_anagrafica_giocatori", "punti"]].values.tolist()
            find_best_portiere = False

        best_giocatore_1 = {}
        best_giocatore_2 = {}
        for giocatore in best_giocatori:
            nome_giocatore = giocatori.loc[giocatore[0]]["nominativo"]
            punti = giocatore[1]
            squadra_giocatore = giocatori.loc[giocatore[0]]["id_anagrafica_squadre"]
            if squadra_giocatore == rows["id_anagrafica_squadre_1"]:
                best_giocatore_1.update({nome_giocatore: punti})
            else:
                best_giocatore_2.update({nome_giocatore: punti})

        best_portiere_1 = {}
        best_portiere_2 = {}
        if find_best_portiere:
            best_portieri = \
            miglior_giocatore.loc[(miglior_giocatore["id_partite"] == idx) & (miglior_giocatore["tipo"] == "P")][
                ["id_anagrafica_giocatori", "punti"]].values.tolist()
            for portieri in best_portieri:
                nome_portiere = giocatori.loc[portieri[0]]["nominativo"]
                punti = portieri[1]
                squadra_portiere = giocatori.loc[portieri[0]]["id_anagrafica_squadre"]
                if squadra_portiere == rows["id_anagrafica_squadre_1"]:
                    best_portiere_1.update({nome_portiere: punti})
                else:
                    best_portiere_2.update({nome_portiere: punti})
        arbitraggio.append((idx, giallo1, giallo2, rosso1, rosso2, goal_squadra_1, goal_squadra_2, autogoal_squadra_1,
                            autogoal_squadra_2, best_giocatore_1, best_giocatore_2, best_portiere_1, best_portiere_2))
    arbitraggio = pd.DataFrame(arbitraggio,
                               columns=["idx", "gialli1", "gialli2", "rossi1", "rossi2", "goleador_1", "goleador_2",
                                        "autogol1", "autogol2", "best_giocatore_1", "best_giocatore_2",
                                        "best_portiere_1", "best_portiere_2"]).set_index("idx")
    partite = partite.join(arbitraggio)

    partite_json_output = {f"torneo_{anno}": json.loads(partite.T.to_json())}
    with open(f"./../legacy/calciosplash_{anno}/torneo_{anno}.json", "w") as file:
        json.dump(partite_json_output, file)
    partite.to_excel(f"./../legacy/calciosplash_{anno}/torneo_{anno}.xlsx")

    punti = pd.read_excel(f"{read_path}/dbo.punti.xlsx", engine="openpyxl")
    # todo: fare sta roba anche qui dai
    return


if __name__ == "__main__":
    for anno in tqdm([2019, 2018, 2017, 2016, 2015, 2014], desc="Reading file from calciosplash"):
        read_path = f'../legacy/calciosplash_{anno}.zip'
        write_path = f'../legacy/calciosplash_{anno}'
        os.makedirs(write_path, exist_ok=True)
        unzip_folder(read_path, write_path)
        get_giocatori(write_path)
        get_torneo(write_path)
