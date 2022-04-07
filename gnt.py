
import random 

POP_SIZE = 10
#megistos arithmos bits simfwna me to pedio orismou
#
bits = 30
#pedio orismou x,y,z
bounds =[[0,10],[0,20],[0,30]]
Pm = 0.3



def decode( bounds, bits, genes):
        real_chromosome=[]
        for i in range(len(bounds)):
            integer = int(''.join(char for char in genes[i]),2)
            real_value = bounds[i][0] + (integer/(2**bits)) * (bounds[i][1] - bounds[i][0])
            real_chromosome.append(real_value) 
        return real_chromosome

# υπολογισμος fitness (καταλληλοτητας)
def objective_function(t):
    x = t[0]
    y = t[1]
    z = t[2]

    Objective_max = x**2 + y**3 + z**4 +x*y*z 
    return Objective_max



class Chromosome:
    #genes = list of 3 binaries representing real numbers x,y,z

    def __init__(self, genes:list,prob=0,qprob=0):
        self.genes = genes
        self.prob = prob
        self.qprob = qprob
        self.real_genes = decode(bounds, bits, self.genes)
        self.fitness = objective_function(self.real_genes)
    
    #εναλλακτικος constructor για αρχικοποιηση τυχαιου χρωμοσοματος
    @classmethod
    def rand(cls):
        chrome=[]
        for _ in range(len(bounds)):
            var=[]
            for _ in range(bits):
                if random.random()>=0.5:
                    var.append("0")
                else:
                    var.append("1")
            chrome.append(var)
        return cls(chrome)


    def __str__(self):
        s = "" 
        t = self.real_genes
        for gene in self.genes:
            s += f"[{''.join(gene)}]"
        s+= f" x={t[0]}, y={t[1]}, z={t[2]}"
        return s
        
    def get_genes(self):
        return self.genes

# ο πληθυσμος μπορει να αρχικοποιηθει ειτε εισαγοντας μια λιστα απο αντικειμενα Chromosomes
# ειτε τυχαια με τον εναλλακτικο constructor Population.rand()

class Population:
    def __init__(self,pop=[]):
        # pop = λίστα χρωμοσομάτων
        self.pop = pop
        # αθροιζει ολες τις καταλληλοτητες των χρωμοσοματων της λιστας
        self.fitness_sum = 0
        # αθροιζει τις πιθανοτητες του καθε χρωμοσωματος
        self.qprob = 0
        if  self.pop:
            for chromosome in self.pop:
                self.fitness_sum += chromosome.fitness
            for chromosome in self.pop:
                chromosome.prob = chromosome.fitness/self.fitness_sum
                self.qprob += chromosome.prob
                chromosome.qprob += self.qprob
    # αρχικοποιει μια λιστα με τυχαια χρωμοσωματα με μοναδικη εισοδο το μεγεοθος της λιστας
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
            s+=f'{elem.real_genes} fitness: {elem.fitness} prob: {elem.prob} qprob: {elem.qprob}\n'
        return s

# Κλαση που περιεχει τους βασικους τελεστες του γενετικου αλγοριθμου
class GeneticAlgorithm:
    # τελεστης επιλογης. Επιστρεφει ενα αντικειμενο Population με στοιχεια του τα Chromosomes που εχουν επιλεχτει
    # Ο τροπος επιλογης βασιζεται στη μεθοδο εξαναγκασμενης ρουλεττας
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
    # τελεστης διασταυρωσης. Δεχετε ως εισοδο ενα αντικειμενο Population, ενεργει πανω του τη διαδικασια της διασταυρωσης και 
    # επιστρεφει ενα καινουριο αντικειμενο Population.
    # Η διαδικασια της διασταυρωσης βασιζεται στην επιλογη μονου σημειου
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

    # Τελεστης μεταλλαξης. Δεχετε ως εισοδο ενα αντικειμενo Population και μια σταθερα mutation_rate 
    # που εισαγεται απο το χρηστη. 
    # Η διαδικασια της μεταλλαξης γινεται "γυρνωντας" ενα bit της συμβολοσειρας .Εφοσον η συμβολοσειρα
    # επιλεγει για διασταυρωση τότε αλλάζει ΕΝΑ TYXAIO  bit απο ολη τη συμβολοσειρα. 
    # Θα μπορουσε να υλοποιηθει και πιο επιθετικα ως εξης
    # TODO #2 δευτερος τροπος μεταλλαξης
    # Για καθε bit της συμβολοσειρας, επιλεγω ενα τυχαιο αριθμο και αν ειναι μικροτερος η ισος με το mutation_rate τότε το γυρνάω.
    # διαφορετικά παραμένει το ίδιο.
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
                    
pop = Population.rand(100)
run = GeneticAlgorithm()

for i in range(300):
    pop=run.selection(pop)
    pop=run.crossover(pop)
    pop=run.mutation(pop,Pm)

print(pop)



