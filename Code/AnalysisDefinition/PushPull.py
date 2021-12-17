import openseespy.opensees as ops
import time

from ImportFromJson import frame,push_pull

from ControlNode import controlNode
from BasicFunctions.NodeFunctions import nodeGrid, nodeRigidBeam, nodeBeam
from ModelOptions import record_section_gaps


m = frame.m
n = frame.n

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Define Push-Pull Analysis
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

def runPushoverAnalysis():

    # Setto i recorders
    base_nodes = []
    storey_nodes = []

    for i in range (n + 1):           # Scrivo a quali nodi devo settare un recorder per la base

        base_nodes.append(nodeGrid(i, 0))

    
    for j in range (m + 1):           # Scrivo a quali nodi devo settare i recorder al piano

        storey_nodes.append(nodeGrid(0, j))


    # Reazione alla base
    ops.recorder('Node', '-file', 'Output\Pushover\Pushover_Base_Reactions.out', '-time', '-node', *base_nodes, '-dof', 1, 'reaction')
    # Spostamento del nodo di Controllo
    ops.recorder('Node', '-file', 'Output\Pushover\Pushover_Control_Disp.out', '-time', '-node', controlNode(), '-dof', 1, 'disp')
    # Spostamenti di piano
    ops.recorder('Node', '-file', 'Output\Pushover\Pushover_Storey_Disp.out', '-time', '-node', *storey_nodes, '-dof', 1, 'disp')

    if record_section_gaps:

        gap_nodes = []

        for j in range (1, m + 1):           # Scrivo a quali nodi devo settare i recorder al piano eccetto Pian Terreno

            gap_nodes.append(nodeRigidBeam(1, j, 0))
            gap_nodes.append(nodeBeam(1, j, 0))

        # Apertura Gap prima verticale
        ops.recorder('Node', '-file', 'Output\Pushover\Pushover_Storey_Gaps.out', '-time', '-node', *gap_nodes, '-dof', 3, 'disp')

    # ---------------------------------------------------------------------------------------------------------------------------
    # Inizio la definizione della prima Push
    # ---------------------------------------------------------------------------------------------------------------------------

    print(f'-o-o-o- Analisi Push-Pull 1/{len(push_pull.points)} -o-o-o-')

    # Parte il cronometro
    tStart = round(time.time() * 1000)

    # Definisco i Parametri 
    direzione = push_pull.points[0]/abs(push_pull.points[0])
    spostamento = push_pull.points[0]
    step = direzione * push_pull.step
    total_steps = round(spostamento/step)

    # ---------------------------------------------------------------------------------------------------------------------------
    # Definisco il Pattern di spinta
    # ---------------------------------------------------------------------------------------------------------------------------

    ops.pattern('Plain', 1, 1)

    for j in range(m):          # j da 0 a m - 1

        try:

            ops.load(nodeGrid(0, j + 1), direzione * push_pull.pattern[j], 0., 0.)  # Applico la forza j al piano j + 1 poiché salto il piano 0

        except:

            print('Errore: Il numero di forze del pattern differisce dal numero di piani fuori terra')

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

    print(f'-o-o-o- Analisi conclusa 1/{len(push_pull.points)} dopo {totalTime} sec -o-o-o- ')

    # ---------------------------------------------------------------------------------------------------------------------------
    # Punti successivi
    # ---------------------------------------------------------------------------------------------------------------------------

    if len(push_pull.points) > 1:

        for v in range(1,len(push_pull.points)):

            print(f'-o-o-o- Analisi Push-Pull {v + 1}/{len(push_pull.points)} -o-o-o-')

            # Parte il cronometro
            tStart = round(time.time() * 1000)

            # Definisco i Parametri 
            try:

                direzione = abs(push_pull.points[v] - push_pull.points[v - 1]) / (push_pull.points[v] - push_pull.points[v - 1])
                spostamento = push_pull.points[v] - push_pull.points[v - 1]
                step = direzione * push_pull.step
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

            print(f'-o-o-o- Analisi conclusa {v + 1}/{len(push_pull.points)} dopo {totalTime} sec -o-o-o- ')


    ops.wipeAnalysis()
    ops.remove('recorders')
    ops.reset()
