import json
import copy
import datetime as dt
from tqdm import tqdm
import render_giocatori_page

with open(f"./../_legacy/palmares_definitivo.json", "r", encoding="UTF-8") as file:
    palmares = json.load(file)
file.close()


def join_player_data():
    player_data = {}
    for anno in [2021, 2019, 2018, 2017, 2016, 2015, 2014]:
        path = f"./../_legacy/calciosplash_{anno}/giocatori_{anno}.json"
        with open(path, "r", encoding="UTF-8") as file:
            data = json.load(file)
        file.close()
        for index, document in data[f"calciosplash_{anno}"].items():
            if document["nominativo"] not in player_data:
                player_data[document["nominativo"]] = {}
                player_data[document["nominativo"]]["soprannome"] = document["soprannome"]
            tmp_document = copy.deepcopy(document)
            del tmp_document["nominativo"]
            del tmp_document["soprannome"]
            del tmp_document["nome"]
            del tmp_document["cognome"]
            del tmp_document["id_anagrafica_squadre"]
            player_data[document["nominativo"]].update({anno: tmp_document})
    print(len(player_data))


def render_player_page(nome):
    player_data = {"anni": [],
                   "soprannome": {},
                   "goal": {},
                   "squadra": {},
                   "gialli": {},
                   "rossi": {},
                   "best": {},
                   "punteggio": {},
                   "autogol": {}, }
    player_data["nome"] = nome
    for anno in [2021, 2019, 2018, 2017, 2016, 2015, 2014]:
        path = f"./../_legacy/calciosplash_{anno}/giocatori_{anno}.json"
        with open(path, "r") as file:
            data = json.load(file)
        for index, document in data[f"calciosplash_{anno}"].items():
            if f"{document['cognome'].strip()} {document['nome'].strip()}" != nome:
                continue
            player_data[f"soprannome"].update({anno: document["soprannome"]})
            player_data[f"goal"].update({anno: document["gol"]})
            player_data[f"squadra"].update({anno: document["squadra"]})
            player_data[f"gialli"].update({anno: document["gialli"]})
            player_data[f"rossi"].update({anno: document["rossi"]})
            player_data[f"best"].update({anno: document["n_best"]})
            player_data[f"punteggio"].update({anno: document["punteggio"]})
            player_data[f"autogol"].update({anno: document["autogol"]})
            player_data["anni"].append(anno)

    markdown = ["\n".join(["---",
                           "layout: post", f"date: {dt.datetime.now()}",
                           "categories: torneo",
                           f"permalink: /giocatore/{nome.lower().replace(' ', '_')}/",
                           "---"])]

    markdown.append("<link rel='stylesheets' href='./../assets/giocatori.css'>\n")

    # title and image
    nominativo = nome if "".join(player_data['soprannome'].values()) == "" else f"{nome} ({max(player_data['soprannome'].values())})"
    nominativo = nominativo.lstrip().rstrip().replace('\n','').replace("\r","")
    titolo = "\n".join([f"| {nominativo} |", "|:-----:|",
                        f"| ![Immagine mancante]('./../../assets/giocatori/{nome.lower().replace(' ', '_')}.png)" + "{:.immagine_giocatori} |"])
    tabella_carriera = "\n".join(
        [f"|{y}|{player_data['squadra'][y].strip()}|{player_data['soprannome'][y].strip()}|" for y in
         player_data["anni"]])
    carriera = "\n".join(["## Carriera",
                          "----\n",
                          "|Anno|Squadra|Soprannome|",
                          "|:---:|---|---|",
                          tabella_carriera])

    # goals
    tabella_goal = "|Goal|" + "|".join([f"{player_data['goal'][y]}" for y in player_data["anni"]]) + "|" + str(
        sum([player_data['goal'][y] for y in player_data["anni"]])) + "|"
    tabella_autogol = "|Autogoal|" + "|".join(
        [f"{player_data['autogol'][y]}" for y in player_data["anni"]]) + "|" + str(
        sum([player_data['autogol'][y] for y in player_data["anni"]])) + "|"
    goal = "\n".join(["## Goal",
                      "----\n",
                      "| " + "".join([f"|{y}" for y in player_data["anni"]]) + "| Totale |",
                      "|---" + "".join([f"|---" for _ in player_data["anni"]]) + "|---|",
                      tabella_goal,
                      tabella_autogol])
    # statistics
    tabella_gialli = "|Gialli|" + "|".join([f"{player_data['gialli'][y]}" for y in player_data["anni"]]) + "|" + str(
        sum([player_data['gialli'][y] for y in player_data["anni"]])) + "|"
    tabella_rossi = "|Rossi|" + "|".join([f"{player_data['rossi'][y]}" for y in player_data["anni"]]) + "|" + str(
        sum([player_data['rossi'][y] for y in player_data["anni"]])) + "|"
    tabella_best = "|Best player|" + "|".join([f"{player_data['best'][y]}" for y in player_data["anni"]]) + "|" + str(
        sum([player_data['best'][y] for y in player_data["anni"]])) + "|"
    tabella_stelle = "|Stelle|" + "|".join([f"{player_data['punteggio'][y]}" for y in player_data["anni"]]) + "|" + str(
        sum([player_data['punteggio'][y] for y in player_data["anni"]])) + "|"

    statistiche = "\n".join(["## Statistiche",
                             "----\n",
                             "| " + "".join([f"|{y}" for y in player_data["anni"]]) + "| Totale |",
                             "|---" + "".join([f"|---" for _ in player_data["anni"]]) + "|---|",
                             tabella_gialli,
                             tabella_rossi,
                             tabella_best,
                             tabella_stelle])

    if nome in palmares:
        pos = palmares[nome]["Posizione"] + 1 if type(palmares[nome]["Posizione"]) == int else palmares[nome]["Posizione"]
        totale_goals = palmares[nome]["Goals"]
        premi = palmares[nome]["Premi"] if "Premi" in palmares[nome] else []
        posizione = "\n".join(["## Palmares",
                               "----\n",
                               f"- **{pos}°** posto per goal segnati (goal fatti: {totale_goals})",
                               "\n".join([f"- {x}" for x in premi])
                               ])
    else:
        posizione = "\n".join(["## Palmares",
                               "----\n",
                               f"**Impegnete de pu! Grinta!!!! Mai subire zo bire!!🍻🍻** "
                               ])

    markdown.append(titolo)
    markdown.append("\n")
    markdown.append(carriera)
    markdown.append("\n")
    markdown.append(goal)
    markdown.append("\n")
    markdown.append(statistiche)
    markdown.append("\n")
    markdown.append(posizione)

    output = "\n".join(markdown)
    with open(f"./../giocatori/{nome.lower().replace(' ', '_')}.markdown", "w", encoding="utf-8") as file:
        file.write(output)


if __name__ == "__main__":
    giocatori = ["Zandonati Stefania", "Barbiero Riccardo", "Zandonati Stefania", "Raffaelli Davide", "Pilati Matteo", "Alovisi Filippo", "Manica Davide",
                 "Baldo Riccardo", "Prezzi Margherita", "Tovazzi Irene", "Chiusole Cecilia", "Deimichei Chiara",
                 "Brentari Gabriele", "Graziola Andrea",
                 "Monaco Alessandro", "Finarolli Alice", "Giordani Luca", "Maraner Matteo", "Zendri Carolina",
                 "Feller Daniele", "Giordani Andrea", "Zaffoni Michele", "Martini Simone", "Battisti Isotta",
                 "Valduga Emanuele", "Feltrinelli Daniele", "Raffaelli Melany", "Osele Veronica",
                 "Giordani Nicolas", "Conzatti Andrea", "Maffei Alessandro", "De Zambotti Davide",
                 "De Zambotti Giacomo", "Di Meo Samuel", "Zambanini Vanessa", "Miorandi Emanuele", "Bertolini Michele",
                 "Frasca Luca", "Cescatti Manuel", "Pedrotti Serena", "Rigo Anna",
                 "Ceschini Leonardo", "Miorandi Emanuele",
                 "Mazzola Matteo", "Parisi Leonardo", "Anzelini Andrea", "Gerola Marco", "Pizzini Stefano", "Gazzini Stefania",
                 "Sala Marco", "Tesini Emma", "Pomarolli Federico", "Manconi Laura", "Manconi Matteo", "Pomarolli Carlotta",
                 "Scrinzi Giulia", "Gober Andrea", "Pomarolli Edoardo", "Incandela Angela", "Giordani Federico", "Russo Omar",
                 "Pedrotti Serena", "Stedile Giulia", "Gottardi Cristina", "Vettori Francesco", "Lanaro Fabrizio", "Ceriani Silvia",
                 "Festi Mattia", "Bottesi Margherita", "Manzana Silvia", "Tita Stefano", "Chiodini Massimo", "Sartori Francesca",
                 "Finarolli Alice", "Dalbosco Daniele", "Turchini Giorgia", "Debiasi Thomas", "Parisi Michele", "Marangoni Alessandra",
                 "Loss Elena", "Togni Nicola", "Castelletti Peter", "Azzolini Elisabetta", "Prezzi Matteo", "Lorandi Chiara",
                 "Frasca Luca", "Arlanch Giorgia", "Tovazzi Irene", "Stedile Carlo", "Bertolini Andrea", "Merighi Michele",
                 "Viola Leonardo", "Maraner Matteo", "Prezzi Sara", "Raffelli Melany"]

    for giocatore in tqdm(giocatori, desc="rendering players..."):
        try:
            render_player_page(giocatore)
        except Exception as e:
            print("Cannot render " + giocatore + ". " + str(e))
    render_giocatori_page.render()