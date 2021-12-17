import csv
import math

from BasicFunctions.PolyArea import polyArea

base_reaction = []
displacement = []

# Ottengo la curva Push-pull
with open('Output\Pushover\Pushover_Base_Reactions.out') as csvfile:

    data = csv.reader(csvfile, delimiter=' ')

    for row in data:
        
        sum = 0

        for i in range(1,len(row)):

            sum += float(row[i])
        

        base_reaction.append(-sum)


with open('Output\Pushover\Pushover_Control_Disp.out') as csvfile:

    data = csv.reader(csvfile, delimiter=' ')

    for row in data:
        
        displacement.append(float(row[1]))


# Cerco indici dei punti di inizio dei cicli interi
n = len(displacement)
indexes= []

for i in range(1, n):

    if (abs(displacement[i - 1] - displacement[i]) < 10**-6) and (displacement[i] > 0):

        indexes.append(i)
    
    else:

        continue

# Ultimo indice
indexes.append(n)

# Separo i cicli
cycles = []

for i in range(len(indexes) - 1):

    # Verifico se la curva che prendo in considerazione è ciclica
    if (abs(displacement[indexes[i]] - displacement[indexes[i + 1] - 1]) < 10**-6):

        cycle_displacements = displacement[indexes[i]:indexes[i + 1]]
        cycle_reactions = base_reaction[indexes[i]:indexes[i + 1]]

        cycles.append([cycle_displacements,cycle_reactions])
       
    else:

        continue
    

# Calcolo le aree
damping_points = []

for cycle in cycles:

    max_point = [cycle[0].pop(0), cycle[1].pop(0)]

    hysteretic_area = polyArea(poly = cycle)

    elastic_area = max_point[0] * max_point[1] * 0.5
    
    equivalent_damping = hysteretic_area / ( 4 * math.pi * elastic_area)

    damping_points.append([max_point[0], equivalent_damping])

print(damping_points)

