from render_tournament_page import TournamentRenderer

class Speaker():
    def start(self):
        ponzio_pilati = TournamentRenderer("./_storage")
        ponzio_pilati.start()

if __name__ == "__main__":
    zorro = Speaker()
    zorro.start()
    print("TRIPLICE FISCHIO")