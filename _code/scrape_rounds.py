from bs4 import BeautifulSoup
import requests
import json
from cleantext import clean

# QUA BISOGNA METTERE A POSTO LA STRINGA CHE SCARICHIAMO DAL SITO DEL CALCIOSPLASH (CODIFICA, ETC) es. 'Una quarta in 4 ,\xa0Babybell&&1 &&12'


def parse_text(string):
    parsed_string = clean(string,
                          fix_unicode=True,
                          to_ascii=True,)
    return parsed_string


def get_historical_data(url):
    soup = BeautifulSoup(requests.get(url).text, features="lxml")
    table = soup.find("table")
    data = {"TORNEO": url.split("_")[2][:4],
            "GENERE": url.split("_")[-1]}
    round_name = ""
    try:
        for row in table.findAll("tr"):
            table_data = [x.text.strip()
                          for x in row.findAll("td") if x.text.strip() != ""]
            if len(table_data) == 1:
                if "Girone" in table_data[0]:
                    if round_name == "":
                        pass
                    else:
                        data[round_name]["RISULTATI"] = matches
                        data[round_name]["CLASSIFICA"] = ranking

                    ranking_flag = False
                    matches_flag = False
                    round_name = table_data[0].replace(
                        "\r\n", "").split(" ")[-1]
                    data[round_name] = {}
                else:
                    continue
            else:
                if "Partita" in table_data and "Risultato" in table_data:
                    matches = []
                    ranking_flag = False
                    matches_flag = True
                elif "Squadra" in table_data and "Punti" in table_data and "Gol fatti" in table_data:
                    ranking = []
                    matches_flag = False
                    ranking_flag = True
                else:
                    if matches_flag:
                        if len(table_data) > 1:
                            matches.append(parse_text(",".join([x.replace("\n", "").replace(
                                "\r", "").strip() for x in table_data]).replace("-", ",")))
                    elif ranking_flag:
                        if len(table_data) > 1:
                            ranking.append(parse_text(",".join([x.replace("\n", "").replace(
                                "\r", "").strip() for x in table_data]).replace("-", ",")))

        with open(f"./_storage/{url.split('_')[-1]}_{url.split('_')[2][:4]}.json", "w+") as writer:
            json.dump(data, writer)
    except:
        print(url)


legacy = [
    "http://calciosplashlizzana.altervista.org/site/index.php?mod=20_Torneo_2014/01_Gironi_maschili",
    "http://calciosplashlizzana.altervista.org/site/index.php?mod=20_Torneo_2014/02_Gironi_femminili",
    "http://calciosplashlizzana.altervista.org/site/index.php?mod=21_Torneo_2015/12_Gironi_maschili",
    "http://calciosplashlizzana.altervista.org/site/index.php?mod=21_Torneo_2015/11_Gironi_femminili",
    "http://calciosplashlizzana.altervista.org/site/index.php?mod=22_Torneo_2016/12_Gironi_maschili",
    "http://calciosplashlizzana.altervista.org/site/index.php?mod=22_Torneo_2016/11_Gironi_femminili",
    "http://calciosplashlizzana.altervista.org/site/index.php?mod=23_Torneo_2017/12_Gironi_maschili",
    "http://calciosplashlizzana.altervista.org/site/index.php?mod=23_Torneo_2017/11_Gironi_femminili",
    "http://calciosplashlizzana.altervista.org/site/index.php?mod=24_Torneo_2018/12_Gironi_Maschili",
    "http://calciosplashlizzana.altervista.org/site/index.php?mod=24_Torneo_2018/11_Gironi_Femminili"
    "http://calciosplashlizzana.altervista.org/site/index.php?mod=25_Torneo_2019/12_Gironi_Maschili",
    "http://calciosplashlizzana.altervista.org/site/index.php?mod=25_Torneo_2019/11_Gironi_Femminili"

]
for url in legacy:
    get_historical_data(url)
