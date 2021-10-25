import openseespy.opensees as ops

from ImportFromJson import frame,beams,column,G_joints
from ModelOptions import rigid_joints,rigid_stiffness

from BasicFunctions.MaterialFunctions import beamS,beamPT,columnS,columnN,jointLink,rigidLink
from BasicFunctions.NodeFunctions import nodeGrid,nodeRigidBeam,nodePanel,nodeBeam,nodeBase,nodeTopColumn,nodeColumn

m = frame.m
n = frame.n

# ---------------------------------------------------------------------------------------------------------------------------
# UniaxialMaterial per i link
# ---------------------------------------------------------------------------------------------------------------------------
def modelDefineLinks(x):

    # DEFINISCO LEGAME N COLONNA
    ops.uniaxialMaterial('ElasticMultiLinear', columnN(), '-strain', column.strain[0], column.strain[1], column.strain[2], column.strain[3], column.strain[4], column.strain[5], column.strain[6], '-stress', column.stress[0], column.stress[1], column.stress[2], column.stress[3], column.stress[4], column.stress[5], column.stress[6])
    # print(f'Material: {columnN()} Proprietà[strain,stress]: {[column.strain[0], column.strain[1], column.strain[2], column.strain[3], column.strain[4], column.strain[5], column.strain[6]], [column.stress[0], column.stress[1], column.stress[2], column.stress[3], column.stress[4], column.stress[5], column.stress[6]]}')

    # DEFINISCO LEGAME S COLONNA
    ops.uniaxialMaterial('Hardening', columnS(), column.E0, column.Fy, column.Hiso, column.Hkin)
    # print(f'Material: {columnS()} Proprietà[E0,Fy]: {column.E0, column.Fy}')

    # DEFINISCO LEGAMI PT TRAVI E S TRAVI
    for j in range(1, m + 1):       # j da 1 a m

        ops.uniaxialMaterial('ElasticMultiLinear', beamPT(j), '-strain', beams[j].strain[0], beams[j].strain[1], beams[j].strain[2], beams[j].strain[3], beams[j].strain[4], beams[j].strain[5], beams[j].strain[6], '-stress', beams[j].stress[0], beams[j].stress[1], beams[j].stress[2], beams[j].stress[3], beams[j].stress[4], beams[j].stress[5], beams[j].stress[6])
        # print(f'Material: {beamPT(j)} Proprietà[strain,stress]: {[beams[j].strain[0], beams[j].strain[1], beams[j].strain[2], beams[j].strain[3], beams[j].strain[4], beams[j].strain[5], beams[j].strain[6]], [beams[j].stress[0], beams[j].stress[1], beams[j].stress[2], beams[j].stress[3], beams[j].stress[4], beams[j].stress[5], beams[j].stress[6]]}')

        ops.uniaxialMaterial('Hardening', beamS(j), beams[j].E0, beams[j].Fy, beams[j].Hiso, beams[j].Hkin)
        # print(f'Material: {beamS(j)} Proprietà[E0,Fy]: {beams[j].E0, beams[j].Fy}')

    # DEFINIZIONE DEI LINK DEI NODI SE NON RIGIDI
    if not rigid_joints:
        for j in range(1, m + 1):            # j da 1 a m
            ops.uniaxialMaterial('Elastic', jointLink(j), (G_joints * column.h**2 * beams[j].h * frame.storey * (frame.span - column.h) * column.b) * 0.5 / (column.h * frame.storey * (frame.span - column.h) - frame.span * beams[j].h * column.h + column.b * frame.span * (frame.storey - beams[j].h) - frame.storey * column.h * column.b))
            print(f'Material: {jointLink(j)} Rigidezza: {(G_joints * column.h**2 * beams[j].h * frame.storey * (frame.span - column.h) * column.b) * 0.5 / (column.h * frame.storey * (frame.span - column.h) - frame.span * beams[j].h * column.h + column.b * frame.span * (frame.storey - beams[j].h) - frame.storey * column.h * column.b)}')
            

    # DEFINISCO IL LINK RIGIDO DA ASSEGNARE ALLA BASE PER 1 E 2
    ops.uniaxialMaterial('Elastic', rigidLink(), rigid_stiffness)
    # print(f'Material: {rigidLink()} Rigidezza: {rigid_stiffness}')

    # ---------------------------------------------------------------------------------------------------------------------------
    # Definisco i Link
    # ---------------------------------------------------------------------------------------------------------------------------

    # DEFINISCO I LINK DELLE COLONNE VERTICALI N e S
    for i in  range(n + 1):          # i da 0 a n

        ops.element('zeroLength', x, nodeGrid(i, 0), nodeBase(i), '-mat', columnN(), rigidLink(), rigidLink(), '-dir', 6, 1, 2)
        # print(f'id: {x} nodo i: {nodeGrid(i, 0)} nodo j: {nodeBase(i)} Material: {columnN()}')
        x += 1

        ops.element('zeroLength', x, nodeGrid(i, 0), nodeBase(i), '-mat', columnS(), rigidLink(), rigidLink(), '-dir', 6, 1, 2)
        # print(f'id: {x} nodo i: {nodeGrid(i, 0)} nodo j: {nodeBase(i)} Material: {columnS()}')
        x += 1

    # DEFINISCO I LINK DELLE TRAVI PT e S a DX e a SX
    for j in range(1, m + 1):        # j da 1 a m

        for i in range(1, n + 1):           # i da 1 a n

            ops.element('zeroLength', x, nodeRigidBeam(i, j, 0), nodeBeam(i, j, 0), '-mat', beamPT(j), rigidLink(), rigidLink(), '-dir', 6, 1, 2)     # PT SX
            # print(f'id: {x} nodo i: {nodeRigidBeam(i, j, 0)} nodo j: {nodeBeam(i, j, 0)} Material: {beamPT(j)}')
            x += 1

            ops.element('zeroLength', x, nodeRigidBeam(i, j, 0), nodeBeam(i, j, 0), '-mat', beamS(j), rigidLink(), rigidLink(), '-dir', 6, 1, 2)      # S  SX
            # print(f'id: {x} nodo i: {nodeRigidBeam(i, j, 0)} nodo j: {nodeBeam(i, j, 0)} Material: {beamS(j)}')
            x += 1 

            ops.element('zeroLength', x, nodeBeam(i, j, 1), nodeRigidBeam(i, j, 1), '-mat', beamPT(j), rigidLink(), rigidLink(), '-dir', 6, 1, 2)     # PT DX
            # print(f'id: {x} nodo i: {nodeBeam(i, j, 1)} nodo j: {nodeRigidBeam(i, j, 1)} Material: {beamPT(j)}')
            x += 1

            ops.element('zeroLength', x, nodeBeam(i, j, 1), nodeRigidBeam(i, j, 1), '-mat', beamS(j), rigidLink(), rigidLink(), '-dir', 6, 1, 2)      # S  DX
            # print(f'id: {x} nodo i: {nodeBeam(i, j, 1)} nodo j: {nodeRigidBeam(i, j, 1)} Material: {beamS(j)}')
            x += 1

    # LINK DEI NODI
    for j in range(1, m + 1):        # j da 1 a m

        for i in range(n + 1):           # i da 0 a n

            if rigid_joints:

                ops.element('zeroLength', x, nodeGrid(i, j), nodePanel(i, j), '-mat', rigidLink(), rigidLink(), rigidLink(), '-dir', 6, 1, 2)
                # print(f'id: {x} nodo i: {nodeGrid(i, j)} nodo j: {nodePanel(i, j)} Material: {rigidLink()}')
                x += 1

            else:
            
                ops.element('zeroLength', x, nodeGrid(i, j), nodePanel(i, j), '-mat', jointLink(j), rigidLink(), rigidLink(), '-dir', 6, 1, 2) 
                # print(f'id: {x} nodo i: {nodeGrid(i, j)} nodo j: {nodePanel(i, j)} Material: {jointLink(j)}')
                x += 1
