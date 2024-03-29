"""Za putanje"""
"""python-2.7.7-docs-html\\library\\"""
"""python-2.7.7-docs-html\\c-api\\"""

import time
from msort import *
import os
from parser_projekat import Parser
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
    pitanje = input("Da li zelite da unosite putanju (DA/NE)")
    if pitanje.lower()=="ne":
        lista_svih_file = [f for f in iglob('python-2.7.7-docs-html/**/*', recursive=True) if os.path.isfile(f)]
    else:
        putanja = input("Unesite putanju")
        #print(putanja)
        lista_svih_file = [f for f in iglob(putanja+"/**/*", recursive=True) if os.path.isfile(f)]
    lista_file_html = []
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
    #print(lista_file_html)
    if len(lista_file_html)==0:
        print("Uneli ste pogresan direktorijum ili u direktorijumu nema html stranica")
        return False

    #print("Broj cvorova u grafu je: ", v.vertex_count())
    napravi_grane(v)
    #print("Broj grana u grafu je:",v.edge_count())

def napravi_grane(v):
    for cv in veza_linkova.keys():
        lista_linkova = veza_linkova[cv]
        for i in range(len(lista_linkova)):
            pom_nova = v.insert_vertex(lista_linkova[i])
            v.insert_edge(cv,pom_nova)

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

    tekst_koji_se_trazi = input("\nUnesite tekst koji zelite da pretrazite (exit za izlaz)").lower().strip()

    if tekst_koji_se_trazi.lower().strip() == "exit":
        print("Izasli ste")
        return False

    """Treba dodati ovde elif al to posle"""
    if " " not in tekst_koji_se_trazi:
        print("JEDNA REC")
        h = racunanje_vr_jedna_rec(tekst_koji_se_trazi)
        if h == False:
            return False
        ispis_file(h,tekst_koji_se_trazi)
    else:
        if "and" in tekst_koji_se_trazi:
            print("AND FUNKCIJA")
            funkcija_and(tekst_koji_se_trazi)

        elif "or" in tekst_koji_se_trazi:
            print("OR FUNKCIJA")
            funkcija_or(tekst_koji_se_trazi)

        elif "not" in tekst_koji_se_trazi:
            print("NOT FUNKCIJA")
            funkcija_not(tekst_koji_se_trazi)
        else:
            print("VISESLOZNOST")
            visesloznost(tekst_koji_se_trazi)

def racunanje_vr_jedna_rec(tekst_koji_se_trazi):
    heuristika_recnik = {}
    lista_broja_reci = []
    lista_trie = trie.search(tekst_koji_se_trazi)
    if len(lista_trie)==0:
        print("Ne postoji trazena rec")
        return False
    broj_ponavljanja_reci = trie.broj_ponavljanja(tekst_koji_se_trazi)

    """Ovo je za broj reci"""
    for key in lista_trie:
        broj_reci = len(lista_trie[key])
        lista_broja_reci.append(broj_reci)
        heuristika_vrednost = broj_reci
        heuristika_recnik[key] = heuristika_vrednost

    """ovo je za broj linkov"""
    for key in heuristika_recnik:
        zbir = 0
        stepen= 0
        for iterator in v.vertices():
            if key == iterator.element():
                stepen = v.degree(iterator,False)
                odlazni_cvor = v.incident_edges(iterator,False)
                for nes in odlazni_cvor:
                    pom = nes.opposite(iterator)
                    if pom.element() in heuristika_recnik.keys():
                        zbir = zbir + heuristika_recnik[pom.element()]

        heuristika_recnik[key] += 0.01*stepen + 0.01*zbir

    return heuristika_recnik

def ispis_file(heuristika_recnik,tekst_koji_se_trazi):
    lista_vr = []
    for key in heuristika_recnik:
        lista_vr.append(heuristika_recnik[key])

    lista_vr_sort = lista_vr
    lista_vr_sort = sort(lista_vr_sort)
    for i in range(len(lista_vr_sort) // 2):
        lista_vr_sort[i], lista_vr_sort[len(lista_vr_sort) - 1 - i] = lista_vr_sort[len(lista_vr_sort) - 1 - i], lista_vr_sort[i]

    iskorisceni_file = []
    broj_strana = input("Unesite koliko stranica zeli da vam se prikaze")
    while True:
        if not broj_strana.isnumeric():
            broj_strana = input("Unesite koliko stranica zeli da vam se prikaze")
        else:
            broj_strana = int(broj_strana)
            break
    br = 0
    for val in lista_vr_sort[0:broj_strana]:
        for key in heuristika_recnik:
            if heuristika_recnik[key] == val and key not in iskorisceni_file and br < broj_strana:
                iskorisceni_file.append(key)
                br += 1
                print("U ovom file se nalazi", key, ", sa ", round(val), "RANGOM ", tekst_koji_se_trazi)

    global najvazniji_link_kljuc
    najvazniji_link_vrednost = lista_vr_sort[0]
    for key in heuristika_recnik:
        if heuristika_recnik[key] == najvazniji_link_vrednost:
            najvazniji_link_kljuc = key
    parser_projekat = Parser()
    reci_za_ispis = parser_projekat.parse(najvazniji_link_kljuc)[1]
    print("\n\nTEKST IZ FILE", najvazniji_link_kljuc)
    print("------------------------------------------------------------------")

    izadji = False
    granica = 10
    print("\n")
    if "i ne" in tekst_koji_se_trazi.lower():
        tekst_koji_se_trazi=tekst_koji_se_trazi.strip().lower()
        reci_trazene = tekst_koji_se_trazi.split("i ne")
        prvi_sep = reci_trazene[0]
        prvi_sep = prvi_sep.strip()
        drugi_sep = reci_trazene[-1]
        drugi_sep = drugi_sep.strip()
        print(prvi_sep,drugi_sep)
        for i in range(len(reci_za_ispis)):
            rec = reci_za_ispis[i].lower()
            if rec == prvi_sep or rec == drugi_sep:
                print(rec,end=": ")
                if len(reci_za_ispis)-i<10:
                    granica = len(reci_za_ispis)-i-1
                for j in range(granica):
                    print(reci_za_ispis[i + j], end=" ")
                break
    else:
        if " i " in tekst_koji_se_trazi.lower():
            tekst_koji_se_trazi = tekst_koji_se_trazi.strip().lower()
            reci_trazene = tekst_koji_se_trazi.split(" i ")
            prvi_sep = reci_trazene[0]
            prvi_sep = prvi_sep.strip()
            drugi_sep = reci_trazene[-1]
            drugi_sep = drugi_sep.strip()
            for i in range(len(reci_za_ispis)):
                rec = reci_za_ispis[i].lower()
                if rec == prvi_sep or rec == drugi_sep:
                    print(rec, end=": ")
                    if len(reci_za_ispis) - i < 10:
                        granica = len(reci_za_ispis) - i - 1
                    for j in range(granica):
                        print(reci_za_ispis[i + j], end=" ")
                    break
        else:
            if " ili " in tekst_koji_se_trazi.lower():
                tekst_koji_se_trazi = tekst_koji_se_trazi.strip().lower()
                reci_trazene = tekst_koji_se_trazi.split(" ili ")
                prvi_sep = reci_trazene[0]
                prvi_sep = prvi_sep.strip()
                drugi_sep = reci_trazene[-1]
                drugi_sep = drugi_sep.strip()
                for i in range(len(reci_za_ispis)):
                    rec = reci_za_ispis[i].lower()
                    if rec == prvi_sep or rec == drugi_sep:
                        print(rec, end=": ")
                        if len(reci_za_ispis) - i < 10:
                            granica = len(reci_za_ispis) - i - 1
                        for j in range(granica):
                            print(reci_za_ispis[i + j], end=" ")
                        break
            else:
                tekst_koji_se_trazi = tekst_koji_se_trazi.strip().lower()
                reci_trazene = tekst_koji_se_trazi.split(",")
                for i in range(len(reci_trazene)):
                    if reci_trazene[i]!="":
                        for j in range(len(reci_za_ispis)):
                            rec = reci_za_ispis[j].lower()
                            if rec == reci_trazene[i]:
                                print(rec, end=": ")
                                if len(reci_za_ispis) - j < 10:
                                    granica = len(reci_za_ispis) - j - 1
                                for k in range(granica):
                                    print(reci_za_ispis[j + k], end=" ")
                                print("\n")
                                izadji = True
                                break
                        if izadji==True:
                            break


    da_li_zelite_novi_dir = input("\nDa li zelite pretrazite novi direktorijum").lower().strip()
    if da_li_zelite_novi_dir == "ne":
        unos()
    else:
        main()

def visesloznost(tekst_koji_se_trazi):
    tekst_podeljen = tekst_koji_se_trazi.split(" ")
    novi_str = ""
    heuristika_za_vise_reci = {}
    for i in range(len(tekst_podeljen)):
        if tekst_podeljen[i] != "":
            novi_str = novi_str + tekst_podeljen[i] + ","
            heu = racunanje_vr_jedna_rec(tekst_podeljen[i])
            if heu == False:
                return False
            for key1 in heu:
                if key1 not in heuristika_za_vise_reci:
                    heuristika_za_vise_reci[key1] = heu[key1]
                else:
                    heuristika_za_vise_reci[key1] = heuristika_za_vise_reci[key1] + heu[key1]
    if len(heuristika_za_vise_reci) == 0:
        print("Nema takvog fajla")
        unos()
    ispis_file(heuristika_za_vise_reci, novi_str[:-1])

def funkcija_or(tekst_koji_se_trazi):
    tekst_podeljen = tekst_koji_se_trazi.split("or")
    novi_str = ""
    heuristika_za_vise_reci = {}
    for i in range(len(tekst_podeljen)):
        tekst_podeljen[i] = tekst_podeljen[i].strip()
        if tekst_podeljen[i] != "":
            novi_str = novi_str + tekst_podeljen[i] + ","
            heu = racunanje_vr_jedna_rec(tekst_podeljen[i])
            if heu == False:
                return False
            for key1 in heu:
                if key1 not in heuristika_za_vise_reci:
                    heuristika_za_vise_reci[key1] = heu[key1]
                else:
                    heuristika_za_vise_reci[key1] = heuristika_za_vise_reci[key1] + heu[key1]
    if len(heuristika_za_vise_reci) == 0:
        print("Nema takvog fajla")
        unos()
    ispis_file(heuristika_za_vise_reci, novi_str[:-1])

def funkcija_or_ponovo(tekst_koji_se_trazi):
        tekst_podeljen = tekst_koji_se_trazi.split("or")
        prva_rec = tekst_podeljen[0].strip()
        druga_rec = tekst_podeljen[1].strip()
        novi_str = prva_rec+" ili " + druga_rec
        heuristika_or = {}
        heuristika_1_rec = racunanje_vr_jedna_rec(prva_rec)
        if heuristika_1_rec == False:
            return False
        heuristika_2_rec = racunanje_vr_jedna_rec(druga_rec)
        if heuristika_2_rec == False:
            return False

        for key in heuristika_1_rec:
            if key not in heuristika_or:
                heuristika_or[key]=heuristika_1_rec[key]

        for key in heuristika_2_rec:
            if key not in heuristika_or:
                heuristika_or[key]=heuristika_2_rec[key]
            else:
                heuristika_or[key] +=heuristika_2_rec[key]

        print(heuristika_or)
        ispis_file(heuristika_or,novi_str)

def funkcija_and(tekst_koji_se_trazi):
    tekst_podeljen = tekst_koji_se_trazi.split("and")
    prva_rec = tekst_podeljen[0].strip()
    druga_rec = tekst_podeljen[1].strip()
    novi_str = prva_rec +" i "+druga_rec
    heuristika_and = {}
    heuristika_1_rec = racunanje_vr_jedna_rec(prva_rec)
    if heuristika_1_rec == False:
        return False
    heuristika_2_rec = racunanje_vr_jedna_rec(druga_rec)
    if heuristika_2_rec == False:
        return False
    for key in heuristika_1_rec:
        if key in heuristika_2_rec:
            heuristika_and[key] = heuristika_1_rec[key] + heuristika_2_rec[key]
    if len(heuristika_and) == 0:
        print("Nema takvog fajla")
        unos()
    ispis_file(heuristika_and,novi_str)

def funkcija_not(tekst_koji_se_trazi):
    tekst_podeljen = tekst_koji_se_trazi.split("not")
    prva_rec = tekst_podeljen[0].strip()
    druga_rec = tekst_podeljen[1].strip()
    novi_str = prva_rec + " i ne " + druga_rec
    heuristika_not = {}
    heuristika_1_rec = racunanje_vr_jedna_rec(prva_rec)
    if heuristika_1_rec == False:
        return False
    heuristika_2_rec = racunanje_vr_jedna_rec(druga_rec)
    if heuristika_2_rec == False:
        return False
    for key in heuristika_1_rec:
        if key not in heuristika_2_rec:
            heuristika_not[key] = heuristika_1_rec[key]
    if len(heuristika_not) == 0:
        print("Nema takvog fajla")
        unos()
    ispis_file(heuristika_not, novi_str)

def main():
    start = time.time()
    pocetak()
    end = time.time()
    print("Vreme da se napravi graf i popuni Trie je: ", end-start)
    unos()

if __name__=="__main__":
    main()