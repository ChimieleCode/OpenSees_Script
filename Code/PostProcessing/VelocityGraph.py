import csv

import matplotlib.pyplot as plt

from ImportFromJson import time_history_analysis, frame

# Utile per il idagramma a scaletta
storey_series = []

for j in range(frame.m + 1):

    storey_series.append(j)
    storey_series.append(j + 1)


for time_history in time_history_analysis:

    storey_envelopes = []
    
    with open(f'Output\TimeHistory\TimeHistory_Storey_Velocity.{time_history.id}_{time_history.sf}.out') as csvfile:

        data = csv.reader(csvfile, delimiter=' ')

        storey_vel = []

        for j in range(frame.m + 1):            # Inizializzo le liste che conterranno i dati

            storey_vel.append([])


        for row in data:                        # Trascrivo i dati

            for j in range(frame.m + 1):

                storey_vel[j].append(abs(float(row[j + 1])))


        for j in range(0, frame.m + 1):       # Calcolo l'envelope ogni piano

            storey_envelopes.append(max(storey_vel[j]))

        # print(storey_envelopes)


    storey_vel = []

    for j in range(frame.m + 1):

        storey_vel.append(storey_envelopes[j])
        storey_vel.append(storey_envelopes[j])


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
#   VELOCITA' RELATIVA
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Opensees
    plt.plot(
        storey_vel,
        storey_series,
        label = 'OpenSees',
        color = 'r',
        linestyle = '-',
        linewidth = 1
        )

    # Titoli Assi
    plt.ylabel('Floor')
    plt.xlabel('Velocity [m/s]')

    # Titolo Grafico
    plt.title(f'Floor Velocity ID: {time_history.id}  SF: {time_history.sf}')

    # Mostra Legenda e Griglia
    plt.legend()

    plt.grid(
        True, 
        linestyle = '--'
        )

    # Save
    plt.savefig(f'Figures\Velocity_Envelopes\Vel_{time_history.id}_{time_history.sf}.png')

    # Display
    # plt.show()

    plt.clf()


        

            

            
            
            












            



