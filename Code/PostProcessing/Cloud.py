import csv
import math

from ModelOptions import compute_local_fragility
from PostProcessing.SectionGaps import global_DCR_DS1, global_DCR_DS2, global_DCR_DST, demand_capacity_ratio_DS1_matrix, demand_capacity_ratio_DS2_matrix, demand_capacity_ratio_DST_matrix
from AnalysisDefinition.TimeHistory import spectral_response 

# global_DCR_DS1 = [[1, 0.27896174747804386], [2, 0.28126931389396786], [3, 0.44095115696216836], [4, 0.33864425806026355], [5, 0.7645643659027233], [6, 0.8373640081441925], [7, 0.6888659383862444]]
# global_DCR_DS2 = [[1, 0.12933171227895135], [2, 0.13040154181101768], [3, 0.18752803478204755], [4, 0.13911329867854114], [5, 0.31770212049497765], [6, 0.38821710128044673], [7, 0.3193707099542446]]
# spectral_response = [ [1, 0.01], [2, 0.02], [3, 0.03], [4, 0.04], [5, 0.05], [6, 0.06], [7, 0.07], [8, 0.08], [9, 0.09], [10, 0.1], [11, 0.11], [12, 0.12], [13, 0.13], [14, 0.14], [15, 0.15], [16, 0.16], [17, 0.17], [18, 0.18], [19, 0.19], [20, 0.2], [21, 0.21], [22, 0.22], [23, 0.23], [24, 0.24], [25, 0.25], [26, 0.26], [27, 0.27], [28, 0.28], [29, 0.29], [30, 0.3], [31, 0.31], [32, 0.32], [33, 0.33], [34, 0.34], [35, 0.35], [36, 0.36], [37, 0.37], [38, 0.38], [39, 0.39], [40, 0.4], [41, 0.41], [42, 0.42], [43, 0.43], [44, 0.44], [45, 0.45], [46, 0.46], [47, 0.47], [48, 0.48], [49, 0.49], [50, 0.5], [51, 0.51], [52, 0.52], [53, 0.53], [54, 0.54], [55, 0.55], [56, 0.56], [57, 0.57], [58, 0.58], [59, 0.59], [60, 0.6], [61, 0.61], [62, 0.62], [63, 0.63], [64, 0.64], [65, 0.65], [66, 0.66], [67, 0.67], [68, 0.68], [69, 0.69], [70, 0.7], [71, 0.71], [72, 0.72], [73, 0.73], [74, 0.74], [75, 0.75], [76, 0.76], [77, 0.77], [78, 0.78], [79, 0.79], [80, 0.8], [81, 0.81], [82, 0.82], [83, 0.83], [84, 0.84], [85, 0.85], [86, 0.86], [87, 0.87], [88, 0.88], [89, 0.89], [90, 0.9], [91, 0.91], [92, 0.92], [93, 0.93], [94, 0.94], [95, 0.95], [96, 0.96], [97, 0.97], [98, 0.98], [99, 0.99], [100, 1], [101, 1.01], [102, 1.02], [103, 1.03], [104, 1.04], [105, 1.05], [106, 1.06], [107, 1.07], [108, 1.08], [109, 1.09], [110, 1.1], [111, 1.11], [112, 1.12], [113, 1.13], [114, 1.14], [115, 1.15], [116, 1.16], [117, 1.17], [118, 1.18], [119, 1.19], [120, 1.2], [121, 1.21], [122, 1.22], [123, 1.23], [124, 1.24], [125, 1.25], [126, 1.26], [127, 1.27], [128, 1.28], [129, 1.29], [130, 1.3], [131, 1.31], [132, 1.32], [133, 1.33], [134, 1.34], [135, 1.35], [136, 1.36], [137, 1.37], [138, 1.38], [139, 1.39], [140, 1.4], [141, 1.41] ]

cloud_DST = []
cloud_DS1 = []
cloud_DS2 = []

# Header globale
header = ['Time History ID', 'DCR', 'Sa']

# Preparo gli array per scrivere
for i, point in enumerate(spectral_response):

    cloud_DS1.append([point[0], global_DCR_DS1[i][1], point[1]])
    cloud_DS2.append([point[0], global_DCR_DS2[i][1], point[1]])
    cloud_DST.append([point[0], global_DCR_DST[i][1], point[1]])

# Scrivo DS1 globale
with open('Output\Cloud\cloud_DS1.csv', 'w', newline = '') as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow(header)

    for point in cloud_DS1:

        writer.writerow(point)

# Scrivo DS2 globale
with open('Output\Cloud\cloud_DS2.csv', 'w', newline = '') as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow(header)

    for point in cloud_DS2:

        writer.writerow(point)

# Scrivo DST globale
with open('Output\Cloud\cloud_DST.csv', 'w', newline = '') as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow(header)

    for point in cloud_DST:

        writer.writerow(point)


# CLOUD points di singole connessioni
if compute_local_fragility:

    # Header locale
    header = ['Time History ID', 'Sa', 'DCR1', 'DCR2', 'DRCT']

    # Definisco delle funzioni per identificare le connessioni
    def floor(i):

        return math.floor(i/2) 


    def vertical(i):

        if (i % 2) == 0:

            return 'ext'
        
        else:

            return 'int'


    # Procedo a scrivere in file
    for i in range(len(demand_capacity_ratio_DS1_matrix[0])):

        with open(f'Output\Connection_Fragility\Data\Cloud\Cloud_{floor(i)}_{vertical(i)}.csv', 'w', newline = '') as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(header)

            for j in range(len(demand_capacity_ratio_DS1_matrix)):

                row = []

                row.append(spectral_response[j][0])
                row.append(spectral_response[j][1])
                row.append(demand_capacity_ratio_DS1_matrix[j][i])
                row.append(demand_capacity_ratio_DS2_matrix[j][i])
                row.append(demand_capacity_ratio_DST_matrix[j][i])

                writer.writerow(row)
