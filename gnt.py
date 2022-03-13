import random 

POP_SIZE = 100
#megistos arithmos bits simfwna me to pedio orismou 
bits = 5
#pedio orismou x,y,z
bounds =[[0,10],[0,20],[0,30]]
# Pc = 
# Pm =
# k = 


def decode(bin):
    pass

def objective_function(t):
    x = t[0]
    y = t[1]
    z = t[2]

    Objective_max = x**2 + y**3 + z**4 +x*y*z 
    return Objective_max


class Chromosome:
    def __init__(self):
        #lista triwn stoixeiwn [x,y,z]
        self.genes = []
        self.fitness = 0
        x = random.randint(bounds[0][0],bounds[0][1])
        y = random.randint(bounds[1][0],bounds[1][1])
        z = random.randint(bounds[2][0],bounds[2][1])
        # προσθετει μηδενικα μπροστα απο καθε gene οπου ο αριθμος των δυαδικων με .zfill
        # του ψηφιων ειναι μικροτερος απο τον μεγιστο αριθμο bits εντος του πεδιου ορισμου (7) 
        
        self.genes.append(list(bin(x)[2:].zfill(bits)))
        self.genes.append(list(bin(y)[2:].zfill(bits)))
        self.genes.append(list(bin(z)[2:].zfill(bits)))

        

    
    def genes(self):
        return self.genes

    def decode(self):
        pass 

     
s = Chromosome()
print(s.genes)