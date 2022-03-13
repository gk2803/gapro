import random 

POP_SIZE = 10
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
        self.prob = 0
        self.qprob = 0
        self.x = random.randint(bounds[0][0],bounds[0][1])
        self.y = random.randint(bounds[1][0],bounds[1][1])
        self.z = random.randint(bounds[2][0],bounds[2][1])
        # προσθετει μηδενικα μπροστα απο καθε gene οπου ο αριθμος των δυαδικων με .zfill
        # του ψηφιων ειναι μικροτερος απο τον μεγιστο αριθμο bits εντος του πεδιου ορισμου (7) 
        
        self.genes.append(list(bin(self.x)[2:].zfill(bits)))
        self.genes.append(list(bin(self.y)[2:].zfill(bits)))
        self.genes.append(list(bin(self.z)[2:].zfill(bits)))
        #fitness 
        self.fitness = objective_function(self.get_real_genes())
    

    def get_real_genes(self):
        return [self.x,self.y,self.z]
    
    
    


class Population:
    def __init__(self):
        
        self.pop = []
        self.sum = 0
        self.q = 0
        for _ in range(POP_SIZE):
            s = Chromosome()
            self.sum += s.fitness
            self.pop.append(s)
        #init probabilities, quantitive probabilities
        for elem in self.pop:
            elem.prob = elem.fitness/self.sum
            self.q += elem.prob
            elem.qprob += self.q
        

        
    
    def __str__(self):
        s = ""
        for elem in self.pop:
            s+=f'x: {elem.x}, y: {elem.y}, z: {elem.z} fitness: {elem.fitness} prob: {elem.prob} qprob: {elem.qprob}\n'
        return s
    



class Genetic_Algorithm:
    def __init__(self):
        pass
        

p = Population()
print(p)