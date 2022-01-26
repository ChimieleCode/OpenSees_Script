from os import listdir, write
from numpy.lib.function_base import disp
import openseespy.opensees as ops
import time
import csv
import math
import numpy as np
from ModelOptions import field_factor
from PostProcessing.Damping import computeDamping
from ModelBuilder import buildModel
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------------------------------------------------------
# Carico gli Spettri
# ---------------------------------------------------------------------------------------------------------------------------
dont_iterate = ['SLD']
pushover_step = 0.001
tollerance = 0.002
g = 9.81

spectras = {}
cases = []

with open('Input\Spectras.csv') as csvfile:

    data = csv.reader(csvfile)

    for i, row in enumerate(data):

        array = []

        # Solo se mi trovo su riga pari definisco nuovo dizionario
        if (i % 2) == 0:

            spectra = {}
    

        for j, value in enumerate(row):

            # Il primo valore è l'indice
            if j == 0:

                index = value

            elif value == '':

                break

            else:

                array.append(float(value))

            # scrivo nel dizionario nestato
            if (i % 2) == 0:

                spectra['T'] = np.array(array)

            else:

                spectra['Sa'] = np.array(array)


        # Solo se mi trovo su riga dispari salvo i dati
        if (i % 2) == 1:

            spectras[index] = spectra
            cases.append(index)

# Calcolo gli spettri in spostamento
for case in cases:

    spectras[case]['Sd'] = spectras[case]['Sa'] * g * spectras[case]['T']**2 / (4 * math.pi**2)
    

# ---------------------------------------------------------------------------------------------------------------------------
# Inizio la definizione della prima Push
# ---------------------------------------------------------------------------------------------------------------------------

from ImportFromJson import frame

from ControlNode import controlNode
from BasicFunctions.NodeFunctions import nodeGrid
from BasicFunctions.InelasticShape import inelasticShape, getEffectiveMass
from Classes.PushPullAnalysis import PushPullAnalysis

m = frame.m
n = frame.n

first_pushover = PushPullAnalysis(points = [0.7], step = pushover_step, pattern = inelasticShape(frame))

# Setto i recorders
base_nodes = []

for i in range (n + 1):           # Scrivo a quali nodi devo settare un recorder per la base

    base_nodes.append(nodeGrid(i, 0))


# Reazione alla base
ops.recorder('Node', '-file', 'Output\PerformancePoint\Base_Reactions.out', '-time', '-node', *base_nodes, '-dof', 1, 'reaction')
# Spostamento del nodo di Controllo
ops.recorder('Node', '-file', 'Output\PerformancePoint\Control_Disp.out', '-time', '-node', controlNode(), '-dof', 1, 'disp')

print(f'-o-o-o- Performance Point: Prima Pushover -o-o-o-')

# Parte il cronometro
tStart = round(time.time() * 1000)

# Definisco i Parametri 
direzione = first_pushover.points[0]/abs(first_pushover.points[0])
spostamento = first_pushover.points[0]
step = direzione * first_pushover.step
total_steps = round(spostamento/step)

# Definisco il pattern di spinta
ops.pattern('Plain', 1, 1)

for j in range(m):          # j da 0 a m - 1

    try:

        ops.load(nodeGrid(0, j + 1), direzione * first_pushover.pattern[j], 0., 0.)  # Applico la forza j al piano j + 1 poiché salto il piano 0

    except:

        print('Errore: Il numero di forze del pattern differisce dal numero di piani fuori terra')

# Opzioni di analisi
ops.constraints('Transformation')
ops.numberer('RCM')
ops.system('BandGen')
ops.test('NormDispIncr', 0.000001, 100)
ops.algorithm('NewtonLineSearch', True, False, False, False, 0.8, 1000, 0.1, 10)
ops.integrator('DisplacementControl', controlNode(), 1, step)
ops.analysis('Static')

# Mando l'analisi
ops.record()
ops.analyze(total_steps)

# Info sulle Performance
tStop = round(time.time() * 1000)
totalTime = (tStop - tStart)/1000

print(f'-o-o-o- Analisi conclusa Prima Pushover dopo {totalTime} sec -o-o-o- ')

ops.remove('recorders')
ops.reset()
ops.wipeAnalysis()
ops.wipe()

# ---------------------------------------------------------------------------------------------------------------------------
# Leggo la curva
# ---------------------------------------------------------------------------------------------------------------------------
pushover_curve = {
    'Base Reactions'    : [],
    'Displacements'     : []
}

with open('Output\PerformancePoint\Base_Reactions.out') as csvfile: 

    data = csv.reader(csvfile, delimiter=' ')

    for row in data:

        base_reaction = 0

        for i, value in enumerate(row):
            
            if i == 0:

                continue

            else:

                base_reaction += float(row[i])

        pushover_curve['Base Reactions'].append(-base_reaction)


with open('Output\PerformancePoint\Control_Disp.out', mode = 'r') as csvfile: 

    data = csv.reader(csvfile, delimiter=' ')

    for row in data:

        pushover_curve['Displacements'].append(float(row[1]))

effective_mass = getEffectiveMass(frame)

pushover_curve['Base Reactions'] = np.array(pushover_curve['Base Reactions'])
pushover_curve['Displacements'] = np.array(pushover_curve['Displacements'])
pushover_curve['Accelerations'] = pushover_curve['Base Reactions'] / (effective_mass/frame.r * g)


performance_points = {}

for case in cases:

    from Performance.Functions import intersection

    displacement, acceleration = intersection(
        pushover_curve['Displacements'], 
        pushover_curve['Accelerations'], 
        spectras[case]['Sd'], 
        spectras[case]['Sa']
        )

    performance_points[case] = {
        'Sd'    :   displacement,
        'Vb'    :   acceleration * effective_mass * g,
        'Sa'    :   acceleration,
        'eta'   :   1
    }

# ---------------------------------------------------------------------------------------------------------------------------
# ITER
# ---------------------------------------------------------------------------------------------------------------------------

for removal in dont_iterate:

    cases.remove(removal)

for case in cases:

    residual = 1

    iteration = 1

    while residual > tollerance and iteration <= 20:

        if iteration == 1:

            performance_points[case]['Sd'] = performance_points[case]['Sd'] * 0.6
            

        cycle_disp = float(performance_points[case]['Sd'])

        buildModel()

        # Definisco il pattern di spinta
        ops.pattern('Plain', 1, 1)

        for j in range(m):          # j da 0 a m - 1

            try:

                ops.load(nodeGrid(0, j + 1), direzione * first_pushover.pattern[j], 0., 0.)  # Applico la forza j al piano j + 1 poiché salto il piano 0

            except:

                print('Errore: Il numero di forze del pattern differisce dal numero di piani fuori terra')


        push_pull_ciclica = PushPullAnalysis(points = [cycle_disp, -cycle_disp, cycle_disp], step = pushover_step, pattern = inelasticShape(frame))

        # Reazione alla base
        ops.recorder('Node', '-file', 'Output\Pushover\Pushover_Base_Reactions.out', '-time', '-node', *base_nodes, '-dof', 1, 'reaction')
        # Spostamento del nodo di Controllo
        ops.recorder('Node', '-file', 'Output\Pushover\Pushover_Control_Disp.out', '-time', '-node', controlNode(), '-dof', 1, 'disp')

        print(f'-o-o-o- Performing PushPull iter:{iteration} -o-o-o-')

        # Parte il cronometro
        tStart = round(time.time() * 1000)

        # Definisco i Parametri 
        direzione = push_pull_ciclica.points[0]/abs(push_pull_ciclica.points[0])
        spostamento = push_pull_ciclica.points[0]
        step = direzione * push_pull_ciclica.step
        total_steps = round(spostamento/step)

        # ---------------------------------------------------------------------------------------------------------------------------
        # Opzioni di analisi
        # ---------------------------------------------------------------------------------------------------------------------------

        ops.constraints('Transformation')
        ops.numberer('RCM')
        ops.system('BandGen')
        ops.test('NormDispIncr', 0.000001, 100)
        ops.algorithm('NewtonLineSearch', True, False, False, False, 0.8, 1000, 0.1, 10)
        ops.integrator('DisplacementControl', controlNode(), 1, step)
        ops.analysis('Static')

        # ---------------------------------------------------------------------------------------------------------------------------
        # Mando l'analisi
        # ---------------------------------------------------------------------------------------------------------------------------
        ops.record()
        ops.analyze(total_steps)

        # Info sulle Performance
        tStop = round(time.time() * 1000)
        totalTime = (tStop - tStart)/1000

        print(f'-o-o-o- Analisi conclusa 1/{len(push_pull_ciclica.points)} dopo {totalTime} sec -o-o-o- ')

        # ---------------------------------------------------------------------------------------------------------------------------
        # Punti successivi
        # ---------------------------------------------------------------------------------------------------------------------------

        if len(push_pull_ciclica.points) > 1:

            for v in range(1,len(push_pull_ciclica.points)):

                print(f'-o-o-o- Analisi Push-Pull {v + 1}/{len(push_pull_ciclica.points)} -o-o-o-')

                # Parte il cronometro
                tStart = round(time.time() * 1000)

                # Definisco i Parametri 
                try:

                    direzione = abs(push_pull_ciclica.points[v] - push_pull_ciclica.points[v - 1]) / (push_pull_ciclica.points[v] - push_pull_ciclica.points[v - 1])
                    spostamento = push_pull_ciclica.points[v] - push_pull_ciclica.points[v - 1]
                    step = direzione * push_pull_ciclica.step
                    total_steps = round(spostamento/step)

                except:

                    print('Errore nella definizione dei punti: controllare che non ci siano punti successivi di egual spostamento')
                    break

                # Opzioni di Analisi
                ops.numberer('RCM')
                ops.system('BandGen')
                ops.test('NormDispIncr', 0.000001, 100)
                ops.algorithm('NewtonLineSearch', True, False, False, False, 0.8, 1000, 0.1, 10)
                ops.integrator('DisplacementControl', controlNode(), 1, step)
                ops.analysis('Static')

                # Mando l'analisi
                ops.record()
                ops.analyze(total_steps)

                # Info sulle Performance
                tStop = round(time.time() * 1000)
                totalTime = (tStop - tStart)/1000

                print(f'-o-o-o- Analisi conclusa {v + 1}/{len(push_pull_ciclica.points)} dopo {totalTime} sec -o-o-o- ')


        ops.remove('recorders')
        ops.reset()
        ops.wipeAnalysis()
        ops.wipe()
    
        # ---------------------------------------------------------------------------------------------------------------------------
        # Computa damping e riduci spettro
        # ---------------------------------------------------------------------------------------------------------------------------
            
        damping_points = computeDamping()

        damping = damping_points[0][1]

        old_eta = performance_points[case]['eta']
        performance_points[case]['eta'] = (7/(2 + 2 + damping * 100))**field_factor

        spectras[case]['Sd'] = spectras[case]['Sd'] * performance_points[case]['eta']/old_eta
        spectras[case]['Sa'] = spectras[case]['Sa'] * performance_points[case]['eta']/old_eta

        # ---------------------------------------------------------------------------------------------------------------------------
        # Nuova intersezione
        # ---------------------------------------------------------------------------------------------------------------------------
            
        displacement, acceleration = intersection(
            pushover_curve['Displacements'], 
            pushover_curve['Accelerations'], 
            spectras[case]['Sd'], 
            spectras[case]['Sa']
            )

        old_displacement = performance_points[case]['Sd']

        performance_points[case] = {
            'Sd'    :   displacement,
            'Vb'     :   acceleration * effective_mass * g,
            'Sa'    :   acceleration,
            'eta'   :   performance_points[case]['eta']
        }

        residual = abs(performance_points[case]['Sd'] - old_displacement)

        print(residual)

        iteration += 1

# ---------------------------------------------------------------------------------------------------------------------------
# Results to CSV
# ---------------------------------------------------------------------------------------------------------------------------

# Spettri
with open('Output\PerformancePoint\spectras.csv', 'w', newline = '') as csvfile:

    writer = csv.writer(csvfile)

    raw_data = []

    cases.insert(0,*dont_iterate)

    for case in cases:

        raw_data.append(spectras[case]['Sd'])
        raw_data.append(spectras[case]['Sa'])

    writer.writerows(zip(*raw_data))

# Pushover
with open('Output\PerformancePoint\pushover.csv', 'w', newline = '') as csvfile:

    writer = csv.writer(csvfile)

    raw_data = [pushover_curve['Displacements'], pushover_curve['Accelerations']]

    writer.writerows(zip(*raw_data))

# PP
with open('Output\PerformancePoint\performance_point.csv', 'w', newline = '') as csvfile:

    writer = csv.writer(csvfile)

    raw_data = []

    for case in cases:

        raw_data.append(
            [
                performance_points[case]['Sd'], 
                performance_points[case]['Sa'], 
                performance_points[case]['Vb'], 
                performance_points[case]['eta']
            ]
            )
        
    writer.writerows(zip(*raw_data))


# ---------------------------------------------------------------------------------------------------------------------------
# Graph
# ---------------------------------------------------------------------------------------------------------------------------

# Push
plt.plot(
    pushover_curve['Displacements'],
    pushover_curve['Accelerations'],
    label = 'Pushover',
    color = '0.5',
    linestyle = '-',
    linewidth = 1
    )

for case in cases:

    spectras[case]['Sd'] = spectras[case]['Sd'].tolist()
    spectras[case]['Sa'] = spectras[case]['Sa'].tolist()

    spectras[case]['Sd'].append(spectras[case]['Sd'][-1])
    spectras[case]['Sa'].append(0)

    plt.plot(
        spectras[case]['Sd'],
        spectras[case]['Sa'],
        label = case,
        color = '0.2',
        linestyle = '--',
        linewidth = 1
        )

    plt.plot(
        performance_points[case]['Sd'],
        performance_points[case]['Sa'],
        color = 'r',
        linestyle = '',
        marker = 'o',
        markersize = 4
    )

# Titoli Assi
plt.ylabel('Sa [g]')
plt.xlabel('Sd [m]')

 # Titolo Grafico
plt.title(f'Performance Points')

# Mostra Legenda e Griglia
plt.legend()

# Imposta i valori limite degli assi
plt.ylim(ymin = 0, ymax = 1)
plt.xlim(xmin = 0, xmax = 0.5)

plt.grid(
    True, 
    linestyle = '--'
    )

plt.savefig('Figures\Performance.png')

plt.clf()
