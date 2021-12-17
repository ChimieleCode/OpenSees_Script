import csv
from math import sqrt
import os
import numpy as np
from scipy.stats import norm

# Folder with CSV
directory = 'Output\Cloud'

regression_params = []

for filename in os.listdir(directory):

    # Get file data
    points_cloud = []

    with open(f'{directory}\{filename}') as csvfile:

        data = csv.reader(csvfile)

        for i, row in enumerate(data):

            if i == 0:

                continue

            else:

                points_cloud.append([float(row[1]), float(row[2])])
    
    # Turn in np array
    points_cloud = np.array(points_cloud)

    points_cloud = np.transpose(points_cloud)

    # Split x and y and find pow reg
    demandcapacityratio_cloud = points_cloud[0]
    intensitymeasure_cloud = points_cloud[1]

    demandcapacityratio_cloud = np.log(demandcapacityratio_cloud)
    intensitymeasure_cloud = np.log(intensitymeasure_cloud)

    # x è la variabile dipendente
    b, a = np.polyfit(intensitymeasure_cloud, demandcapacityratio_cloud, 1)

    beta = sqrt(np.sum((a + b * intensitymeasure_cloud - demandcapacityratio_cloud) ** 2) / (len(demandcapacityratio_cloud) - 2))

    regression_params.append([filename[-7:-4], np.exp(a), b, beta])  # aIM^b

    # create fragility
    intensitymeasure = np.linspace(0.01, 5, 500) # Non Ln

    demandcapacityratio_predicted = intensitymeasure ** b * np.exp(a)

    fragility = norm.cdf(np.log(demandcapacityratio_predicted) / beta)
    upper = norm.cdf((np.log(demandcapacityratio_predicted) + beta) / beta)
    lower = norm.cdf((np.log(demandcapacityratio_predicted) - beta) / beta)


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


# Scrivo i parametri
    with open('Output\Fragility\Params.csv', 'w', newline = '') as csvfile:

        writer = csv.writer(csvfile,)

        header = ['SL', 'a', 'b', 'beta']

        writer.writerow(header)

        for row in regression_params:

            writer.writerow(row)