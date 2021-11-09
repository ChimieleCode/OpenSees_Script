import csv

def consistentTimeSeries(timehistory):

    base_acc = []
    new_acc = []

    # Load Base Exitation
    with open(f'acc_{timehistory.id}.txt') as csvfile:

        data = csv.reader(csvfile, delimiter=' ')

        for row in data:                       

            # If overshoot, 0
            try:

                base_acc.append(float(row[0]) * timehistory.sf)      # in m/s2

            except:

                base_acc.append(0)

    #Interpolates points
    for t in range(1,len(base_acc)):

        k = base_acc[t] - base_acc[t - 1]
        a = round(1/timehistory.timestepratio)

        for tt in range(a):

            new_acc.append(tt * timehistory.timestepratio * k + base_acc[t - 1])

    new_acc.append(base_acc[-1])        # Last point

    return new_acc