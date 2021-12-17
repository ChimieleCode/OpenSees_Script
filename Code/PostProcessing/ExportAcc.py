import csv
from Graphs.AccelerationGraph import global_acc_envelopes
from ImportFromJson import frame


with open('Output\Processed\Accelerations.csv', 'w', newline = '') as csvfile:

    writer = csv.writer(csvfile)

    # Header
    header = ['Piano'] 

    for i in range(len(global_acc_envelopes)):

        header.append(f'TH{i + 1}')

    
    writer.writerow(header)

    # Data
    for j in range(frame.m + 1):  # Nelle acc c'è anche il pian terreno

        level_acc = [j]

        for data in global_acc_envelopes:

            level_acc.append(data[j])
       

        writer.writerow(level_acc)



            



