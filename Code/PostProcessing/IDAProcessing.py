import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

directory = 'Output\IDA\Curves'

# Ottengo le informazioni
curves = []

for j, filename in enumerate(os.listdir(directory)):

    with open(f'{directory}/{filename}') as csvfile:

        data = csv.reader(csvfile)

        curve = []

        for i, row in enumerate(data):

            if i == 0:

                continue

            else:

                curve.append({
                    'IM' : float(row[0]), 
                    'DCR' : float(row[1])
                    })

        curves.append(curve)
        

# Calcolo le intersezioni
DS1_points = []

for curve in curves:

    point = (1 - curve[-2]['DCR']) * (curve[-1]['IM'] - curve[-2]['IM']) / (curve[-1]['DCR'] - curve[-2]['DCR']) + curve[-2]['IM']

    DS1_points.append(point)


DS1_points.sort()

num_points = len(DS1_points)

DS1_fragility = {}

DS1_fragility['theta'] = np.exp(1 / num_points * sum([np.log(a) for a in DS1_points]))
DS1_fragility['beta'] = (1 / (num_points - 1) * sum([np.log(a / DS1_fragility['theta'])**2 for a in DS1_points]))**0.5
DS1_fragility['IM'] = np.linspace(0.01, 5, 500)
DS1_fragility['P'] = norm.cdf(np.log(DS1_fragility['IM'] / DS1_fragility['theta']) / DS1_fragility['beta'])
DS1_fragility['upper'] = norm.cdf((np.log(DS1_fragility['IM'] / DS1_fragility['theta']) + DS1_fragility['beta']) / DS1_fragility['beta'])
DS1_fragility['lower'] = norm.cdf((np.log(DS1_fragility['IM'] / DS1_fragility['theta']) - DS1_fragility['beta']) / DS1_fragility['beta'])

# Scrivo la curva a step
with open(f'Output\IDA\Fragility\DS1_fragility_step.csv', 'w', newline = '') as csvfile:

    writer = csv.writer(csvfile)

    DS1_fragility['IMstep'] = []
    DS1_fragility['Pstep']  = []

    for i, point in enumerate(DS1_points):

        writer.writerow([point, i / num_points])
        writer.writerow([point, (i + 1) / num_points])

        DS1_fragility['IMstep'].append(point)
        DS1_fragility['IMstep'].append(point)

        DS1_fragility['Pstep'].append(i / num_points)
        DS1_fragility['Pstep'].append((i + 1) / num_points)

# Stampo la curva
plt.plot(
    DS1_fragility['IMstep'],
    DS1_fragility['Pstep'],
    label = 'Step Curve',
    color = 'r',
    linestyle = '-',
    linewidth = 1
    )

plt.plot(
    DS1_fragility['IM'],
    DS1_fragility['P'],
    label = 'Fragility',
    color = 'k',
    linestyle = '-',
    linewidth = 1
    )

plt.plot(
    DS1_fragility['IM'],
    DS1_fragility['upper'],
    label = 'Upper',
    color = '0.5',
    linestyle = '--',
    linewidth = 1
    )

plt.plot(
    DS1_fragility['IM'],
    DS1_fragility['lower'],
    label = 'Lower',
    color = '0.5',
    linestyle = '--',
    linewidth = 1
    )


# Titoli Assi
plt.ylabel('P(DCR > 1|Sa)')
plt.xlabel('Sa(T1) [g]')

# Titolo Grafico
plt.title('Fragility DS1 IDA')

# Opzioni
plt.xlim(left = 0, right = 1)
plt.ylim(bottom = 0, top = 1)

# Mostra Legenda e Griglia
plt.legend()

plt.grid(
    True, 
    linestyle = '--'
    )

# Save
# plt.savefig(f'Figures\PushPull.png')

# Display
plt.show()

plt.clf()


