import openseespy.opensees as ops

from ImportFromJson import frame
from MomentoRotazione import beams,column
from ControlNode import controlNode_override

from BasicFunctions.NodeFunctions import nodeGrid,nodeColumn,nodeTopColumn,nodeBase,nodeBeam,nodePanel,nodeRigidBeam
from ControlNode import controlNode

m = frame.m
n = frame.n

# ---------------------------------------------------------------------------------------------------------------------------
# Definisco i nodi
# ---------------------------------------------------------------------------------------------------------------------------

def modelDefineNodes():

    for j in range(m + 1):          # j da 0 a m

        for i in range(n + 1):          # i da 0 a n

            ops.node(nodeGrid(i, j), i * frame.span, j * frame.storey)      # Nodo Griglia
            # print(f'nodo: {nodeGrid(i, j)} coordinate[x, y]: {[i * frame.span, j * frame.storey]} ')

    # NODI BASE E COLONNA TOP
    for i in range(n + 1):          # i da 0 a n

        ops.node(nodeBase(i), i * frame.span, 0)     # Nodo Base
        # print(f'nodo: {nodeBase(i)} coordinate[x, y]: {[i * frame.span, 0]} ')

        ops.node(nodeTopColumn(i), i * frame.span, m * frame.storey - beams[m].h / 2)     # Nodo Colonna Top
        # print(f'nodo: {nodeTopColumn(i)} coordinate[x, y]: {[i * frame.span, m * frame.storey - beams[m].h / 2]} ')

    # NODI PANNELLO
    for j in range(1, m + 1):       # j da 1 a m

        for i in range(n + 1):          # i da 0 a n

            ops.node(nodePanel(i, j), i * frame.span, j * frame.storey)     # Nodo Pannello
            # print(f'nodo: {nodePanel(i, j)} coordinate[x, y]: {[i * frame.span, j * frame.storey]} ')


    # NODI RIGID BEAM E BEAM
    for j in range(1, m + 1):        # j da 1 a m

        for i in range(1, n + 1):           # i da 1 a n

            ops.node(nodeRigidBeam(i, j, 0), (i - 1) * frame.span + column.h / 2, j * frame.storey)     # Nodo Rigid Beam Sx ( l = 0 )
            # print(f'nodo: {nodeRigidBeam(i, j, 0)} coordinate[x, y]: {[(i - 1) * frame.span + column.h / 2, j * frame.storey]} ')

            ops.node(nodeBeam(i, j, 0), (i - 1) * frame.span + column.h / 2, j * frame.storey)          # Nodo Beam Sx ( l = 0 )
            # print(f'nodo: {nodeBeam(i, j, 0)} coordinate[x, y]: {[(i - 1) * frame.span + column.h / 2, j * frame.storey]} ')

            ops.node(nodeRigidBeam(i, j, 1), i * frame.span - column.h / 2, j * frame.storey)           # Nodo Rigid Beam Sx ( l = 1 )
            # print(f'nodo: {nodeRigidBeam(i, j, 1)} coordinate[x, y]: {[i * frame.span - column.h / 2, j * frame.storey]} ')

            ops.node(nodeBeam(i, j, 1), i * frame.span - column.h / 2, j * frame.storey)                # Nodo Beam Sx ( l = 1 )
            # print(f'nodo: {nodeBeam(i, j, 1)} coordinate[x, y]: {[i * frame.span - column.h / 2, j * frame.storey]} ')

    # NODI COLUMN 
    for j in range(1, m):        # j da 1 a m - 1

        for i in range(n + 1):           # i da 0 a n

            ops.node(nodeColumn(i, j, 0), i * frame.span, j * frame.storey - beams[j].h / 2)               # Nodo Colonna Sotto ( l = 0 )
            #    print(f'nodo: {nodeColumn(i, j, 0)} coordinate[x, y]: {[i * frame.span, j * frame.storey - beams[j].h / 2]} ') 

            ops.node(nodeColumn(i, j, 1), i * frame.span, j * frame.storey + beams[j].h / 2)               # Nodo Colonna Sopra ( l = 0 )
            #    print(f'nodo: {nodeColumn(i, j, 1)} coordinate[x, y]: {[i * frame.span, j * frame.storey + beams[j].h / 2]} ') 

    # NODO DI CONTROLLO
    if not controlNode_override:

        ops.node(controlNode(), 0, frame.Heff)
        # print(f'nodo: {controlNode()} coordinate[x, y]: {[0, frame.Heff]} ') 