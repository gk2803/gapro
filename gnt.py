from operator import attrgetter
import random
import numpy.random as npr 


class Chromosome:
    def __init__(
        self, genes: list, bounds: list, objective_function: callable, bits: int 
    ):
        self.bounds = bounds
        self.genes = genes
        self.bits = bits 
        self.real_genes = self.decode(self.genes)
        self.fitness = objective_function(*self.real_genes)
        self.scaled_fitness = self.fitness 
        
    @classmethod
    def rand(cls, bounds,objective_function,bits):
        '''
        alternative constructor ->random chromosome
        '''
        genes = [[str(random.randint(0,1)) for i in range(bits)] for _ in range(len(bounds))]
        return cls(genes,bounds,objective_function,bits)

    def decode(self, genes):
        '''
         list of binaries -> list of real numbers
         '''
        real_chromosome = []
        for i in range(len(self.bounds)):
            integer = int("".join(char for char in genes[i]), 2)
            real_value = self.bounds[i][0] + (
                integer / (2 ** self.bits)
            ) * (  
                self.bounds[i][1] - self.bounds[i][0]
            )
            real_chromosome.append(real_value)
        return real_chromosome
      

class GeneticAlgorithm:
    def __init__(self, size:int, bits:int, bounds:list, pm:float, pc:float, cp:int, objective_function:callable,):
        self.objective_function = objective_function
        self.size = size
        self.bits = bits
        self.bounds = bounds
        self.pm = pm
        self.pc = pc
        self.cp = cp
        self.population = [Chromosome.rand(self.bounds,objective_function,self.bits) for _ in range(size)]
            
        

    # calculates fitness scores/qprob
    def misc(self):
        '''
        prepares class for selection
        '''
        self.fitness_sum = sum([chrome.fitness for chrome in self.population])
        self.fitness_average = self.fitness_sum / len(self.population)
        
  
    def roulette_selection(self):
        '''
        Fitness proportionate selection
        '''
        #scale if negative value
        self.flag = any(c.fitness<=0 for c in self.population)
        if self.flag:
            min_fitness = min(self.population, key=attrgetter("fitness")).fitness
            
            for chrome in self.population:
                chrome.scaled_fitness -= (min_fitness -10) #fitness can't be zero
            self.scaled_sum = sum([chrome.scaled_fitness for chrome in self.population])
            
        t = []
        selection_probs = [c.fitness/self.fitness_sum for c in self.population] if not self.flag else [c.scaled_fitness/self.scaled_sum for c in self.population]
        for _ in range(self.size):
            t.extend(random.choices(self.population,weights=selection_probs))
        self.population = t 
        self.flag = False




    def tournament_selection(self):
        '''
        tournament based selection
        '''
        self.population =  [max(random.sample(self.population,2), key=attrgetter("fitness")) for _ in range(self.size)]

    def crossover(self):

        pop = self.population
        newpop = list()
        for i in range(int(len(pop) / 2)):
            parent1 = pop[2 * i - 1].genes
            parent2 = pop[2 * i].genes
            if random.random() <= self.pc:
                child1, child2 = self.multiple_crossover(
                    parent1, parent2, self.cp
                )
                newpop.extend(
                    [
                        Chromosome(
                            child1, self.bounds, self.objective_function,self.bits
                        ),
                        Chromosome(
                            child2, self.bounds, self.objective_function,self.bits
                        ),
                    ]
                )

            else:
                newpop.extend([pop[2 * i - 1], pop[2 * i]])

        self.population = newpop

    def mutation(self):
        pop = self.population
        offsprings = []
        for chromosome in pop:
            z = chromosome.genes
            if random.random() <= self.pm:
                dummy = []
                for i in range(len(self.bounds)):
                    j = random.randint(0, self.bits - 1)
                    if z[i][j] == "1":  # flip
                        z[i][j] = "0"
                    else:
                        z[i][j] = "1"
                    dummy.append(z[i])
                offsprings.append(
                    Chromosome(dummy, self.bounds, self.objective_function,self.bits)
                )
            else:
                offsprings.append(
                    Chromosome(z, self.bounds, self.objective_function,self.bits)
                )
        self.population = offsprings
    

    def best(self):
        return max(self.population, key=attrgetter("fitness"))
    
    
    @staticmethod
    def multiple_crossover(parent1, parent2, cp):
        bits = len(parent1[0])
        if cp == 1:
            index = random.randint(1, bits - 1)
            child1 = [
                parent1[i][:index] + parent2[i][index:]
                for i in range(len(parent1))
            ]
            child2 = [
                parent2[i][:index] + parent1[i][index:]
                for i in range(len(parent1))
            ]
            return child1, child2

        cp = random.sample(range(1, bits), cp)
        cp.sort()
        child1 = [[None] * bits for _ in range(len(parent1))]
        child2 = [[None] * bits for _ in range(len(parent1))]
        for j in range(len(parent1)):
            sum = 0
            flag = False
            for i in range(bits):

                if sum < len(cp) and i == cp[sum]:
                    flag = not flag
                    sum += 1

                if flag == True:
                    child1[j][i] = parent1[j][i]
                    child2[j][i] = parent2[j][i]
                else:
                    child1[j][i] = parent2[j][i]
                    child2[j][i] = parent1[j][i]
        return child1, child2

    def run(self,val):
        self.misc()
        self.tournament_selection() if val == 1 else self.roulette_selection()
        self.crossover()
        self.mutation()


