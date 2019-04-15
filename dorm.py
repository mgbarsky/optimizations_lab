from optimization import *


def print_solution(sol, dorms, prefs):
    slots=[]
    # Create two slots for each dorm
    for i in range(len(dorms)):
        slots+=[i,i]

    # Loop over each students assignment
    for i in range(len(sol)):
        x=int(sol[i])

        # Choose the slot from the remaining ones
        dorm=dorms[slots[x]]
        # Show the student and assigned dorm
        print (prefs[i][0],"got:", dorm, " - prefs:", prefs[i][1])

        # Remove this slot
        del slots[x]


def dorm_cost(sol, dorms, prefs):
    cost=0
    # Create list a of slots
    slots=[0,0,1,1,2,2,3,3,4,4]

    # Loop over each student
    for i in range(len(sol)):
        x=int(sol[i])
        dorm=dorms[slots[x]]
        pref=prefs[i][1]

        # First choice costs 0, second choice costs 1
        if pref[0]==dorm: cost+=0
        elif pref[1]==dorm: cost+=1
        else: cost+=3 # Not on the list costs 3


        # Remove selected slot
        del slots[x]
    
    return cost


def main():
    # The dorms, each of which has two available spaces
    dorms=['Dolliver','Crosby','Hill','Carriage','MODs']

    # People, along with their first and second choices
    prefs=[('Daniel', ('Carriage', 'Hill')),
       ('Steven', ('Dolliver', 'MODs')),
       ('Akarsh', ('Crosby', 'Dolliver')),
       ('Kelvin', ('Dolliver', 'MODs')),
       ('Betty', ('Crosby', 'Carriage')),
       ('Jeff', ('Hill', 'MODs')),
       ('Cat', ('MODs', 'Crosby')),
       ('Michael', ('Carriage', 'Hill')),
       ('Gary', ('Carriage', 'Hill')),
       ('James', ('Hill', 'Crosby'))]

    # [(0,9),(0,8),(0,7),(0,6),...,(0,0)]
    domain=[(0,(len(dorms)*2)-i-1) for i in range(0,len(dorms)*2)]
    fitness_function = lambda x: dorm_cost(x, dorms, prefs)

    s = random_optimize(domain, fitness_function, 10000)
    print()
    print("-----------Random optimize----------")
    print(dorm_cost(s, dorms, prefs))

    s = genetic_optimize(domain, fitness_function)
    print()
    print("-----------Genetic optimize----------")
    print(dorm_cost(s, dorms, prefs))
    print_solution(s, dorms, prefs)



if __name__ == "__main__":
    main()