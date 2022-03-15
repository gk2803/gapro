
import random 

POP_SIZE = 10
#megistos arithmos bits simfwna me to pedio orismou 
bits = 5
#pedio orismou x,y,z
bounds =[[0,10],[0,20],[0,30]]
# Pc = 
Pm = 0.3
# k = 

#random.seed(5)
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

    def __init__(self, genes:list,prob=0,qprob=0):
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


class Population:
    def __init__(self,pop=[]):
        #pop is a list of Chromosomes
        self.pop = pop
        self.fitness_sum = 0
        self.qprob = 0
        if  self.pop:
            for chromosome in self.pop:
                #μηδενιζω τις αθροιστικες πιθανοτητες
                
                self.fitness_sum += chromosome.fitness
            for chromosome in self.pop:
                chromosome.prob = chromosome.fitness/self.fitness_sum
                self.qprob += chromosome.prob
                chromosome.qprob += self.qprob
  
    @classmethod
    def rand(cls,size):
        t = []
        for _ in range(size):
            s = Chromosome.rand()
            t.append(s)
        return cls(t)
    
    def __str__(self):
        s = ""
        for elem in self.pop:
            s+=f'{elem.get_int()} fitness: {elem.fitness} prob: {elem.prob} qprob: {elem.qprob}\n'
        return s
    
class GeneticAlgorithm:
    @staticmethod
    def selection(pop:Population):
        p = pop.pop
        t=[]
        for i in range(len(p)):
            r = random.random()
            for chromosome in p:
                if r<= chromosome.qprob:
                    t.append(chromosome)
                    break
        return Population(t)
    
    @staticmethod
    def crossover(pop:Population):
        p = pop.pop
        children = list()
        for i in range(int(len(p)/2)):
            parent1 = p[2*i-1].get_genes()
            parent2 = p[2*i].get_genes()
            #ρουλετα για επιλογη μονου σημειου διασταυρωσης
            r = random.random()
            for i in range(1,bits):  
                if r<i/(bits-1):
                    index = i
                    
                    break
            child1 = [parent1[0][:index] +parent2[0][index:], parent1[1][:index] +parent2[1][index:],parent1[2][:index] +parent2[2][index:] ]
            child2 = [parent2[0][:index] +parent1[0][index:], parent2[1][:index] +parent1[1][index:],parent2[2][:index] +parent1[2][index:] ]
            child1 = Chromosome(child1)
            child2 = Chromosome(child2)
            children.append(child1)
            children.append(child2)
        return Population(children)

    @staticmethod
    def mutation(pop:Population, mutation_rate:float):
        pop = pop.pop.copy()
        offsprings = []
        for chromosome in pop:
            z = chromosome.get_genes()
            if random.random() <= mutation_rate:
                i = random.randint(0,2)
                j = random.randint(0,bits-1)
                c = z
                if c[i][j] == '1':#flip
                    c[i][j] == '0' 
                else:
                    c[i][j] ='1'
                offsprings.append(Chromosome(c))
            else:
                offsprings.append(Chromosome(z))
        return Population(offsprings)
                    
pop = Population.rand(1000)
genetic_algorithm = GeneticAlgorithm()


pop = genetic_algorithm.selection(pop)
pop = genetic_algorithm.crossover(pop)
pop = genetic_algorithm.mutation(pop, Pm)
    
print(len(pop.pop))

for k in pop.pop:
    print(k)