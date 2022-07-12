import os

def render():
    markdown = []
    header = "\n".join(["---", "layout: page", "title: Giocatori", "permalink: /giocatori", "---"])
    markdown.append(header)
    markdown.append("\n")
    markdown.append("---")
    markdown.append("\n")
    row = ""
    pagine_giocatori = os.listdir("./../giocatori")
    pagine_giocatori.sort()
    alfabeto = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,z".split(",")
    giocatori_ordinati = []
    for lettera in alfabeto:
        giocatori_tmp = []
        for giocatore in pagine_giocatori:
            if giocatore.startswith(lettera):
                giocatori_tmp.append(giocatore)
        giocatori_ordinati.append(giocatori_tmp)

    for nn,pagine_giocatori in enumerate(giocatori_ordinati):
        markdown.append("\n".join([alfabeto[nn].upper(),"\n","---","\n"]))
        for n, giocatori in enumerate(pagine_giocatori):
            n=n+1
            giocatori = giocatori.replace(".markdown","")
            giocatore = " ".join([x.capitalize() for x in giocatori.split("_")])
            row += " | " + f"[{giocatore}](/giocatore/{giocatori})"
            if n % 3 == 0:
                row = row + ""
                markdown.append(row)
                row = ""
            if n == len(pagine_giocatori):
                row+= " \n"
                markdown.append(row)
                row = ""



    #if markdown[-1].endswith("|") == False:
    #    markdown[-1]+=" |"

    markdown = "\n".join(markdown)

    with open(f"./../giocatori.markdown", "w", encoding="utf-8") as file:
        file.write(markdown)

