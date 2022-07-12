import json
import pandas as pd

#### QUA DEVO CARICARE L'ALBO DORO E METTERCI I GOAL DEL 2021
def render_albodoro():
    #albo_doro = {}
    with open("./../_storage/albo_doro/femminile.json", "r") as file:
        albo_doro = json.load(file)
    with open("./../_storage/albo_doro/maschile.json", "r") as file:
        albo_doro.update(json.load(file))

    for anno in range(2014, 2022):
        try:
            path = f"./../_legacy/calciosplash_{anno}/giocatori_{anno}.json"
            with open(path, "r") as file:
                data = json.load(file)
        except Exception as e:
            print(e)
            continue
        for index, document in data[f"calciosplash_{anno}"].items():
            nome = f"{document['cognome'].strip()} {document['nome'].strip()}"
            if nome not in albo_doro:
                albo_doro[nome] = {anno: document["gol"]}
            else:
                albo_doro[nome].update({anno: document["gol"]})
    print(albo_doro)
    albo_doro = pd.DataFrame(albo_doro).sort_index()
    albo_doro = albo_doro.T.fillna(0).astype(int)
    albo_doro["Totale"] = albo_doro.sum(axis=1)
    albo_doro.sort_values("Totale", ascending=False)


if __name__ == "__main__":
    render_albodoro()
