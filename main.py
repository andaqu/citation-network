from networkx_viewer import Viewer
import networkx as nx
import bibtexparser
import requests 

edges = []
nodes = {}

def build():
    
    print("Input absolute path of your bibtex or biblatex file")
    read = input()

    bib = open(read)
    bib = bibtexparser.load(bib)

    for e in bib.entries:
        try:
            nodes[e["doi"]] = e["ID"]
        except KeyError:
            print("(!) No doi found for " + e["ID"] + "! Skipping...")
            continue
        
    for n1 in nodes:
        print("Checking who " + nodes[n1] + " cited...")
        # n1 is doi (node 1)
        url = f"https://opencitations.net/index/coci/api/v1/citations/{n1}"

        r = requests.get(url)
        data = r.json()
        
        if(data == []):
            print(f"(!) Unforunately API didn't provide any citations for: {nodes[n1]}")
            continue

        for d in data:
            
            n2 = d['citing']
            if n2 in nodes:
                edges.append([nodes[n2], nodes[n1]])

    with open('edges.txt', 'w') as f:
        for e in edges:
            f.write(f"{e[0]} {e[1]}\n")

def draw():
    edge_list_path = r"edges.txt"
    DG = nx.read_edgelist(edge_list_path,create_using=nx.DiGraph())

    app = Viewer(DG)
    app.mainloop()

while True:
    print("Input: 1 -> to build citation network, 2 -> to draw it")
    menu = input()

    if menu == "1":
        build()
        print("Done! You can draw it now")
    elif menu == "2":
        draw()
    else:
        print("OK")
    

    