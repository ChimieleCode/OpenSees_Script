import csv
import os
import math
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from Fragility.LogisticRegression import collapse_IDs, regression_parameters

# directory
directory = 'Output\Cloud'


def printFragility(intensity_measure, probability, upper_confidence, lower_confidence, damage_state):

    plt.plot(
        intensity_measure,
        probability,
        label = 'Fragility',
        color = 'r',
        linestyle = '-',
        linewidth = 1.5
    )

    plt.plot(
        intensity_measure,
        upper_confidence,
        label = 'Upper confidence',
        color = 'r',
        linestyle = ':',
        linewidth = 0.75
    )

    plt.plot(
        intensity_measure,
        lower_confidence,
        label = 'Lower confidence',
        color = 'r',
        linestyle = ':',
        linewidth = 0.75
    )
    
    # Labels
    plt.title(f'Fragility {damage_state}')
    plt.ylabel('P(DCR > 1|Sa)')
    plt.xlabel('Sa [g]')
    plt.legend()

    # Opzioni
    plt.xlim(left = 0, right = 4)
    plt.ylim(bottom = 0, top = 1)

    plt.grid(
        True, 
        linestyle = '--'
    )

    # plt.show()
    plt.savefig(f'Output\Fragility\Figures\Fragility_{damage_state}')
    plt.clf()


def printScatter(scatter_Sa, scatter_DCR, regression_Sa, regression_DCR, damage_state, scatter_SaC, scatter_DCRC):

     # PLOT SCATTER
    plt.plot(
        regression_DCR,
        regression_Sa,
        label = 'Regression',
        color = '0.5',
        linestyle = '-.',
        linewidth = 1
    )

    plt.plot(
        scatter_DCR,
        scatter_Sa,
        label = 'Cloud NoC',
        color = 'r',
        linestyle = '',
        marker = 'o',
        markersize = 3
    )

    plt.plot(
        scatter_DCRC,
        scatter_SaC,
        label = 'Cloud C',
        color = 'b',
        linestyle = '',
        marker = 'o',
        markersize = 3
    )

    plt.plot(
        [1 ,1],
        [0.01, 10],
        label = 'Limit State',
        color = 'k',
        linestyle = '--',
        linewidth = 0.75
    )

    # Labels
    plt.title(f'Fit {damage_state}')
    plt.ylabel('Sa [g]')
    plt.xlabel('DCR')
    plt.legend()

    # Opzioni
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(left = 0.01, right = 10)
    plt.ylim(bottom = 0.01, top = 10)

    plt.grid(
        True, 
        linestyle = '--'
    )

    # plt.show()
    plt.savefig(f'Output\Fragility\Figures\Regression_{damage_state}')
    plt.clf()



# Import cloud points
for filename in os.listdir(directory):

    # Get file data
    points_cloud = [[], []]
    points_collapse = [[], []]

    with open(f'{directory}\{filename}') as csvfile:

        data = csv.reader(csvfile)

        for i, row in enumerate(data):

            if i == 0:
                continue

            if collapse_IDs.__contains__(i):

                points_collapse[0].append(float(row[1]))
                points_collapse[1].append(float(row[2]))

            else:

                points_cloud[0].append(float(row[1]))
                points_cloud[1].append(float(row[2]))
    
    # Turn in np array
    points_cloud = np.array(points_cloud)
    points_collapse = np.array(points_collapse)
    
    # Split x and y and find pow reg
    demandcapacityratio_cloud = points_cloud[0]
    intensitymeasure_cloud = points_cloud[1]

    demandcapacityratio_cloud = np.log(demandcapacityratio_cloud)
    intensitymeasure_cloud = np.log(intensitymeasure_cloud)

    # Effettuo la regressione
    b, a = np.polyfit(intensitymeasure_cloud, demandcapacityratio_cloud, 1)
    beta = math.sqrt(np.sum((a + b * intensitymeasure_cloud - demandcapacityratio_cloud) ** 2) / (len(demandcapacityratio_cloud) - 2))

    # Creo Fragility base
    intensitymeasure = np.linspace(0.01, 5, 500)

    demandcapacityratio_predicted = intensitymeasure ** b * np.exp(a)

    fragility = norm.cdf(np.log(demandcapacityratio_predicted) / beta)
    upper = norm.cdf((np.log(demandcapacityratio_predicted) + beta) / beta)
    lower = norm.cdf((np.log(demandcapacityratio_predicted) - beta) / beta)

    # Calcolo i parametri di correzione dovuti alla logistica
    exponents = -(regression_parameters[0] + regression_parameters[1] * np.log(intensitymeasure))
    correction_multiplier = np.exp(exponents)/(1 + np.exp(exponents))
    correction_add = 1/(1 + np.exp(exponents))

    # Correggo le fragility
    fragility = fragility * correction_multiplier + correction_add
    upper = upper * correction_multiplier + correction_add
    lower = lower * correction_multiplier + correction_add
    
    # Print Graph
    printFragility(
        intensity_measure = intensitymeasure,
        probability = fragility,
        upper_confidence = upper,
        lower_confidence = lower,
        damage_state = filename[6:-4]
    )

    printScatter(
        scatter_Sa = points_cloud[1],
        scatter_DCR = points_cloud[0],
        regression_DCR = demandcapacityratio_predicted,
        regression_Sa = intensitymeasure,
        damage_state = filename[6:-4],
        scatter_SaC = points_collapse[1],
        scatter_DCRC = points_collapse[0]
    )

    # Scrivo csv
    data = [intensitymeasure, demandcapacityratio_predicted, fragility, upper, lower]
    data = np.transpose(data)
    data = data.tolist()

    # Scrivo la curva
    with open(f'Output\Fragility\{filename[6:]}', 'w', newline = '') as csvfile:

        writer = csv.writer(csvfile)

        header = ['IM', 'DCR', 'P', 'Upper', 'Lower']

        writer.writerow(header)

        for row in data:

            writer.writerow(row)
