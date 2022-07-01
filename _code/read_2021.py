import pymongo
import pandas as pd

client = pymongo.MongoClient("mongodb+srv://gsp:Parma4ever@gsp.pfv6c.mongodb.net/?retryWrites=true&w=majority")
db = client.test

matches = pd.DataFrame().from_records([x for x in client.GSP.matches.find({})])
matches.columns = ["id", "squadra_1", "squadra_2", "gol_squadra_1", "gol_squadra_2", "data", "orario", "genere_gironi",
                   "id", "tempo", "goal", "best_giocatore", "gialli1", "team"]
matches = matches.drop(columns=["id"])

players = pd.DataFrame().from_records([x for x in client.GSP.player.find({})])