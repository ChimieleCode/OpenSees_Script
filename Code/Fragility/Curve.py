import csv
import os
import numpy as np
import matplotlib.pyplot as plt

directory_cloud = 'Output\Cloud'
directory_fragility = 'Output\Fragility'
directory_figures = 'Output\Fragility\Figures'

fragility_curves = []

for filename in os.listdir(directory_cloud):

    points_cloud = []

    with open(f'{directory_cloud}\{filename}') as csvfile:

        data = csv.reader(csvfile)

        for i, row in enumerate(data):

            if i == 0:

                continue

            else:

                points_cloud.append([float(row[1]), float(row[2])])

        points_cloud = np.array(points_cloud)

        points_cloud = np.transpose(points_cloud)



    curves = [[], [], [], [], []]     # 0:IM  1:DCR   2:Frag  3:Up    4:Low

    with open(f'{directory_fragility}\{filename[6:]}') as csvfile:

        data = csv.reader(csvfile)

        for i, row in enumerate(data):

            if i == 0:

                continue

            else:
                
                for j, entry in enumerate(row):

                    curves[j].append(float(entry))


    fragility_curves.append([filename[6:-4], curves[0], curves[2]])
 
    # PLOT FRAGILITY
    plt.plot(
        curves[0],
        curves[2],
        label = 'Fragility',
        color = 'r',
        linestyle = '-',
        linewidth = 1.5
    )

    plt.plot(
        curves[0],
        curves[3],
        label = 'Upper confidence',
        color = 'r',
        linestyle = ':',
        linewidth = 0.75
    )

    plt.plot(
        curves[0],
        curves[4],
        label = 'Lower confidence',
        color = 'r',
        linestyle = ':',
        linewidth = 0.75
    )
    
    # Labels
    plt.title(f'Fragility {filename[6:-4]}')
    plt.ylabel('P(DCR > 1|Sa)')
    plt.xlabel('Sa [g]')
    plt.legend()

    # Opzioni
    plt.xlim(left = 0, right = 2)
    plt.ylim(bottom = 0, top = 1)

    plt.grid(
        True, 
        linestyle = '--'
    )

    # plt.show()
    plt.savefig(f'{directory_figures}/Fragility_{filename[6:-4]}.png')
    plt.clf()


    # --------------------------------------------------------------------------------------------------------


    # PLOT SCATTER
    plt.plot(
        curves[1],
        curves[0],
        label = 'Regression',
        color = '0.5',
        linestyle = '-.',
        linewidth = 1
    )

    plt.plot(
        points_cloud[0],
        points_cloud[1],
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
    plt.title(f'Fit {filename[6:-4]}')
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
    plt.savefig(f'{directory_figures}/Regression_{filename[6:-4]}.png')
    plt.clf()


# --------------------------------------------------------------------------------------------------------

# PLOT FRAGILITY

for curve in fragility_curves:

    plt.plot(
        curve[1],
        curve[2],
        label = curve[0],
        color = 'r',
        linestyle = '-',
        linewidth = 1.5
    )

# Labels
plt.title(f'Fragility')
plt.ylabel('P(DCR > 1|Sa)')
plt.xlabel('Sa [g]')
plt.legend()

# Opzioni
plt.xlim(left = 0, right = 2)
plt.ylim(bottom = 0, top = 1)

plt.grid(
    True, 
    linestyle = '--'
)

# plt.show()
plt.savefig(f'{directory_figures}/Fragility.png')
plt.clf()
