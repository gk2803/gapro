
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
    #genes = list of 3 binaries representing integers x,y,z

    def __init__(self, genes,prob=0,qprob=0):
        self.genes = genes
        self.prob = prob
        self.qprob = qprob
        self.fitness = objective_function(self.get_int())

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

c = Chromosome.rand()
c = Chromosome([['1','0','0','1','0'],['1','0','0','1','0'],['1','0','0','1','0']])
print(c.fitness)