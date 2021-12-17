import csv

import matplotlib.pyplot as plt

from BasicFunctions.ConsistentTimeSeries import consistentTimeSeries

from ImportFromJson import time_history_analysis, frame

g = 9.81

# Utile per il idagramma a scaletta
storey_series = []
global_acc_envelopes = []

for j in range(frame.m + 1):

    storey_series.append(j)
    storey_series.append(j + 1)


# Elaboro i dati per ogni TH
for time_history in time_history_analysis:

    # Carico le accelerazioni alla base
    base_acc = consistentTimeSeries(timehistory = time_history)

    storey_envelopes = []
    
    # Carico le accelerazioni relative
    with open(f'Output\TimeHistory\TimeHistory_Storey_Acceleration.{time_history.id}_{time_history.sf}.out') as csvfile:

        data = csv.reader(csvfile, delimiter=' ')

        storey_acc = []

        for j in range(frame.m + 1):            # Inizializzo le liste che conterranno i dati

            storey_acc.append([])


        for row in data:                        # Trascrivo i dati

            for j in range(frame.m + 1):

                storey_acc[j].append(float(row[j + 1]))


        for i in range(len(storey_acc[0])):      # Unisco Base e Relative

            for j in range(frame.m + 1):

                # Se l'accelerogramma termina, metti 0
                try:

                    storey_acc[j][i] = abs(base_acc[i] + storey_acc[j][i])


                except:

                    storey_acc[j][i] = abs(storey_acc[j][i])


        for j in range(0, frame.m + 1):       # Calcolo l'envelope ogni piano

            storey_envelopes.append(max(storey_acc[j]) / g)

        # print(storey_envelopes)

    storey_acc = []

    global_acc_envelopes.append(storey_envelopes)

    for j in range(frame.m + 1):

        storey_acc.append(storey_envelopes[j])
        storey_acc.append(storey_envelopes[j])


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ACCELERAZIONE ASSOLUTA
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Opensees
    plt.plot(
        storey_acc,
        storey_series,
        label = 'OpenSees',
        color = 'r',
        linestyle = '-',
        linewidth = 1
        )

    # Titoli Assi
    plt.ylabel('Floor')
    plt.xlabel('Acceleration [g]')

    # Titolo Grafico
    plt.title(f'Floor Acceleration ID: {time_history.id}  SF: {time_history.sf}')

    # Mostra Legenda e Griglia
    plt.legend()

    # Imposta i valori limite degli assi
    plt.ylim(ymin = 0, ymax = frame.m)
    plt.xlim(xmin = 0, xmax = 1)

    # Imposta i piani
    plt.yticks(range(frame.m + 2))

    plt.grid(
        True, 
        linestyle = '--'
        )

    # Save
    plt.savefig(f'Figures\Acc_Envelopes\Acc_{time_history.id}_{time_history.sf}.png')

    # Display
    # plt.show()

    plt.clf()


        

            

            
            
            












            



