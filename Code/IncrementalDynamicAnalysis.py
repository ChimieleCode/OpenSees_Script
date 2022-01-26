import math
import csv

from ModelOptions import initialSa, initialstep, maxiterIDA
from BasicFunctions.SpectralAcceleration import spectralAcceleration
from AnalysisDefinition.SingleTH import runSingleTimeHistory
from MomentoRotazione import damage_state
from ImportFromJson import frame

def computeDemandCapacityRatio(time_history):

    gaps = []

    for j in range(2 * frame.m + 2):    # 2 * Piani + colonna interna + colonna esterna

        gaps.append([])

    with open(f'Output\IDA\Outputs_Junk\TimeHistory_Section_Gaps.{time_history.id}_{time_history.serializedid}.out') as csvfile:

        data = csv.reader(csvfile, delimiter=' ')

        for row in data:

            drift = 0

            for i in range(1,len(row)):

                if i%2 == 0:

                    gaps[math.floor(i/2) - 1].append(abs(float(row[i]) - drift))
                
                else:

                    drift = float(row[i])


    gap_envelopes = []

    for level in gaps:

        gap_envelopes.append(max(level))

    demand_capacity_ratio_DST = []
    demand_capacity_ratio_DS1 = []
    demand_capacity_ratio_DS2 = []

    # Calcolo i DCR
    for i, gap in enumerate(gap_envelopes):

        # DS1
        if damage_state[i][0] != None:

            demand_capacity_ratio_DS1.append(gap/damage_state[i][0])
        
        else:

            demand_capacity_ratio_DS1.append(0) 

        # DS2   
        if damage_state[i][1] != None:

            demand_capacity_ratio_DS2.append(gap/damage_state[i][1])
        
        else:

            demand_capacity_ratio_DS2.append(0) 

        # DST   
        if damage_state[i][2] != None:

            demand_capacity_ratio_DST.append(gap/damage_state[i][2])
        
        else:

            demand_capacity_ratio_DST.append(0) 

    # print(gap_envelopes)
    # print(demand_capacity_ratio_DS1)
    # print(demand_capacity_ratio_DS2)
    # print(demand_capacity_ratio_DST)

    # print(damage_state)
    

    global_DCR_DS1 = max(demand_capacity_ratio_DS1)
    global_DCR_DS2 = max(demand_capacity_ratio_DS2)
    global_DCR_DST = max(demand_capacity_ratio_DST)

    return [global_DCR_DS1, global_DCR_DS2, global_DCR_DST]





def incrementalDynamicAnalysis(time_histories = [], structure_periods = []):

    # Cancella TUTTA la cartella


    serializedid = 1

    for time_history in time_histories:

        # Inizializzo gli array di output
        intensity_measures = [0]
        demandcapacity_ratios_DS1 = [0]
        demandcapacity_ratios_DS2 = [0]
        demandcapacity_ratios_DST = [0]

        # Calcolo Sa e scalo in maniera che Sa di prima iterazione sia pari a quella definita dall'utente
        unscaledSa = spectralAcceleration(time_history = time_history, structure_period = structure_periods[0])

        initialSF = initialSa / unscaledSa

        time_history.sf = initialSF

        # Inizializzo parametri per la convergenza
        step = initialSF * initialstep

        bisection = False


        # Inizia il loop
        while ((demandcapacity_ratios_DS1[-1] < 1) or (demandcapacity_ratios_DST[-1] < 1) or (demandcapacity_ratios_DS2[-1] < 1)) and (step > initialstep * 0.5**maxiterIDA):

            time_history.serializedid = serializedid
            serializedid += 1

            # Mando la TH e salvo lo status
            success = runSingleTimeHistory(time_history = time_history, structure_periods = structure_periods)

            # Capisto se sto già iterando per la convergenza con algoritmo di bisezione o è necessario cominciare
            bisection = (not success) or (bisection)

            if bisection:
                
                # Biseziono lo step
                step = step * 0.5

                if success:

                    demandcapacity_ratios_DS1.append(computeDemandCapacityRatio(time_history)[0])
                    demandcapacity_ratios_DS2.append(computeDemandCapacityRatio(time_history)[1])
                    demandcapacity_ratios_DST.append(computeDemandCapacityRatio(time_history)[2])
                    intensity_measures.append(spectralAcceleration(time_history = time_history, structure_period = structure_periods[0]))

                    time_history.sf = time_history.sf + step
                
                else:

                    time_history.sf = time_history.sf - step

            else:

                demandcapacity_ratios_DS1.append(computeDemandCapacityRatio(time_history)[0])
                demandcapacity_ratios_DS2.append(computeDemandCapacityRatio(time_history)[1])
                demandcapacity_ratios_DST.append(computeDemandCapacityRatio(time_history)[2])
                intensity_measures.append(spectralAcceleration(time_history = time_history, structure_period = structure_periods[0]))

                time_history.sf = time_history.sf + step


        with open(f'Output\IDA\Curves\IDA_Curve.{time_history.id}.csv', 'w', newline = '') as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(['IM', 'DCR'])

            for i in range(len(intensity_measures)):

                writer.writerow([intensity_measures[i], demandcapacity_ratios_DS1[i], demandcapacity_ratios_DS2[i], demandcapacity_ratios_DST[i]])

    

    import PostProcessing.IDAProcessing
                    





