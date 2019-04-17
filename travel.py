from optimization import *


def getminutes(t):
    x = time.strptime(t,'%H:%M')
    return x[3]*60+x[4]


# Displays the resulting schedule found by an algorithm
def print_schedule(r, people, destination, flights):
    for d in range(len(r)//2):
        name = people[d][0]
        origin = people[d][1]
        out = flights[(origin,destination)][int(r[d])]
        ret = flights[(destination,origin)][int(r[d+1])]
        print('%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name, origin,
                                                      out[0], out[1], out[2],
                                                      ret[0], ret[1], ret[2]))


def schedule_cost(sol, people, destination, flights):
    totalprice = 0
    latestarrival = 0
    earliestdep = 24 * 60

    for d in range(len(sol) // 2):
        # Get the inbound and outbound flights
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[d])]
        returnf = flights[(destination, origin)][int(sol[d + 1])]

        # Total price is the price of all outbound and return flights
        totalprice += outbound[2]
        totalprice += returnf[2]

        # Track the latest arrival and earliest departure
        if latestarrival < getminutes(outbound[1]):
            latestarrival = getminutes(outbound[1])
        if earliestdep > getminutes(returnf[0]):
            earliestdep = getminutes(returnf[0])

    # Every person must wait at the airport until the latest person arrives.
    # They also must arrive at the same time and wait for their flights.
    totalwait = 0
    for d in range(len(sol) // 2):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[d])]
        returnf = flights[(destination, origin)][int(sol[d + 1])]
        totalwait += latestarrival - getminutes(outbound[1])
        totalwait += getminutes(returnf[0]) - earliestdep

    # Does this solution require an extra day of car rental? That'll be $50!
    if latestarrival > earliestdep:
        totalprice += 50

    return totalprice + totalwait


def main():
    people = [('Seymour', 'BOS'),
              ('Franny', 'DAL'),
              ('Zooey', 'CAK'),
              ('Walt', 'MIA'),
              ('Buddy', 'ORD'),
              ('Les', 'OMA')]
    # Laguardia
    destination = 'LGA'

    flights = {}
    # Create list of flights for each (origin,destination)
    f = open('schedule.txt')
    for line in f:
        origin, dest, depart, arrive, price = line.strip().split(',')
        flights.setdefault((origin, dest), [])

        # Add details to the list of possible flights
        flights[(origin, dest)].append((depart, arrive, int(price)))

    domain = [(0, 8)] * (len(people) * 2)
    fitness_function = lambda x: schedule_cost(x, people, destination,flights)
    s = random_optimize(domain,  fitness_function, 10000)
    print("\n-----------Random optimize----------")
    print(schedule_cost(s, people, destination, flights))
    print_schedule(s, people, destination, flights)

    s = hillclimb_optimize(domain, fitness_function)
    print("\n-----------Hill climb optimize----------")
    print(schedule_cost(s, people, destination, flights))
    print_schedule(s, people, destination, flights)

    s = annealing_optimize(domain, fitness_function)
    print("\n-----------Simulated annealing optimize----------")
    print(schedule_cost(s, people, destination, flights))
    print_schedule(s, people, destination, flights)

    s = genetic_optimize(domain, fitness_function)
    print("\n-----------Genetic optimize----------")
    print(schedule_cost(s, people, destination, flights))
    print_schedule(s, people, destination, flights)

if __name__ == "__main__":
    main()