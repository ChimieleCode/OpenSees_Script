import openseespy.opensees as ops
import math

from ImportFromJson import frame

m = frame.m
n = frame.n

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Define Modal Analysis
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

def runModalAnalysis():

    ops.printModel('-file','Output\Model.out')

    ops.recorder('Node', '-file', 'Output\Modal\ModalAnalysis_Node_EigenVectors_EigenVectorsVec1.out', '-time', '-node', 3, '-dof', 1, 'eigen1')
    ops.recorder('Node', '-file', 'Output\Modal\ModalAnalysis_Node_EigenVectors_EigenVectorsVec2.out', '-time', '-node', 3, '-dof', 1, 'eigen2')

    print('-o-o-o- Modal Analysis Started -o-o-o-' )

    # Analysis Options
    ops.constraints('Transformation')
    ops.numberer('RCM')
    ops.system('BandGen')
    ops.test('NormDispIncr', 10**-6, 25, 0, 1)
    ops.algorithm('Newton')
    ops.integrator('Newmark', 0.5, 0.25)
    ops.analysis('Transient')

    # Analyze and Record
    eigen_lambdas = []
    eigen_periods = []

    eigen_lambdas = ops.eigen('-fullGenLapack', m)

    for eigen_lambda in eigen_lambdas:

        omega = math.sqrt(eigen_lambda)
        period = 2 * math.pi / omega

        eigen_periods.append(period)

    # if m == 1:          # Se ho 1 solo piano ho un solo modo

    #     eigen_lambdas = ops.eigen('-fullGenLapack',1)
    #     omega = math.sqrt(eigen_lambdas[0])
    #     period = 2 * math.pi / omega

    #     eigen_periods.append(period)

    # else:
        
    #     eigen_lambdas = ops.eigen('-fullGenLapack',2)

    #     for eigen_lambda in eigen_lambdas:

    #         omega = math.sqrt(eigen_lambda)
    #         period = 2 * math.pi / omega

    #         eigen_periods.append(period)

    ops.record()

    ops.wipeAnalysis()

    print('-o-o-o- Modal Analysis Completed -o-o-o-' )
    print(eigen_periods)

    return eigen_periods