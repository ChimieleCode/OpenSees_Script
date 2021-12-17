import openseespy.opensees as ops
import time
import math

from ImportFromJson import frame
from ModelOptions import compute_spectral_response, compute_section_gaps_evnelopes

from ControlNode import controlNode
from BasicFunctions.NodeFunctions import nodeGrid, nodeRigidBeam, nodeBeam, nodeBase
from BasicFunctions.SpectralAcceleration import spectralAcceleration

m = frame.m
n = frame.n

spectral_response = []

def runTimeHistory (time_histories = [], structure_periods = []):

    i = 1

    for time_history in time_histories:

        print(f'-o-o-o- Analysis TH {time_history.id} -o-o-o-')

        base_nodes = []
        storey_nodes = []

        for i in range (n + 1):           # Scrivo a quali nodi devo settare un recorder per la base

            base_nodes.append(nodeGrid(i, 0))


        for j in range (m + 1):           # Scrivo a quali nodi devo settare i recorder al piano

            storey_nodes.append(nodeGrid(0, j))


        # Reazioni alla base
        ops.recorder('Node', '-file', f'Output\TimeHistory\TimeHistory_Base_Reactions.{time_history.id}_{time_history.sf}.out', '-time', '-node', *base_nodes, '-dof', 1, 'reaction')
        # Spostamenti di piano
        ops.recorder('Node', '-file', f'Output\TimeHistory\TimeHistory_Storey_Displacement.{time_history.id}_{time_history.sf}.out', '-time', '-node', *storey_nodes, '-dof', 1, 'disp')
        # Accelerazione di piano
        ops.recorder('Node', '-file', f'Output\TimeHistory\TimeHistory_Storey_Acceleration.{time_history.id}_{time_history.sf}.out', '-time', '-node', *storey_nodes, '-dof', 1, 'accel')
        # Velocità di piano
        ops.recorder('Node', '-file', f'Output\TimeHistory\TimeHistory_Storey_Velocity.{time_history.id}_{time_history.sf}.out', '-time', '-node', *storey_nodes, '-dof', 1, 'vel')
        # Spostamento nodo di controllo
        ops.recorder('Node', '-file', f'Output\TimeHistory\TimeHistory_ControlNode_Displacement.{time_history.id}_{time_history.sf}.out', '-time', '-node', controlNode(), '-dof', 1, 'disp')


        if compute_section_gaps_evnelopes:

            gap_nodes = [nodeGrid(0,0), nodeBase(0), nodeGrid(1,0), nodeBase(1)]

            for j in range (1, m + 1):           # Scrivo a quali nodi devo settare i recorder al piano eccetto Pian Terreno

                gap_nodes.append(nodeRigidBeam(1, j, 0))
                gap_nodes.append(nodeBeam(1, j, 0))

                gap_nodes.append(nodeRigidBeam(1, j, 1))
                gap_nodes.append(nodeBeam(1, j, 1))


            # Apertura Gap prima verticale
            ops.recorder('Node', '-file', f'Output\TimeHistory\TimeHistory_Section_Gaps.{time_history.id}_{time_history.sf}.out', '-time', '-node', *gap_nodes, '-dof', 3, 'disp')

            # print(gap_nodes)



        # Definisco i parametri della matrice di Damping

        T1 = structure_periods[0]

        try:

            T2 = structure_periods[1]

        except: # Caso di SDOF

            T2 = structure_periods[0] * 0.25

        omega1 = 2 * math.pi / T1
        omega2 = 2 * math.pi / T2
        aR = 2 * (omega1 * omega2 * (omega2 * frame.damping - omega1 * frame.damping)) / (omega2**2 - omega1**2)
        bR = 2 * (omega2 * frame.damping - omega1 * frame.damping) / (omega2**2 - omega1**2)

        # Calcolo accelerazione spettrale SDOF di primo Modo
        if compute_spectral_response:

            Sa = spectralAcceleration(time_history = time_history, structure_period = structure_periods[0])

            print(f'Sa: {Sa}')

            spectral_response.append([time_history.id, Sa])

        # Parametri TH
        dt = time_history.dt
        TH_steps = round((time_history.duration + 10 * structure_periods[0]) / dt)

        ops.timeSeries('Path', time_history.id + 1, '-dt', dt, '-filePath', f'acc_{time_history.id}.txt', '-factor', time_history.sf)

        # Parametri di Analisi

        tol = 0.000001
        maxIter = 5000

        ops.test('NormDispIncr', tol, maxIter, 0, 0)
        ops.pattern('UniformExcitation', time_history.id + 1, 1, '-accel', time_history.id + 1)
        ops.constraints('Plain')
        ops.integrator('Newmark', 0.5, 0.25)
        ops.rayleigh(aR, bR, 0., 0.)
        ops.algorithm('NewtonLineSearch', True, False, False, False, 0.8, 100, 0.1, 1)
        # ops.algorithm('RaphsonNewton')
        ops.numberer('RCM')
        ops.system('BandGen')
        ops.analysis('Transient')

        # Lacio e monitoro
        success = True

        t = 0 

        finalt = ops.getTime() + TH_steps * dt
        tStart = round(time.time() * 1000)

        dt_analysis = dt * time_history.timestepratio  # Un decimo della discretizzazione della TH

        while (success and t <= finalt):

            analysis_status = ops.analyze(1, dt_analysis)
            success = (analysis_status == 0)

            t = ops.getTime()

        
        tStop = round(time.time() * 1000)
        timeSeconds = round((tStop - tStart) / 1000)
        timeMinutes = math.floor(timeSeconds / 60)
        timeHours = math.floor(timeSeconds / 3600)
        timeMinutes = round(timeMinutes - timeHours * 60)
        timeSeconds = round(timeSeconds - timeHours * 3600 - timeMinutes * 60)

        if success:

            print(f'-o-o-o- Analisi TH terminata {time_history.id} in {timeHours}:{timeMinutes}:{timeSeconds} -o-o-o-')

        else:

            print(f'-o-o-o- Analisi TH fallita {time_history.id} in {timeHours}:{timeMinutes}:{timeSeconds} -o-o-o-')


        ops.wipeAnalysis()
        ops.remove('recorders')
        ops.remove('loadPattern', time_history.id + 1)
        ops.reset()
        i += 1
