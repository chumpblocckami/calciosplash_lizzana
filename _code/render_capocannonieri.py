import json
import pandas as pd
import datetime as dt


#### QUA DEVO CARICARE L'ALBO DORO E METTERCI I GOAL DEL 2021
def load_albodoro():
    with open("./../_storage/albo_doro/femminile.json", "r") as file:
        femminile = json.load(file)
    femminile = {x["NOMINATIVO"]: x for x in femminile[1:]}
    with open("./../_storage/albo_doro/maschile.json", "r") as file:
        maschile = json.load(file)
    maschile = {x["NOMINATIVO"]: x for x in maschile[1:]}

    femminile.update(maschile)
    albo_doro = pd.DataFrame().from_dict(femminile).T.drop(columns=["NOMINATIVO", "GOL"])
    albo_doro = albo_doro.apply(lambda row: row.str.strip().replace("", "0"))
    albo_doro = albo_doro.T.to_dict()
    for anno in range(2004, dt.datetime.now().year):
        nome_anno = str(anno)[-2:]
        goals_anno = []
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
                albo_doro[nome] = {nome_anno: document["gol"]}
            else:
                if nome in albo_doro and nome_anno in albo_doro[nome] and document["gol"] != int(albo_doro[nome][nome_anno]):
                    print(f"Anno {anno} - {nome}: Goal secondo i dati: {document['gol']}, Goal secondo l'annuario: {albo_doro[nome][nome_anno]}")
                else:
                    albo_doro[nome].update({nome_anno: document["gol"]})
    albo_doro = pd.DataFrame(albo_doro).sort_index()
    albo_doro = albo_doro.T.fillna(0).astype(int)
    albo_doro["Totale"] = albo_doro.sum(axis=1)
    albo_doro = albo_doro.sort_values("Totale", ascending=False)
    albo_doro.to_csv("./../_legacy/albo_doro.csv")
    albo_doro = albo_doro.loc[albo_doro["Totale"] > 0]
    albo_doro = albo_doro[albo_doro.columns.sort_values(ascending=False)]
    albo_doro_indice = albo_doro["Totale"].reset_index().reset_index().set_index("index")
    albo_doro_indice.columns = ["Posizione", "Goals"]
    with open(f"./../_legacy/palmares.json", encoding="UTF-8", mode="w") as file:
        json.dump(albo_doro_indice.T.to_dict(),file)
    file.close()

    return albo_doro


def render_albodoro(albodoro):
    markdown = []
    markdown.append("\n".join(["---", "layout: post", f"date: {dt.datetime.now()}", "categories: albo_doro", "permalink: albo_doro/goleador", "---",
                               "<link rel='stylesheet' href='../../assets/style.css'>"]))
    markdown.append("\n")
    albodoro = albodoro.T.to_dict()
    flag = True
    n = 1
    for nome, trends in albodoro.items():
        if flag:
            table_header = "|POS|GOAL|NOME|" + "|".join([str(x) for x in trends.keys()][1:]) + "|"
            markdown.append(table_header)
            table_separator = "|:---:|" + "|".join(["---" for _ in range(len(trends.keys()) + 1)]) + "|"
            markdown.append(table_separator)
            flag = False
        history = "|".join([str(x) if x != 0 else "" for x in trends.values()][1:]) + "|"
        if n == 1:
            row = f"{n}🥇|**{trends['Totale']}**|{nome}|{history}"
        elif n == 2:
            row = f"{n}🥈|**{trends['Totale']}**|{nome}|{history}"
        elif n == 3:
            row = f"{n}🥉|**{trends['Totale']}**|{nome}|{history}"
        else:
            row = f"{n}|**{trends['Totale']}**|{nome}|{history}"
        markdown.append(row)
        n = n + 1
    with open(f"./../albo_doro/goleador.markdown", encoding="UTF-8", mode="w") as file:
        file.write("\n".join(markdown))
    file.close()


if __name__ == "__main__":
    albo = load_albodoro()
    render_albodoro(albo)
