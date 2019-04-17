import random
import math
print_steps = False

def randomoptimize(population, fitness_function):
    best_fitness = None
    best_solution = None
    for i in range(len(population)):
        # Get the cost
        fitness = fitness_function(population[i])

        # Compare it to the best one so far
        if best_fitness == None or fitness < best_fitness:
            best_fitness = fitness
            best_solution = population[i]
    return (best_fitness, best_solution, len(population))


def hillclimb_optimize(rand_sol, fitness_function):
    sol = rand_sol
    current_score = fitness_function(sol)
    iterations = 0
    # Main loop
    while 1:
        iterations += 1
        # Create list of neighboring solutions
        neighbors = []

        for j in range(len(sol)):
            # One away in each direction
            neighbors.append(sol[0:j] + min('z',chr(ord(sol[j]) + 1)) + sol[j + 1:])
            neighbors.append(sol[0:j] + max('A',chr(ord(sol[j]) - 1)) + sol[j + 1:])

        # See what the best solution amongst the neighbors is
        current_score = fitness_function(sol)
        best = current_score
        for j in range(len(neighbors)):
            cost = fitness_function(neighbors[j])
            if cost < best:
                best = cost
                sol = neighbors[j]

        # If there's no improvement, then we've reached the bottom
        if best == current_score:
            break
    return (current_score, sol, iterations)


def annealing_optimize(rand_sol, fitness_function, T=10000.0, cool=0.95, step=1):
    # Initialize the values randomly
    vec = rand_sol
    iterations = 0
    while T > 0.1:
        iterations += 1
        # Choose one of the indices
        i = random.randint(0, len(vec) - 1)

        # Choose a direction to change it
        dir = random.randint(-step, step)

        # Create a new solution with one of the values changed
        vecb = vec[:i] + chr(ord(vec[i])+dir) + vec[i+1:]

        # Calculate the current cost and the new cost
        ea = fitness_function(vec)
        eb = fitness_function(vecb)
        p = pow(math.e, (-eb - ea) / T)

        # Is it better, or does it make the probability
        # cutoff?
        if (eb < ea or random.random() < p):
            vec = vecb

            # Decrease the temperature
        T = T * cool
    return (fitness_function(vec),vec,iterations)


def genetic_optimize(population, fitness_function,
                     mutation_function, mate_function,
                     mutation_probability, elite,
                     maxiterations, params=None):

    # How many winners from each generation?
    original_population_size = len(population)
    top_elite = int(elite * original_population_size)

    # Main loop
    iterations = 0
    for i in range(maxiterations):
        iterations += 1
        individual_scores = [(fitness_function(v), v) for v in population]
        individual_scores.sort()
        ranked_individuals = [v for (s, v) in individual_scores]

        # Start with the pure winners
        population = ranked_individuals[0:top_elite]

        # Add mutated and bred forms of the winners
        while len(population) < original_population_size:
            if random.random() < mutation_probability:
                # Mutation
                c = random.randint(0, top_elite)
                population.append(mutation_function(ranked_individuals[c], params))
            else:
                # Crossover
                c1 = random.randint(0, top_elite)
                c2 = random.randint(0, top_elite)
                population.append(mate_function(ranked_individuals[c1], ranked_individuals[c2], params))

        # Print current best score
        if print_steps:
            print(
            'best fitness score in iteration %d is %d ' % (i, individual_scores[0][0]))
            print (
            ' for individual %r ' % (individual_scores[0][1]))

        if individual_scores[0][0] == 0:
            return (individual_scores[0][0],individual_scores[0][1], iterations)

    # returns the best solution
    return (individual_scores[0][0],individual_scores[0][1],iterations)
