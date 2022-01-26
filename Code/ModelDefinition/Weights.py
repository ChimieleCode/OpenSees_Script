import openseespy.opensees as ops

from ImportFromJson import frame

from BasicFunctions.NodeFunctions import nodeGrid
from ImportFromJson import sections

m = frame.m
n = frame.n
axialUnit = sections[0].axialLoad/sum(frame.mass)
# print(axialUnit)

def modelAssignWeights():

    ops.pattern('Plain', 0, 1)

    try:

        for j in range(1, m + 1):        # j da 1 a m

            for i in range(n + 1):           # i da 0 a n

                if i == 0 or i == n:

                    ops.load(nodeGrid(i, j), 0., -frame.mass[j - 1]/2 * axialUnit, 0.)
                    # print(f'nodo: {nodeGrid(i, j)} Load: {-frame.mass[j - 1]/2 * axialUnit}kN')

                else:

                    ops.load(nodeGrid(i, j), 0., -frame.mass[j - 1] * axialUnit, 0.)
                    # print(f'nodo: {nodeGrid(i, j)} Load: {-frame.mass[j - 1] * axialUnit}kN')

    except:

        print('Errore: il numero di masse di piano definite non corrisponde al numero di piani')


    base_nodes = []

    for i in range (n + 1):           # Scrivo a quali nodi devo settare un recorder per la base

        base_nodes.append(nodeGrid(i, 0))

    ops.recorder('Node', '-file', 'Output\Vertical.out', '-time', '-node', *base_nodes, '-dof', 2, 'reaction')

    ops.constraints('Transformation')
    ops.numberer('RCM')
    ops.system('ProfileSPD')
    ops.test('NormDispIncr', 0.000001, 100)
    ops.algorithm('Newton')
    ops.integrator('LoadControl', 0.1)
    ops.analysis('Static')

    ops.record()
    ops.analyze(10)

    ops.setTime(0.)
    ops.loadConst()
    ops.wipeAnalysis()