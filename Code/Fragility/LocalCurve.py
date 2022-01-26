import csv
from math import sqrt
import os
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Folder with CSV
directory = 'Output\Connection_Fragility\Data\Cloud'


def printFragility(intensity_measure, probability, upper_confidence, lower_confidence, damage_state, identifier):

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
    plt.title(f'Fragility {damage_state} {identifier}')
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
    plt.savefig(f'Output\Connection_Fragility\Figures\{damage_state}\{damage_state}_Fragility_{identifier}.png')
    plt.clf()


def printScatter(scatter_Sa, scatter_DCR, regression_Sa, regression_DCR, damage_state, identifier):

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
        label = 'Cloud',
        color = 'r',
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
    plt.title(f'Fit {damage_state} {identifier}')
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
    plt.savefig(f'Output\Connection_Fragility\Figures\{damage_state}\{damage_state}_Regression_{identifier}.png')
    plt.clf()


def computeFragility(dictionary, regression_parameters):

    limit_states = ['DCR1', 'DCR2', 'DCRT']

    demandcapacityratio_predicted = {}
    fragility = {}
    upper = {}
    lower = {}

    for limit_state in limit_states:

        # Lavoro con i dati in np array
        points_cloud = np.array([dictionary[limit_state], dictionary['IM']])

        # Separo le 2 liste
        demandcapacityratio_cloud = points_cloud[0]
        intensitymeasure_cloud = points_cloud[1]

        # Calcolo il log naturale
        demandcapacityratio_cloud = np.log(demandcapacityratio_cloud)
        intensitymeasure_cloud = np.log(intensitymeasure_cloud)

        # x è la variabile dipendente
        # print(len(demandcapacityratio_cloud),limit_state,dictionary['identity'])
        b, a = np.polyfit(intensitymeasure_cloud, demandcapacityratio_cloud, 1)
        beta = sqrt(np.sum((a + b * intensitymeasure_cloud - demandcapacityratio_cloud) ** 2) / (len(demandcapacityratio_cloud) - 2))
        
        # Creo fragility
        intensitymeasure = np.linspace(0.01, 5, 500)
        demandcapacityratio_predicted[limit_state] = intensitymeasure ** b * np.exp(a)

        fragility[limit_state] = norm.cdf(np.log(demandcapacityratio_predicted[limit_state]) / beta)
        upper[limit_state] = norm.cdf((np.log(demandcapacityratio_predicted[limit_state]) + beta) / beta)
        lower[limit_state] = norm.cdf((np.log(demandcapacityratio_predicted[limit_state]) - beta) / beta)

        # Calcolo i parametri di correzione dovuti alla logistica
        exponents = -(regression_parameters[0] + regression_parameters[1] * np.log(intensitymeasure))
        correction_multiplier = np.exp(exponents)/(1 + np.exp(exponents))
        correction_add = 1/(1 + np.exp(exponents))

        # Correggo le fragility
        fragility[limit_state] = fragility[limit_state] * correction_multiplier + correction_add
        upper[limit_state] = upper[limit_state] * correction_multiplier + correction_add
        lower[limit_state] = lower[limit_state] * correction_multiplier + correction_add

        # Print Graph
        printFragility(
            intensity_measure = intensitymeasure,
            probability = fragility[limit_state],
            upper_confidence = upper[limit_state],
            lower_confidence = lower[limit_state],
            damage_state = limit_state.replace('CR', 'S'),
            identifier = dictionary['identity']
        )

        printScatter(
            scatter_Sa = points_cloud[1],
            scatter_DCR = points_cloud[0],
            regression_DCR = demandcapacityratio_predicted[limit_state],
            regression_Sa = intensitymeasure,
            damage_state = limit_state.replace('CR', 'S'),
            identifier = dictionary['identity']
        )

    # Formatto i dati per poterli scrivere
    writedata = [intensitymeasure]

    for limit_state in limit_states:

        writedata.append(demandcapacityratio_predicted[limit_state])
        writedata.append(fragility[limit_state])
        writedata.append(upper[limit_state])
        writedata.append(lower[limit_state])

    writedata = np.transpose(writedata)
    writedata = writedata.tolist()

    # Scrivo le curve
    auxiliay = 'identity'
    with open(f'Output\Connection_Fragility\Data\Fragility\Fragility_{dictionary[auxiliay]}.csv', 'w', newline = '') as csvfile:

        writer = csv.writer(csvfile)

        header = ['IM', 'DCR1', 'P', 'Upper', 'Lower', 'DCR2', 'P', 'Upper', 'Lower', 'DCRT', 'P', 'Upper', 'Lower']

        writer.writerow(header)

        for row in writedata:

            writer.writerow(row)

    
def logisticRegression(collapse_data, no_collapse_data):

    def objective(regression_parameters):

        # Definisco le variabili di input
        a0 = regression_parameters[0]
        a1 = regression_parameters[1]

        # Calcolo la likelihood di collasso e non collasso per ogni caso
        total_log_likelihood = 0

        for point in collapse_data['IM']:

            likelihood = 1/(1 + np.exp(-(a0 + a1 * np.log(point))))
            total_log_likelihood += np.log(likelihood)


        for point in no_collapse_data['IM']:

            likelihood = 1 - 1/(1 + np.exp(-(a0 + a1 * np.log(point))))
            total_log_likelihood += np.log(likelihood)


        return -total_log_likelihood


    regression_parameters = minimize(objective, [1, 1])['x']

    return regression_parameters

# ------------------------------------------------------------------------------------
# MAIN ROUTINE
# ------------------------------------------------------------------------------------

for filename in os.listdir(directory):

    # Salverò i dati in un dizionario
    no_collapse_data = {
        'identity'  : '',
        'IM'        : [],
        'DCR1'      : [],
        'DCR2'      : [],
        'DCRT'      : []
    }

    collapse_data = {
        'identity'  : '',
        'IM'        : [],
        'DCR2'      : []
    } 

    with open(f'{directory}\{filename}') as csvfile:

        csvdata = csv.reader(csvfile)

        no_collapse_data['identity'] = filename[6:-4]
        collapse_data['identity'] = filename[6:-4]

        for i, row in enumerate(csvdata):

            if i == 0:
                # skip the header
                continue

            else:

                if float(row[3]) >= 1:

                    collapse_data['IM'].append(float(row[1]))
                    collapse_data['DCR2'].append(float(row[3]))

                else:
                
                    no_collapse_data['IM'].append(float(row[1]))
                    no_collapse_data['DCR1'].append(float(row[2]))
                    no_collapse_data['DCR2'].append(float(row[3]))
                    no_collapse_data['DCRT'].append(float(row[4]))

    regression_parameters = logisticRegression(collapse_data, no_collapse_data)

    computeFragility(no_collapse_data, regression_parameters)
