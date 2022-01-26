import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

max_Sa = 2.5

directory = 'Output\IDA\Curves'

damage_states = ['DS1', 'DS2', 'DST']

for r, damage_state in enumerate(damage_states):

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
                        'DCR' : float(row[r + 1])
                        })

            curves.append(curve)
            

    # Calcolo le intersezioni
    points = []

    # print(curves)

    for curve in curves:

        for k, value in enumerate(curve):

            if value['DCR'] >= 1:

                point = (1 - curve[k - 1]['DCR']) * (curve[k]['IM'] - curve[k - 1]['IM']) / (curve[k]['DCR'] - curve[k - 1]['DCR']) + curve[k - 1]['IM']

                points.append(point)

                break

            else:

                continue
    
    points.sort()

    num_points = len(points)

    DS1_fragility = {}

    DS1_fragility['theta'] = np.exp(1 / num_points * sum([np.log(a) for a in points]))
    DS1_fragility['beta'] = (1 / (num_points - 1) * sum([np.log(a / DS1_fragility['theta'])**2 for a in points]))**0.5
    DS1_fragility['IM'] = np.linspace(0.01, 5, 500)
    DS1_fragility['P'] = norm.cdf(np.log(DS1_fragility['IM'] / DS1_fragility['theta']) / DS1_fragility['beta'])
    DS1_fragility['upper'] = norm.cdf((np.log(DS1_fragility['IM'] / DS1_fragility['theta']) + DS1_fragility['beta']) / DS1_fragility['beta'])
    DS1_fragility['lower'] = norm.cdf((np.log(DS1_fragility['IM'] / DS1_fragility['theta']) - DS1_fragility['beta']) / DS1_fragility['beta'])

    # Scrivo la curva a step
    with open(f'Output\IDA\Fragility\{damage_state}_fragility_step.csv', 'w', newline = '') as csvfile:

        writer = csv.writer(csvfile)

        DS1_fragility['IMstep'] = []
        DS1_fragility['Pstep']  = []

        for i, point in enumerate(points):

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
    plt.title(f'Fragility {damage_state} IDA')

    # Opzioni
    plt.xlim(left = 0, right = max_Sa)
    plt.ylim(bottom = 0, top = 1)

    # Mostra Legenda e Griglia
    plt.legend()

    plt.grid(
        True, 
        linestyle = '--'
        )

    # Save
    plt.savefig(f'Output\IDA\Figures\Fragility_{damage_state}.png')

    # Display
    # plt.show()

    plt.clf()



    # .---------------------------------------------------------------------------

    for i, curve in enumerate(curves):

        display_curve = {
            'DCR'   : [],
            'IM'    : []
        }

        [display_curve['DCR'].append(a['DCR']) for a in curve]
        [display_curve['IM'].append(a['IM']) for a in curve]

        plt.plot(
            display_curve['DCR'],
            display_curve['IM'],
            label = f'{i + 1}',
            color = '0.7',
            linestyle = '-',
            linewidth = 0.75
            )

    plt.plot(
            [1, 1],
            [0, max_Sa - 0.5],
            label = 'LS',
            color = 'k',
            linestyle = '-.',
            linewidth = 1.5
            )

    plt.plot(
            np.ones(len(points)),
            points,
            label = 'Strikes',
            color = 'r',
            linestyle = '',
            marker = 'x',
            markersize = 2.5
        )

    # Titoli Assi
    plt.ylabel('Sa(T1) [g]')
    plt.xlabel(f'DCR {damage_state}')

    # Titolo Grafico
    plt.title('IDA')

    # Opzioni
    plt.xlim(left = 0, right = 1.5)
    plt.ylim(bottom = 0, top = max_Sa - 0.5)

    # Mostra Legenda e Griglia

    plt.grid(
        True, 
        linestyle = '--'
        )

    # Save
    plt.savefig(f'Output\IDA\Figures\IDA_{damage_state}.png')

    # Display
    # plt.show()

    plt.clf()
