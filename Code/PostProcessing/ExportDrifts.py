import csv
from Graphs.DriftGraph import global_drift_envelopes
from ImportFromJson import frame


with open('Output\Processed\Drifts.csv', 'w', newline = '') as csvfile:

    writer = csv.writer(csvfile)

    # Header
    header = ['Piano'] 

    for i in range(len(global_drift_envelopes)):

        header.append(f'TH{i + 1}')

    
    writer.writerow(header)

    # Data
    for j in range(frame.m):

        # print(j)

        level_drifts = [j + 1]

        for data in global_drift_envelopes:

            level_drifts.append(data[j])
        

        # print(level_drifts)

        writer.writerow(level_drifts)



            

