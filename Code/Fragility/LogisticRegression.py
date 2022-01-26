import csv
import numpy as np
from scipy.optimize import minimize

no_collapse_points = []
collapse_points = []

with open('Output\Cloud\cloud_DS2.csv') as csvfile:

    data = csv.reader(csvfile)

    for i, row in enumerate(data):

        if i == 0:
            # Salta l'intestazione
            continue

        else:

            cloud_point = {
                'ID'    : int(row[0]),
                'DCR'    : float(row[1]),
                'IM'    : float(row[2])
            }

            if cloud_point['DCR'] >= 1:

                collapse_points.append(cloud_point)

            else:

                no_collapse_points.append(cloud_point)

# Salvo gli ID dei collapse points
collapse_IDs = [point['ID'] for point in collapse_points]

# Calcolo la logistica
def objective(regression_parameters):

    # Definisco le variabili di input
    a0 = regression_parameters[0]
    a1 = regression_parameters[1]

    # Calcolo la likelihood di collasso e non collasso per ogni caso
    total_log_likelihood = 0

    for point in collapse_points:

        likelihood = 1/(1 + np.exp(-(a0 + a1 * np.log(point['IM']))))
        total_log_likelihood += np.log(likelihood)


    for point in no_collapse_points:

        likelihood = 1 - 1/(1 + np.exp(-(a0 + a1 * np.log(point['IM']))))
        total_log_likelihood += np.log(likelihood)


    return -total_log_likelihood

regression_parameters = minimize(objective, [1, 1])['x']

