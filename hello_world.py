from string_optimization import *

def create_random_string(target_length):
    individual_str = ''
    for j in range(0, target_length):
        individual_str += chr(random.randint(32, 90))
    return individual_str


# build initial population of many random strings of target length
def init_strings_population(population_size, target_length):
    population=[]
    for i in range(0,population_size):
        individual_str = create_random_string(target_length)
        population.append(individual_str)
    return population


# Mutation Operation
def mutate_string(individual,params=None):
    ipos = random.randint(0, len(individual) - 1)

    # mutation changes character at random position
    # to any valid character from 32 (space) to 90 (Z)
    rchar = chr(random.randint(0, 32000) % 90 + 32)

    individual = individual[0:ipos] + rchar + individual[(ipos + 1):]
    return individual


# Mate operation (crossover)
def string_crossover(p1,p2,params=None):
    ipos = random.randint(1,len(p1)-2)
    return p1[0:ipos]+p2[ipos:]


def main():
    TARGET_STRING = 'Hello world'
    target_length = len(TARGET_STRING)
    # fitness function - hamming distance
    fitness_function = lambda x: sum([abs(ord(x[i])- ord(TARGET_STRING[i]))
                            for i in range(target_length)])

    string_population = init_strings_population(204800, target_length)
    best_score, best_sol, iterations = randomoptimize(string_population, fitness_function)
    print("performed",iterations,"iterations",
    "best random solution:",best_sol," with score", best_score)

    print()
    print("*************Hill climbing****************")
    rand_solution = create_random_string(target_length)
    best_score, best_sol, iterations = hillclimb_optimize(rand_solution, fitness_function)
    print("performed",iterations,"iterations",
        "best hill climb solution:", best_sol, " with score", best_score)

    print()
    print("*************Simulated annealing****************")
    rand_solution = create_random_string(target_length)
    best_score, best_sol, iterations = annealing_optimize(rand_solution, fitness_function,
                                              T=204800.0,cool=0.999)
    print("performed",iterations,"iterations",
        "best annealing solution:", best_sol, " with score", best_score)

    print()
    print(
    "*****************GENETIC ALGORITHM ***************")
    string_population = init_strings_population(2048, target_length)
    best_score, best_sol, iterations  = genetic_optimize(string_population, fitness_function,
                                    mutate_string, string_crossover,
                                    mutation_probability=0.25, elite=0.1,
                                    maxiterations=100)
    print("performed",iterations,"iterations",
        "best GENETIC ALGORITHM solution: ", best_sol, " with score", best_score)


if __name__ == "__main__":
    main()