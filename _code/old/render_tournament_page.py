import os
import json
import datetime as dt

from table_data import Header, Ranking, Results


class TournamentRenderer():
    def __init__(self, storage_path) -> None:
        self.storage = storage_path
        self.data = None
        self.text = []
        self.emoticon = json.load(open("./_storage/_emoticons.json", "r"))

    def read_data(self, raw):
        with open(f"{self.storage}/{raw}", "r") as handler:
            doc = json.load(handler)
            self.data = doc

    def render(self):
        markdown = []

        # MAKE HEADER
        header = Header(category="torneo",
                        url=f"/tornei/torneo_{self.data['TORNEO']}_{self.data['GENERE'].lower()}").create()
        markdown.append(header)

        # MAKE TITLE
        title = f"<h2>Torneo {self.data['TORNEO']}</h2>"
        markdown.append(title)

        for key in self.data.keys():
            if key == "TORNEO" or key=="GENERE":
                continue
            if self.data[key] == {}:
                continue

            # MAKE ROUND NAME
            try:
                round_name = f"<h3>Girone {key} {self.emoticon[key.lower()]}</h3>"
            except:
                round_name = f"<h3>Girone {key} </h3>"
            markdown.append(round_name)

            # MAKE ROUND
            results = Results(self.data[key]["RISULTATI"]).create()
            markdown.append(results)

            # MAKE RANKING
            ranking = Ranking(self.data[key]["CLASSIFICA"]).create()
            markdown.append(ranking)
            markdown.append("---")

        markdown = "\n\n".join(markdown)

        date = f"{dt.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)}".split(
            ' ')[0]
        with open(f"./posts/{date}_{self.data['TORNEO']}_{self.data['GENERE'].upper()}_tournament.markdown", "w+") as renderer:
            renderer.write(markdown)

    def start(self):
        for doc in os.listdir(self.storage):
            if doc.startswith("_") is False:
                self.read_data(doc)
                self.render()
