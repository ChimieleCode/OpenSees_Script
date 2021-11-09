import csv

import matplotlib.pyplot as plt

base_reaction = []
displacement = []

with open('Output\Pushover\Pushover_Base_Reactions.out') as csvfile:

    data = csv.reader(csvfile, delimiter=' ')

    for row in data:
        
        sum = 0

        for i in range(1,len(row)):

            sum += float(row[i])
        

        base_reaction.append(-sum)


with open('Output\Pushover\Pushover_Storey_Drift.out') as csvfile:

    data = csv.reader(csvfile, delimiter=' ')

    for row in data:
        
        displacement.append(float(row[1]))



# Opensees
plt.plot(
    displacement,
    base_reaction,
    label = 'OpenSees',
    color = 'r',
    linestyle = '-',
    linewidth = 1
    )

# Titoli Assi
plt.ylabel('Base Reaction [kN]')
plt.xlabel('Displacement [m]')

# Unità assi

# Titolo Grafico
plt.title('Control Node')

# Mostra Legenda e Griglia
plt.legend()

plt.grid(
    True, 
    linestyle = '--'
    )

# Save
plt.savefig(f'Figures\PushPull.png')

# Display
# plt.show()

plt.clf()
