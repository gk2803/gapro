from pickle import POP
import random 
import time
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
    #genes = list of 3 binaries representing integers x,y,z
    def __init__(self, genes,prob=0,qprob=0):
        self.genes = genes
        self.prob = prob
        self.qprob = qprob
    
    @classmethod
    def rand(cls):
        x = random.randint(bounds[0][0],bounds[0][1])
        y = random.randint(bounds[1][0],bounds[1][1])
        z = random.randint(bounds[2][0],bounds[2][1])
        t = []
        t.append(list(bin(x)[2:].zfill(bits)))
        t.append(list(bin(y)[2:].zfill(bits)))
        t.append(list(bin(z)[2:].zfill(bits)))
        return cls(t)

    def get_int(self):
        t = list()
        for gene in self.genes:
            t.append(int(''.join(gene),2))
        return t
   
    def __str__(self):
        s = "" 
        t = self.get_int()
        for gene in self.genes:
            s += f"[{''.join(gene)}]"
        s+= f" x={t[0]}, y={t[1]}, z={t[2]}"
        return s
        
    def get_genes(self):
        return self.genes

    def set_genes(self,t):
        self.genes = t

 #TODO sdsd
class Population:
    def __init__(self):
        
        self.pop = []
        self.sum = 0
        q = 0
        for _ in range(POP_SIZE):
            s = Chromosome()
            self.sum += s.fitness
            self.pop.append(s)
        #init probabilities, quantitive probabilities
        for elem in self.pop:
            elem.prob = elem.fitness/self.sum
            q += elem.prob
            elem.qprob = q
        
    def get_pop(self):
        return self.pop

    
    #TODO  sadasdadads
    def __str__(self):
        s = ""
        for elem in self.pop:
            s+=f' {elem.get_int()} fitness: {elem.fitness} prob: {elem.prob:.2f} qprob: {elem.qprob:.2f}\n'
        return s
    



#class Genetic_Algorithm:
#    #επιδρα πανω στον υπαρχον πληθυσμο και κραταει μονο 
#    #τα χρωμοσωματα που περνανε το σταδιο της επιλογης
#    @staticmethod
#    def selection(pop: Population):
#        # t λιστα χρωμοσωμάτων
#        t = pop.get_pop()
#        for i in range(POP_SIZE):
#            r = random.random()
#            for index,elem in enumerate(pop.get_pop(),start=0):
#                if r<=elem.qprob:
#                    t[index] = elem
#                    break
#        return t 
#                
#        
#
#    @staticmethod
#    def crossover(pop: Population):
#        pop = pop.get_pop()
#        print(len(pop))
#        for i in range(int(POP_SIZE/2)):
#            p1 = pop[2*i-1].get_genes()
#            
#            p2 = pop[2*i].get_genes()
#            r = random.random()
#            for i in range(bits-1):
#                if (r<=i/(bits-1)):
#                    index = i
#            c1 = [p1[0][:index] +p2[0][index:],p1[1][:index] + p2[1][index:], p1[2][:index] +p2[2][index:]]
#            c2 = [p2[0][:index] +p1[0][index:],p2[1][:index] + p1[1][index:], p2[2][:index] +p1[2][index:]]
#            pop[2*i-1].set_genes(c1)
#            pop[2*i].set_genes(c2)
#        
#
#        
#
#
#pop = Population()
#print(pop)
#g=Genetic_Algorithm()
#print(g.selection(pop))
#
##g.crossover(pop)
##print(pop)