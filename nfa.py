def comments(line):  #functia verifica daca o linie din fisier este un comentariu
    return line.startswith('#')

def comment_after_string(line):   #functia returneaza doar informatia necesara, eliminand eventualele comentarii de dupa informatia care ne intereseaza
    if '#' in line:
        position = line.index('#')
        return line[:position].strip()
    return line.strip()

#aici incepe checker-ul pentru nfa
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
            # adaug in sigma E, in acest caz reprezentand epsilon
            sigma.append("E")
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
                    if s1.strip() not in states or s3.strip() not in states or s2.strip() not in sigma:#verific daca cele 2 stari si tranztitia au fost introduse corespunzator
                        ok = False
                        break
                    if a not in d:
                        d[a]=[]
                        d[a].append(s3.strip())
                    else:
                        d[a].append(s3.strip())

                i += 1
        i += 1

    # elimin duplicatele din array-ul finals pentru cazul in care exista o sectiune speciala pentru starile finale iar starile din States sunt urmate de un F
    finals = list(set(finals))


    # verific daca toate array-urile au macar un element, altfel afisez o eroare, caz in care datele din fisier nu au fost introduse bine
    print("Sigma is " ,sigma)
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


sigma,states,s_start,finals,d=automat("input(lab3).txt", "$")

#aici incepe emulatorul pentru nfa
#citesc stringul de la tastatura si verific sa fie introdus corect, mai exact verific sa fie format doar din caractere din Sigma
ok=0
while ok==0:
    ok2=0
    str = [x for x in input("Introdu un string: ")] #string-ul introdus este transformat intr-un array
    for x in str:
        if x not in sigma:
            print("string invalid")
            ok2=1
            break
    if(ok2==0):
        ok=1

#prima stare in care ma aflu este chiar starea initiala
#pot exista mai multe cazuri pentru starea curenta, de aceea voi folosi un array care le va memora, pentru a putea trata fiecare caz in parte
#vizualizez nfa-ul ca pe un arbore, asa cum apare si in curs, iar in stare_curenta introduc starile de pe fiecare nivel al arborelui
stare_curenta=[s_start]
for arrow in str: #parcurg string-ul(arrow este tranzitia)
    stare_urmatoare=[] #in acest array voi introduce toate starile in care am posibilitatea de a urma o tranzitie din fiecare stare din stare_curenta
    for q in stare_curenta:
        for key in d: #parcurg dictionarul format pentru Delta si verific daca gasesc un element de forma stareinitiala_tranzitie care sa corespunda
            if key==q+"_"+arrow:
                stare_urmatoare.append(d[key]) #adaug noile stari in stare_urmatoare

    #actualizez array-ul stare_curenta cu starile noi introduse in stare_urmatoare si reiau algoritmul pentru noile mele stari curente
    stare_curenta=[stare_urmatoare[i][j] for i in range(len(stare_urmatoare)) for j in  range(len(stare_urmatoare[i]))]

#parcurg array-ul final cu stari si verific daca vreuna din stari se afla in array-ul finals(de stari finale)
ok=0
for stare in stare_curenta:
    if stare in finals:
        ok=1

#tratez cazurile in care apare tranzitia epsilon
stare_curenta=[s_start]
index=0
while index<len(str):
    stare_urmatoare=[]
    for q in stare_curenta:
        if q+"_"+"E" in d: #in acest caz, prioritate o sa aiba tranzitiile epsilon. daca gasesc o astfel de tranzitie, trec direct in starea urmatoare
            stare_urmatoare.append(d[q+"_"+"E"])
        elif q+"_"+str[index] in d: #daca nu gasesc un epsilon, atunci practic repet procedeul de mai sus si parcurg string-ul introdus
            stare_urmatoare.append(d[q+"_"+str[index]])
            index+=1

    stare_curenta = [stare_urmatoare[i][j] for i in range(len(stare_urmatoare)) for j in range(len(stare_urmatoare[i]))]

#parcurg array-ul final cu stari pentru noul caz si verific daca vreuna din stari se afla in array-ul finals(de stari finale)
ok2=0
for stare in stare_curenta:
    if stare in finals:
        ok2=1

#daca in macar un caz s-a modificat variabila mea ok/ok2 inseamna nfa-ul accepta string-ul introdus, altfel nu
if ok==1 or ok2==1:
    print("NFA-ul accepta stringul")
else:
    print("NFA-ul nu accepta stringul")




