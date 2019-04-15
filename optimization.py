import time
import random
import math

def random_optimize(domain,  fitness_function, n=9999):
    """
    Optimizes overall schedule by creating n random guesses
    :param domain: list of (max,min) tuples
    specifying min and max values for each variable
    :param fitness_function: computes overall cost of a solution
    :return: best solution with the lowest cost
    :param n: max number of iterations
    """
    best = None
    bestr = None
    for iter in range(n):
        # Create a random solution
        r=[random.randint(domain[i][0],domain[i][1])
                      for i in range(len(domain))]
    
        # Get the cost
        cost=fitness_function(r)
    
        # Compare it to the best one so far
        if best is None or cost < best:
            best=cost
            bestr=r

    return r


def hillclimb_optimize(domain,fitness_function):
    # Create an initial random solution
    sol=[random.randint(domain[i][0],domain[i][1])
              for i in range(len(domain))]

    # Main loop
    while 1:
        # Create list of neighboring solutions
        neighbors=[]

        for j in range(len(domain)):
            # One away in each direction
            if sol[j]>domain[j][0]:
                neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])
            if sol[j]<domain[j][1]:
                neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])

        # See what the best solution amongst the neighbors is
        current=fitness_function(sol)
        best=current

        for j in range(len(neighbors)):
            cost=fitness_function(neighbors[j])
            if cost < best:
                best=cost
                sol=neighbors[j]

        # If there's no improvement, then we've reached the local min
        if best==current:
            break

    return sol


def annealing_optimize(domain, fitness_function,
                      T=10000.0,cool=0.95,step=1):
    # Initialize the values randomly
    vec=[random.randint(domain[i][0],domain[i][1])
              for i in range(len(domain))]

    while T > 0.1:
        # Choose one of the indices
        i = random.randint(0,len(domain)-1)

        # Choose a direction to change it
        dir = random.randint(-step,step)

        # Create a new list with one of the values changed
        vecb = vec[:]
        vecb[i] += dir
        if vecb[i] < domain[i][0]:
            vecb[i] = domain[i][0]
        elif vecb[i] > domain[i][1]:
            vecb[i] = domain[i][1]

        # Calculate the current cost and the new cost
        ea = fitness_function(vec)
        eb = fitness_function(vecb)
        p = pow(math.e,(-eb-ea)/T)

        # Is it better, or does it make the probability
        # cutoff?
        if eb < ea or random.random() < p:
            vec = vecb

        # Decrease the temperature
        T = T*cool

    return vec


def genetic_optimize(domain,fitness_function,
                    popsize=100,step=1,
                    mutprob=0.2,elite=0.2,n=100):
    # Mutation Operation
    def mutate(vec):
        i=random.randint(0,len(domain)-1)
        if random.random()<0.5 and vec[i]>domain[i][0]:
            return vec[0:i]+[vec[i]-step]+vec[i+1:]
        elif vec[i]<domain[i][1]:
            return vec[0:i]+[vec[i]+step]+vec[i+1:]
        return vec

    # Crossover Operation
    def crossover(r1,r2):
        i=random.randint(1,len(domain)-2)
        return r1[0:i]+r2[i:]

    # Build the initial population
    pop=[]
    for i in range(popsize):
        vec = [random.randint(domain[i][0], domain[i][1])
               for i in range(len(domain))]
        pop.append(vec)


    # How many winners from each generation?
    topelite=int(elite*popsize)

    # Main loop
    for i in range(n):
        scores = [(fitness_function(sol_vect), sol_vect) for sol_vect in pop]
        scores.sort()

        # See what is current best score
        if scores[0][0] == 0:
            return scores[0][1]

        ranked_solutions = [sol_vect for (cost,sol_vect) in scores]

        # Build next gen population
        # Start with the pure winners
        pop = ranked_solutions[0:topelite]

        # Add mutated and bred forms of the winners
        while len(pop) < popsize:
            if random.random() < mutprob:
                # Mutation
                c = random.randint(0,topelite)
                pop.append(mutate(ranked_solutions[c]))
            else:
                # Crossover
                c1 = random.randint(0, topelite)
                c2 = random.randint(0,topelite)
                pop.append(crossover(ranked_solutions[c1],ranked_solutions[c2]))



    return scores[0][1]
