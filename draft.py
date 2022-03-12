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
N = 10
bits = 6

#προβλημα
def foo(x):
    return x**2

#αρχικοποίηση λίστας με τυχαίους αριθμούς
a = []
for i in range(N):
     a.append(random.randint(1,31))


#αξιολογηση
t=[]
for i in range(N):
    t.append(foo(a[i]))

 
f=[]
#αθροισμα αξιολογησεων και εκχωρηση στην μεταβλητη s
s= sum(t)
#πιθανοτητα επιλογης του κανε χρωμοσωματος(λυσης)
for i  in range(N):
    f.append(t[i]/s)

average = s/N
max = max(t)
#υπολογισμος αθροιστικης ικανοτητας
q=[]
for i in range(N):
    q.append(n_elements_sum(f,i))

#επιλογη ρουλετας 
select = [0 for _ in range(N)]

for i in range(N):
    r = random.random()
    for j in range(N):
        if (r<=q[j]):
            select[j]+=1
            break

#διασταυρωση μονου σημειου
#χωριζουμε τον πληθυσμο σε ζευγη με βαση τη σειρα επιλογης
#

last_list=[]
for i in range(N):
    last_list.append((a[i],f[i],select[i]))
    

#last_list.sort(key=lambda y: y[2])

for i in range(N):
    print(last_list[i])
