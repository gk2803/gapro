import random
from re import A

random.seed(10)

#TODO recursive
def n_elements_sum(l,n):
    sum = 0
    if (n==0):
        return l[0]
    for i in range(n+1):
        sum += l[i]
            
    return sum

#κατασκευη πιθανων λυσεων 

#Ν αριθμος πιθανων λυσεων
N = 6
bits = 5

#προβλημα
def foo(x):
    return x**2


#αρχικοποίηση λίστας με τυχαίους αριθμούς
a = []
for i in range(N):
     a.append(random.randint(1,31))


#αξιολογηση (υπολογισμός τιμών μέσω της συνάρτησης) (fitness)
#ο πινακας t περιεχει τις "λυσεις" των αρχικοποιημενων τυχαίων αριθμων
t=[]
for i in range(N):
    t.append(foo(a[i]))

# τα στοιχεία του πίνακα f αποτελούν την πιθανότητα επιλογής των στοιχείων του πίνακα t
# η πιθανότητα κάθε χρωμοσώματος υπολογίζεται διαιρώντας την αξιολόγηση (fitness) με τον συνολικό
# αριθμό αξιολογήσεων s = sum(t)
f=[]
s= sum(t)
for i  in range(N):
    f.append(t[i]/s)

# average = s/N τα average και max δεν χρειάζονται αλλά αποτελούν ένα ένδιαφέρον στατιστικό
# max = max(t)

# βήμα αθροιστικής πιθανότητας όπου θα μας βοηθήσει
# στην αναπαράσταση των πιθανοτήτων σε μια ρουλέτα
# υπολογισμος αθροιστικης πιθανότητα: 
# q[0] = f[0]
# q[1] = f[0] + f[1]
# q[2] = f[0] + f[1] + f[2] κ.ο.κ
# όπου f[i] η πιθανότητα του χρωμοσώματος i
q=[]
for i in range(N):
    q.append(n_elements_sum(f,i))

#επιλογη ρουλετας - διασταύρωση
select = [0 for _ in range(N)]

for i in range(N):
    r = random.random()
    for j in range(N):
        if (r<=q[j]):
            select[j]+=1
            break



last_list=[]
for i in range(N):
    last_list.append((a[i],f[i],select[i]))
    
#διασταυρωση μονου σημειου (one point crossover)
#συναρτηση που θα χρησιμοποιηθει ΚΑΤΑ τη διαδικασια της επιλογης
def crossover(parent1, parent2):
    
    # ρουλέτα για επιλογή σημείου bits -1 καθως τα σημεια στα οποια 
    # μπορει να χωριστει το binary ειναι bits-1 
    # σσ. bits = ο αριθμος των ψηφιων της δυαδικης συμβολοσειρας π.χ. ο αριθμος 31 σε binary ειναι 11111
    
    r = random.random()
    for i in range(bits-1):
        if (r<=i/(bits-1)):
            position = i
            break
    child1 = parent1[:position]+parent2[position:]
    child2 = parent2[:position]+parent1[position:]
    print("το σημείο τομής είναι",position)
    return child1,child2
    

print(crossover("01234","99912"))
    




#last_list.sort(key=lambda y: y[2])

for i in range(N):
    print(f"chromosome: {last_list[i][0]}, probability: {last_list[i][1]:.2f}, roulette-selection: {last_list[i][2]}")
