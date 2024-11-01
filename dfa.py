def comments(line):  #functia verifica daca o linie din fisier este un comentariu
    return line.startswith('#')

def comment_after_string(line):   #functia returneaza doar informatia necesara, eliminand eventualele comentarii de dupa informatia care ne intereseaza
    if '#' in line:
        position = line.index('#')
        return line[:position].strip()
    return line.strip()

#checker pentru un dfa
def automat(file_name,end):
    with open(file_name, 'r') as file_in:
        lines = file_in.readlines()

    sigma = []   #array pentru elem. din sigma
    states = []   #array pentru elem. din states
    finals = []   #array pentru elem. din finals
    d = {}        #dictionar pentru elem. din delta
    s_start = ''  #starea initiala

    i = 0
    ok = True  # Vom folosi această variabilă pentru a verifica dacă datele sunt corecte

    while i < len(lines):  #parcurg fiecare linie din fisier
        linie = comment_after_string(lines[i])
        if linie == "Sigma":   #adaug in array-ul sigma stringurile din alfabet
            i += 1
            while comment_after_string(lines[i]) != end:
                if len(lines[i].strip()) > 0 and not comments(lines[i]):
                    sigma.extend(comment_after_string(lines[i]).split(','))
                i += 1
        elif linie == "States":  #adaug in array-ul states starile
            i += 1
            while comment_after_string(lines[i]) != end:
                if len(lines[i].strip()) > 0 and not comments(lines[i]):
                    linie = comment_after_string(lines[i])
                    if ',F' in linie:
                        states.append(linie[:-2])  #daca sectiunea finals nu exista, adaug in arry-ul finals starile urmate de caracterul 'F'
                        finals.append(linie[:-2])
                    elif ',S' in linie:
                        states.append(linie[:-2])
                        s_start = linie[:-2]    #starea urmata de caracterul 'S' este starea initiala
                    else:
                        states.append(linie)
                i += 1
        elif linie == "Finals":  #adaug in array-ul finals starile finale
            i += 1
            while comment_after_string(lines[i]) != end:
                if len(lines[i].strip()) > 0 and not comments(lines[i]):
                    finals.extend(comment_after_string(lines[i]).split(','))
                i += 1
        elif linie == "Delta":  #adaug in dictionarul d relatiile din delta, sub forma stareinitiala_tranzitie: starefinala
            i += 1
            while comment_after_string(lines[i]) != end:
                if len(lines[i].strip()) > 0 and not comments(lines[i]):
                    s1, s2, s3 = comment_after_string(lines[i]).split(",") #s1=stare initiala, s2=tranzitie, s3=stare finala
                    a = s1.strip() + "_" + s2.strip()
                    if s1.strip() not in states or s3.strip() not in states or s2.strip() not in sigma: #verific daca cele 2 stari si tranzitia au fost introduse corespunzator in fisier
                        ok = False
                        break
                    d[a] = s3.strip()
                i += 1
        i += 1
    # elimin duplicatele din array-ul finals pentru cazul in care exista o sectiune speciala pentru starile finale iar starile din States sunt urmate de un F
    finals = list(set(finals))

    # verific daca toate array-urile au macar un element, altfel afisez o eroare, caz in care datele din fisier nu au fost introduse bine
    if len(sigma)>0:
        print("Sigma is ", sigma)
    else:
        print("error:sigma is not valid")
    if len(states)>0:
        print("States are ", states)
    else:
        print("error:states are not valid")
    if s_start != '':
        print("The start state is ", s_start)
    else:
        print("error: the start state doesn't exist")
    if len(finals) == 1:
        print("The final state is ", finals)
    elif len(finals) > 1:
        print("The final states are ", finals)
    elif len(finals)==0:
        print("error: final states don't exist")
    if ok:
        print("Delta is ", d)
    else:
        print("error: Delta is not valid")

    return sigma, states, s_start, finals, d


sigma,states,s_start,finals,d=automat("input(lab2).txt", "$")

#aici incepe emulatorul pentru dfa
stare_initiala=s_start #starea initiala
str=input("Introdu stringul:")
str=[x for x in str]  #string-ul introdus este transformat intr-un array ale carui elemente sunt cifrele din Sigma care il formeaza
for arrow in str:  #parcurg string-ul introdus(arrow reprzinta tranzitia)
    for key in d:  #parcurg dictionarul format pentru Delta si verific daca gasesc un element de forma stareinitiala_tranzitie care sa corespunda
        if key==stare_initiala+"_"+arrow:
            stare_initiala=d[key]  #daca gasesc, starea initiala se modifica, astfel starea de la capatul trazitiei devine noua mea stare initiala. continui pana se termina string-ul
            break
if stare_initiala in finals:  #daca, la final, ultima stare memorata in variabila stare_initiala se afla in array-ul finals atunci string-ul meu este acceptat de dfa, altfel nu
    print("dfa-ul accepta stringul")
else:
    print("dfa-ul nu accepta stringul")











