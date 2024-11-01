def comments(line):  #functia verifica daca o linie din fisier este un comentariu
    return line.startswith('#')

def comment_after_string(line):   #functia returneaza doar informatia necesara, eliminand eventualele comentarii de dupa informatia care ne intereseaza
    if '#' in line:
        position = line.index('#')
        return line[:position].strip()
    return line.strip()

def automat(file_name,end):
    with open(file_name, 'r') as file_in:
        lines = file_in.readlines()

    variables = []   #array pentru variabile
    terminals = []   #array pentru elem. terminale
    rules = {}        #dictionar pentru reguli


    i = 0
    ok = True  # Vom folosi această variabilă pentru a verifica dacă datele sunt corecte

    while i < len(lines):  #parcurg fiecare linie din fisier
        linie = comment_after_string(lines[i])
        if linie == "Variables":   #adaug in array-ul sigma stringurile din alfabet
            i += 1
            while comment_after_string(lines[i]) != end:
                if len(lines[i].strip()) > 0 and not comments(lines[i]):
                    variables.extend(comment_after_string(lines[i]).split(','))
                i += 1
        elif linie == "Terminals":  #adaug in array-ul states starile
            i += 1
            while comment_after_string(lines[i]) != end:
                if len(lines[i].strip()) > 0 and not comments(lines[i]):
                    linie = comment_after_string(lines[i])
                    terminals.append(linie)
                i += 1

        elif linie == "Rules": #adaug in dcitionarul rules regulile pentru fiecare variabila
            i += 1
            while comment_after_string(lines[i]) != end:
                if len(lines[i].strip()) > 0 and not comments(lines[i]):
                    if "|" not in lines[i]:  #cazul in care regulile pentru o singura variabila sunt pe linii diferite
                        s1, s2 = comment_after_string(lines[i]).split(",")  #s1=partea stanga a regulii, s2=partea dreapta a regulii
                        if s1 not in rules:
                            rules[s1]=[]
                            rules[s1].append(s2)
                        else:
                            rules[s1].append(s2)
                    else:
                        #cazul in care regulile pentru o variabila sunt despartitie prin "|", pe un singur rand
                        s1, s2 = comment_after_string(lines[i]).split(",")  #s1=partea stanga a regulii, s2=partea dreapta a regulii

                        a=0
                        for j in range(len(s2)):
                            if s2[j]=="|":
                                if s1 not in rules:
                                    rules[s1] = []
                                    rules[s1].append(s2[a:j])
                                    a=j+1
                                else:
                                    rules[s1].append(s2[a:j])
                                    a=j+1
                        rules[s1].append(s2[a:])
                #verific daca regulile sunt bine definite
                ok=0
                for caracter in comment_after_string(lines[i]):
                    if caracter!="|" and caracter!=",":
                        if caracter not in variables and caracter not in terminals:
                            ok=1
                if ok==1:
                    rules["eroare"]=[] #daca intalnesc cheia "eroare" in dictionar atunci este o problema cu datele din fisier
                    break
                i += 1
        i += 1

    return variables,terminals,rules

variables,terminals,rules=automat('input2(lab4).txt', 'end')

#memorez valoarea variabilei de start
if len(rules)>0:
    for key in rules:
        starting_symbol=key
        break

count=0 #verific daca toate array-urile/dictionarele sunt ok, daca se afiseaza vreo eroara atunci count devine 1 si nu mai pot continua cu emulatorul pentru cfg
if len(variables)>0:
    print("Multimea de variabile este ",variables)
else:
    print("Eroare: variabilele nu au fost introduse in fisier")
    count=1

if len(terminals)>0:
    print("Multimea de terminale este ",terminals)
else:
    print("Eroare: multimea de terminale nu a fost introdusa in fisier")
    count=1

if "eroare" in rules:
    print("Eroare: regulile nu au fost bine definite")
    count=1
else:
    print("Dictionarul cu reguli este ",rules)

print("Variabila de start este ",starting_symbol)


#aici incepe emulatorul pentru cfg
#emulatorul este gandit pe baza exemplelor de la curs
#nu genereaza automat toate string-urile posibile deoarece ar fi o infinitate, ci ii permite utilizatorul sa isi construiasca singur string-ul
if count==0:
    start=input("Doresti sa incepi gramatica?(da/nu)")
    ok=0
    gramatica=""
    gramatica+=starting_symbol #initial, string-ul meu este format doar din variabila de start

    if start=="da":
        while ok==0: #algoritmul continua cat timp in "gramatica" am macar o variabila din array-ul variables
            #sunt afisate pe ecran,pe rand, regulile pentru fiecare variabila din regula iar variabile este aleasa introducand indexul ei din array-ul afisat(se incepe cu 0)
            print("Regulile pentru variabila ",starting_symbol," sunt: ",rules[starting_symbol])
            symbol=int(input("Alege indexul unei reguli cu care sa continui: "))
            #daca indexul nu este bine introdus, nu esti lasat sa continui constructia string-ului pana cand nu introduci un index valid
            while symbol>=len(rules[starting_symbol]):
                print("introducere invalida")
                symbol = int(input("Alege indexul unei reguli cu care sa continui: "))
            print("Ati selectat regula ",starting_symbol,"->",rules[starting_symbol][symbol])#pentru mai multa claritate, este afisata regula aleasa

            gramatica=gramatica.replace(starting_symbol,rules[starting_symbol][symbol],1) #inlocuiesc, in string-ul obtinut pana in momentul respectiv, variabila cu o regula de a sa
            print("Rezultatul este ",gramatica) #pentru claritate, afisez rezultatul obtinut la fiecare pas

            nr_caractere=0
            for caracter in gramatica:
                if caracter in variables:
                    starting_symbol=caracter #variabila de start este actualizata
                    nr_caractere+=1

            if nr_caractere==0:
                ok=1  #"ok" devine 1 in momentul in care nu mai am variabile in string, ci doar terminale. in acel moment programul se incheie





