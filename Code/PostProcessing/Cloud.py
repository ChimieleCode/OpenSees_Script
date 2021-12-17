import csv

from PostProcessing.SectionGaps import global_DCR_DS1, global_DCR_DS2, global_DCR_DST
from AnalysisDefinition.TimeHistory import spectral_response 

# global_DCR_DS1 = [[1, 0.27896174747804386], [2, 0.28126931389396786], [3, 0.44095115696216836], [4, 0.33864425806026355], [5, 0.7645643659027233], [6, 0.8373640081441925], [7, 0.6888659383862444]]
# global_DCR_DS2 = [[1, 0.12933171227895135], [2, 0.13040154181101768], [3, 0.18752803478204755], [4, 0.13911329867854114], [5, 0.31770212049497765], [6, 0.38821710128044673], [7, 0.3193707099542446]]
# spectral_response = [[1, 0.1805800477786648], [2, 0.1510976970752806], [3, 0.3045396943746819], [4, 0.16365797547285382], [5, 0.4946830117396905], [6, 0.2817064378680877], [7, 0.2671389781800418]]

cloud_DST = []
cloud_DS1 = []
cloud_DS2 = []

header = ['Time History ID', 'DCR', 'Sa']

for i, point in enumerate(spectral_response):

    cloud_DS1.append([point[0], global_DCR_DS1[i][1], point[1]])
    cloud_DS2.append([point[0], global_DCR_DS2[i][1], point[1]])
    cloud_DST.append([point[0], global_DCR_DST[i][1], point[1]])


with open('Output\Cloud\cloud_DS1.csv', 'w', newline = '') as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow(header)

    for point in cloud_DS1:

        writer.writerow(point)


with open('Output\Cloud\cloud_DS2.csv', 'w', newline = '') as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow(header)

    for point in cloud_DS2:

        writer.writerow(point)


with open('Output\Cloud\cloud_DST.csv', 'w', newline = '') as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow(header)

    for point in cloud_DST:

        writer.writerow(point)