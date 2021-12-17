import csv
import math

from ImportFromJson import time_history_analysis, frame
from MomentoRotazione import damage_state

g = 9.81

global_DCR_DST = []
global_DCR_DS1 = []
global_DCR_DS2 = []

for time_history in time_history_analysis:

    gaps = []

    for j in range(2 * frame.m + 2):    # 2 * Piani + colonna interna + colonna esterna

        gaps.append([])


    with open(f'Output\TimeHistory\TimeHistory_Section_Gaps.{time_history.id}_{time_history.sf}.out') as csvfile:

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
    

    global_DCR_DS1.append([time_history.id, max(demand_capacity_ratio_DS1)])
    global_DCR_DS2.append([time_history.id, max(demand_capacity_ratio_DS2)])
    global_DCR_DST.append([time_history.id, max(demand_capacity_ratio_DST)])

# print(global_DCR_DS1)
# print(global_DCR_DS2)
# print(global_DCR_DST)


