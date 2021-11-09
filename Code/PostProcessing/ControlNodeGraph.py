import csv
import matplotlib.pyplot as plt

from ImportFromJson import time_history_analysis, frame

for time_history in time_history_analysis:

    time = []
    base_reaction = []
    displacement = []

    # LOAD BASE REACTION DATA AND TIME
    with open(f'Output\TimeHistory\TimeHistory_Base_Reactions.{time_history.id}_{time_history.sf}.out') as csvfile:

        data = csv.reader(csvfile, delimiter=' ')

        for row in data:
            
            sum = 0

            for i in range(1,len(row)):

                sum += float(row[i])
            

            base_reaction.append(-sum)
            time.append(float(row[0]))

    # LOAD CONTROL NODE DISPLACEMENT DATA
    with open(f'Output\TimeHistory\TimeHistory_ControlNode_Displacement.{time_history.id}_{time_history.sf}.out') as csvfile:

        data = csv.reader(csvfile, delimiter=' ')

        for row in data:
            
            displacement.append(float(row[1]))

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# FORZA-SPOSTAMENTO
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Opensees
    plt.plot(
        displacement,
        base_reaction,
        label = 'OpenSees',
        color = 'r',
        linestyle = '-',
        linewidth = 1
        )

    # Titoli Assi
    plt.ylabel('Base Reaction [kN]')
    plt.xlabel('Displacement [m]')

    # Titolo Grafico
    plt.title(f'Shear-Displacement ID: {time_history.id}  SF: {time_history.sf}')
    # Mostra Legenda e Griglia
    plt.legend()

    plt.grid(
        True, 
        linestyle = '--'
        )

    # Save
    plt.savefig(f'Figures\Base_Shear_Disp\BS_D_{time_history.id}_{time_history.sf}.png')

    # Display
    # plt.show()

    plt.clf()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# SPOSTAMENTO-TEMPO
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Opensees
    plt.plot(
        time,
        displacement,
        label = 'OpenSees',
        color = 'r',
        linestyle = '-',
        linewidth = 1
        )

    # Titoli Assi
    plt.ylabel('Base Reaction [kN]')
    plt.xlabel('Displacement [m]')

    # Titolo Grafico
    plt.title(f'Time-Displacement ID: {time_history.id}  SF: {time_history.sf}')

    # Mostra Legenda e Griglia
    plt.legend()

    plt.grid(
        True, 
        linestyle = '--'
        )

    # Save
    plt.savefig(f'Figures\Disp_Time\D_T_{time_history.id}_{time_history.sf}.png')

    # Display
    # plt.show()

    plt.clf()
