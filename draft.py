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
N = 30
bits = 5

#προβλημα
def objective_function(x):
    return x**2


#αρχικοποίηση λίστας με τυχαίους αριθμούς
a = []
for i in range(N):
     a.append(random.randint(1,31))
     

#αξιολογηση (υπολογισμός τιμών μέσω της συνάρτησης) (fitness)
#ο πινακας t περιεχει τις "λυσεις" των αρχικοποιημενων τυχαίων αριθμων
t=[]
for i in range(N):
    t.append(objective_function(a[i]))

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


#list of tuples (value,fitness,prob,qi)
pop =[]
for i in range(N):
    pop.append((a[i],t[i],f[i],q[i]))
    print(pop[i])
#επιλογη ρουλετας - διασταύρωση



for i in range(N):
    r = random.random()
    for j in range(N):
        
        if (r<=q[j]):
            #κωδικας διασταύρωσης
            break




    
#διασταυρωση μονου σημειου (one point crossover)
#συναρτηση που θα χρησιμοποιηθει ΚΑΤΑ τη διαδικασια της επιλογης
def crossover(parent1, parent2):
    
    # ρουλέτα για επιλογή σημείου bits -1 καθως τα σημεια στα οποια 
    # μπορει να χωριστει το binary ειναι bits-1 
    # σσ. bits = ο αριθμος των ψηφιων της δυαδικης συμβολοσειρας π.χ. ο αριθμος 31 σε binary ειναι 11111
    
    r = random.random()
    for i in range(bits-1):
        if (r<=i/(bits-1)):
            index = i
            break
    child1 = parent1[:index]+parent2[index:]
    child2 = parent2[:index]+parent1[index:]
    print("το σημείο τομής είναι",index)
    return child1,child2
    

print(crossover("01234","99912"))
    
