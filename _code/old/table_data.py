import datetime as dt


class Header():
    def __init__(self, category, url) -> None:
        self.data = {"layout": "post",
                     "date": dt.datetime.now().replace(microsecond=0),
                     "categories": category,
                     "permalink": f"/{url}/",
                     }
        self.text = []
        self.separator = "---"

    def create(self):
        self.text.append(self.separator)
        for key, value in self.data.items():
            self.text.append(f"{key}: {value}")
        self.text.append(self.separator)
        markdown = "\n".join(self.text)
        return markdown


class Results():
    def __init__(self, data):
        self.table = [
            "|  |  | **RISULTATI** |  |  |",
            "|:---:|:---:|:---:|:---:|:---:|"
        ]
        self.data = data

    def create(self):
        for doc in self.data:
            doc = doc.replace(", ","&&")
            team1, team2, score1, score2 = [x for x in doc.split("&&") if x!=""]
            row = f"|  {team1} | vs.|  {team2} | - | {score1} | {score2} |"
            self.table.append(row)
        markdown = "\n".join(self.table)+"\n"
        return markdown


class Ranking():
    def __init__(self, data):
        self.table = [
            "|  |  | **CLASSIFICA** |  |  |",
            "|:---:|:---:|:---:|:---:|:---:|",
            "|squadra|punteggio|goal fatti|goal subiti|diff. reti|"
        ]
        self.data = data

    def create(self):
        for doc in self.data:
            team, points, goals, not_goals, diff_goal= [x for x in doc.split("&&") if x!=""]

            row = f"|  {team} |   {points} |  {goals} | {not_goals} | {diff_goal} |"
            self.table.append(row)
        markdown = "\n".join(self.table)+"\n"
        return markdown
