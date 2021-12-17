import csv
import matplotlib.pyplot as plt

from ImportFromJson import time_history_analysis, frame

# Utile per il idagramma a scaletta
storey_series = []
global_drift_envelopes = []

for j in range(frame.m):

    storey_series.append(j)
    storey_series.append(j + 1)


for time_history in time_history_analysis:

    storey_envelopes = []

    # LOAD STOREY DISPLACEMENT DATA
    with open(f'Output\TimeHistory\TimeHistory_Storey_Displacement.{time_history.id}_{time_history.sf}.out') as csvfile:

        data = csv.reader(csvfile, delimiter=' ')

        storey_displacements = []
        storey_drifts = []

        for j in range(frame.m + 1):            # Inizializzo le liste che conterranno i dati

            storey_displacements.append([])


        for j in range(frame.m):            

            storey_drifts.append([])


        for row in data:                        # Trascrivo i dati

            for j in range(frame.m + 1):

                storey_displacements[j].append(float(row[j + 1]))

        
        for j in range(1, frame.m + 1):       # Calcolo i drift per ogni piano escluso il PT j-esimo

            for k in range(len(storey_displacements[0])):       # Per ogni tempo k

                storey_drifts[j - 1].append(abs(storey_displacements[j][k] - storey_displacements[j - 1][k]) / frame.storey)


        for j in range(0, frame.m):       # Calcolo l'envelope ogni piano escluso il PT j-esimo

            storey_envelopes.append(max(storey_drifts[j]))

    # PROCESSO I DATI PER FARE SCALETTA
    storey_drifts = []

    for j in range(frame.m):

        storey_drifts.append(storey_envelopes[j])
        storey_drifts.append(storey_envelopes[j])

    
    # CALCOLA IL DRIFT MAX
    print(f'Max drift TH: {time_history.id} Drift: {max(storey_envelopes)}')

    global_drift_envelopes.append(storey_envelopes)




# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DRIFT DI PIANO
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Opensees
    plt.plot(
        storey_drifts,
        storey_series,
        label = 'OpenSees',
        color = 'r',
        linestyle = '-',
        linewidth = 1
        )

    # Titoli Assi
    plt.ylabel('Floor')
    plt.xlabel('Drift [rad]')

    # Titolo Grafico
    plt.title(f'Floor Drift ID: {time_history.id}  SF: {time_history.sf}')

    # Mostra Legenda e Griglia
    plt.legend()

    # Imposta i valori limite degli assi
    plt.ylim(ymin = 0, ymax = frame.m)
    plt.xlim(xmin = 0, xmax = 0.04)

    # Imposta i piani
    plt.yticks(range(frame.m + 1))

    plt.grid(
        True, 
        linestyle = '--'
        )

    # Save
    plt.savefig(f'Figures\Drift_Envelopes\Drift_{time_history.id}_{time_history.sf}.png')

    # Display
    # plt.show()

    plt.clf()
