import json
from datetime import datetime as dt

TEMPLATE_NAME = "template_albo.markdown"


def clean(string):
    to_replace = {"à": "a'", "ò": "o", "ì": "i'"}
    if string.isascii():
        return string
    else:
        for token in to_replace.keys():
            string = string.replace(token, to_replace[token])
        return string


def load_template():
    with open(f"./_storage/{TEMPLATE_NAME}", "r") as file:
        template = file.read()
    file.close()
    return template


def create_albo(data):
    albo = []
    columns = ["GOL", "NOMINATIVO", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17",
               "18", "19"]
    albo.append("|".join(columns))
    albo.append("|:-----:|-----------|-------|------|------|------|")
    for player_history in data[1:]:
        albo.append("|".join([clean(data) if data != "" else " " for data in player_history.values()]))
    albo = "\n".join(albo)
    return albo


def fill_template(data, template):
    template = template.replace("DATA_ALBO", f"{dt.now()}")
    template = template.replace("URL_ALBO", f"/albo/{data[0]['GENERE']}")
    albo = create_albo(data)
    template = template.replace("ALBO_DORO", albo)
    return template


if __name__ == "__main__":
    docs = ["femminile",
            "maschile"]

    for doc in docs:
        print(f"Rendering {doc}")
        with open(f"./_storage/albo_doro/{doc}.json", "r") as file:
            data = json.load(file)
        file.close()
        template = load_template()
        template = fill_template(data, template)
        with open(f"./albo_doro/{doc}.markdown", encoding="Latin-1", mode="w") as file:
            file.write(template)
        file.close()
