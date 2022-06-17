"""Za putanje"""
import time
import graph
from msort import *
from projekat2_SV4_2021 import parser_projekat

"""https://www.tutorialspoint.com/python/os_walk.htm"""
"""https://www.geeksforgeeks.org/os-walk-python/"""

import os
from parser_projekat import Parser
import pickle
from glob import iglob
from graph import *
from Trie import *
global lista_svih_file
global veza_linkova
global najvazniji_link_kljuc

veza_linkova = {}
v = Graph()
#trie = Trie()

def pocetak():
    global veza_linkova
    global trie
    global lista_svih_file
    trie = Trie()
    lista_svih_file = [f for f in iglob('python-2.7.7-docs-html/**/*', recursive=True) if os.path.isfile(f)]
    lista_file_html = []
    lista = []
    parser_projekat = Parser()
    for fajl in lista_svih_file:
        zavrsetak = fajl[-4:-1] + fajl[-1]
        if zavrsetak.lower() == "html":
            linkovi, reci = parser_projekat.parse(fajl)
            fajl = os.path.abspath(fajl)
            lista_file_html.append(fajl)
            pom = v.insert_vertex(fajl)
            veza_linkova[pom] = linkovi
            file_trie = fill_trie(fajl, reci)
    print("Broj cvorova u grafu je: ", v.vertex_count())
    napravi_grane(v)
    print("Broj grana u grafu je:",v.edge_count())

def napravi_grane(v):
    for cv in veza_linkova.keys():
        lista_linkova = veza_linkova[cv]
        for i in range(len(lista_linkova)):
            pom_nova = v.insert_vertex(lista_linkova[i])
            if cv != lista_linkova[i]:
                v.insert_edge(cv,pom_nova,None)

def fill_trie(fajl, reci):
    global trie
    #trie = Trie()
    """Ovde se gleda i podstring"""
    for i in range(len(reci)):
        if not reci[i]:
            continue
        rec = reci[i].lower()
        trie.insert(rec, fajl, i)
    return trie

def unos():
    global lista_svih_file
    heuristika = 0
    heuristika_recnik = {}
    lista_broja_reci = []

    tekst_koji_se_trazi = input("\nUnesite tekst koji zelite da pretrazite (exit za izlaz)").lower().strip()
    if tekst_koji_se_trazi.lower().strip()=="exit":
        print("Izasli ste")
        return False
    lista_trie = trie.search(tekst_koji_se_trazi)
    broj_ponavljanja_reci = trie.broj_ponavljanja(tekst_koji_se_trazi)
    heuristika = broj_ponavljanja_reci             #dodati dodatno ono
    for key in lista_trie:
        #print(key)
        #print(lista_trie[key])
        broj_reci = len(lista_trie[key])
        lista_broja_reci.append(broj_reci)
        heuristika_vrednost = broj_reci
        heuristika_recnik[key] = heuristika_vrednost

    lista_vr = []
    for key in heuristika_recnik:
        lista_vr.append(heuristika_recnik[key])

    lista_vr_sort = lista_vr
    lista_vr_sort = sort(lista_vr_sort)
    for i in range(len(lista_vr_sort)//2):
        lista_vr_sort[i],lista_vr_sort[len(lista_vr_sort)-1-i] = lista_vr_sort[len(lista_vr_sort)-1-i],lista_vr_sort[i]

    # print("SORT LISTA")
    # print("Sortiran dict")
    # for val in sorted(heuristika_recnik.values()):
    #     for key in heuristika_recnik:
    #         if heuristika_recnik[key] == val:
    #             print("U ovom file se nalazi", key,", sa ", val, "pojavljivanja reci",tekst_koji_se_trazi)
    #             # broj_stanica = input("Unesite broj stranica koje zelite da vam se prikaze")
    #             # broj_stanica = int(broj_stanica)

    iskorisceni_file = []
    broj_strana = input("Unesite koliko stranica zeli da vam se prikaze")
    broj_strana = int(broj_strana)
    br = 0
    #for val in sort(lista_vr):
    for val in lista_vr_sort[0:broj_strana]:
        for key in heuristika_recnik:
            if heuristika_recnik[key] == val and key not in iskorisceni_file and br<broj_strana:
                iskorisceni_file.append(key)
                br +=1
                print("U ovom file se nalazi", key, ", sa ", val, "pojavljivanja reci", tekst_koji_se_trazi)

    global najvazniji_link_kljuc
    najvazniji_link_vrednost = lista_vr_sort[0]
    for key in heuristika_recnik:
        if heuristika_recnik[key] == najvazniji_link_vrednost:
            najvazniji_link_kljuc = key
    print(najvazniji_link_kljuc)
    parser_projekat = Parser()
    reci_za_ispis = parser_projekat.parse(najvazniji_link_kljuc)[1]
    print(reci_za_ispis)
    print("TEKST IZ FILE",najvazniji_link_kljuc)
    print("------------------------------------------------------------------")
    index = 0
    brojac = 0
    granica = 10
    for rec in reci_za_ispis:
        index +=1
        if rec.lower() == tekst_koji_se_trazi.lower() and brojac==0:
            if(len(reci_za_ispis)-index)<10:
                granica = len(reci_za_ispis)-index
            while brojac < granica:
                print(reci_za_ispis[index+brojac],end=" ")
                brojac+=1
            break
    unos()

def main():
    start = time.time()
    pocetak()
    end = time.time()
    print("Vreme da se napravi graf i popuni Trie je: ", end-start)
    unos()

if __name__=="__main__":
    main()