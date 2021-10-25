import openseespy.opensees as ops

from ImportFromJson import frame,beams,column
from ControlNode import on_Column,on_CCR_up,on_CCR_down,p,controlNode_override
from ModelOptions import rigid_factor,LinearTT

from BasicFunctions.NodeFunctions import nodeGrid,nodeRigidBeam,nodePanel,nodeBeam,nodeBase,nodeTopColumn,nodeColumn
from ControlNode import controlNode

m = frame.m
n = frame.n

# ---------------------------------------------------------------------------------------------------------------------------
# Elementi ElasticBeamColumn
# ---------------------------------------------------------------------------------------------------------------------------

def modelDefineElements():

    x = 0  # Variabile ausiliaria per la numerazione degli elementi, attualmente non vi è la necessità di avere formule, l'importante è che venga sempre incrementato ad ogni nuova definizione

    # COLONNE DI BASE
    for i in range(n + 1):          # i da 0 a n

        if (p == 0) and on_Column and i == 0: # Se il nodo di controllo giace su questo elemento, non definirlo

            continue

        else:

            if m == 1:

                ops.element('elasticBeamColumn', x, nodeBase(i), nodeTopColumn(i), column.area(), column.Emat, column.inertia(), LinearTT)
                # print(f'id: {x} nodo i: {nodeBase(i)} nodo j: {nodeTopColumn(i)} Element: Colonna') 
                x += 1

            else:

                ops.element('elasticBeamColumn', x, nodeBase(i), nodeColumn(i ,1, 0), column.area(), column.Emat, column.inertia(), LinearTT)
                # print(f'id: {x} nodo i: {nodeBase(i)} nodo j: {nodeColumn(i ,1, 0)} Element: Colonna') 
                x += 1

    # COLONNA PIANO j [solo per edifici di almeno 2 piani]
    if m > 1:

        for j in range(1, m):       # j da 1 a m - 1

            for i in range(n + 1):          # i da 0 a n

                if (p == j) and on_Column and i == 0: # Se il nodo di controllo giace su questo elemento, non definirlo

                    continue

                else:

                    if j == m - 1:

                        ops.element('elasticBeamColumn', x, nodeColumn(i ,j, 1), nodeTopColumn(i), column.area(), column.Emat, column.inertia(), LinearTT)
                        # print(f'id: {x} nodo i: {nodeColumn(i ,j, 1)} nodo j: {nodeTopColumn(i)} Element: Colonna')
                        x += 1

                    else:

                        ops.element('elasticBeamColumn', x, nodeColumn(i ,j, 1), nodeColumn(i ,j + 1, 0), column.area(), column.Emat, column.inertia(), LinearTT)
                        # print(f'id: {x} nodo i: {nodeColumn(i ,j, 1)} nodo j: {nodeColumn(i ,j + 1, 0)} Element: Colonna')
                        x += 1

    # TRAVE PIANO j CAMPATA i
    for j in range(1, m + 1):        # j da 1 a m

        for i in range(1, n + 1):           # i da 1 a n

            ops.element('elasticBeamColumn', x, nodeBeam(i ,j, 0), nodeBeam(i ,j, 1), beams[j].area(), beams[j].Emat, beams[j].inertia(), LinearTT)
            # print(f'id: {x} nodo i: {nodeBeam(i ,j, 0)} nodo j: {nodeBeam(i ,j, 1)} Element: Trave')
            x += 1

    # CONNESSIONE COLONNA RIGIDA SOTTO VERTICALE i PIANO j
    for j in range(1, m + 1):       # j da 1 a m

        for i in range(n + 1):          # i da 0 a n

            if on_CCR_down and i == 0: # Se il nodo di controllo giace su questo elemento, non definirlo

                continue

            else:

                if j == m:

                    ops.element('elasticBeamColumn', x, nodeTopColumn(i), nodeGrid(i, j), column.area(), column.Emat * rigid_factor, column.inertia(), LinearTT)
                    # print(f'id: {x} nodo i: {nodeTopColumn(i)} nodo j: {nodeGrid(i, j)} Element: CCR')
                    x += 1 

                else:

                    ops.element('elasticBeamColumn', x, nodeColumn(i ,j, 0), nodeGrid(i, j), column.area(), column.Emat * rigid_factor, column.inertia(), LinearTT)
                    # print(f'id: {x} nodo i: {nodeColumn(i ,j, 0)} nodo j: {nodeGrid(i, j)} Element: CCR')
                    x += 1 

    # CONNESSIONE COLONNA RIGIDA SOPRA VERTICALE i PIANO j
    for j in range(1, m):       # j da 1 a m - 1

        for i in range(n + 1):          # i da 0 a n

            if on_CCR_up and i == 0: # Se il nodo di controllo giace su questo elemento, non definirlo

                continue

            else:

                ops.element('elasticBeamColumn', x, nodeGrid(i, j), nodeColumn(i ,j, 1), column.area(), column.Emat * rigid_factor, column.inertia(), LinearTT)
                # print(f'id: {x} nodo i: {nodeGrid(i, j)} nodo j: {nodeColumn(i ,j, 1)} Element: CCR')
                x += 1 

    # CONNESSIONE TRAVE RIGIDA SX e DX PIANO j CAMPATA i
    for j in range(1, m + 1):        # j da 1 a m

        for i in range(1, n + 1):           # i da 1 a n

            ops.element('elasticBeamColumn', x, nodePanel(i - 1, j), nodeRigidBeam(i, j, 0), beams[j].area(), beams[j].Emat * rigid_factor, beams[j].inertia(), LinearTT)
            # print(f'id: {x} nodo i: {nodePanel(i - 1, j)} nodo j: {nodeRigidBeam(i, j, 0)} Element: CTR')
            x += 1

            ops.element('elasticBeamColumn', x, nodeRigidBeam(i, j, 1), nodePanel(i, j), beams[j].area(), beams[j].Emat * rigid_factor, beams[j].inertia(), LinearTT)
            # print(f'id: {x} nodo i: {nodeRigidBeam(i, j, 1)} nodo j: {nodePanel(i, j)} Element: CTR')
            x += 1

    # HANDLER DEL NODO DI CONTROLLO
    if not controlNode_override:

        if on_Column:           # Costruisco la colonna in 2 pezzi con il nodo di controllo dentro

            if p == m - 1:

                ops.element('elasticBeamColumn', x, controlNode(), nodeTopColumn(0), column.area(), column.Emat, column.inertia(), LinearTT)
                # print(f'id: {x} nodo i: {controlNode()} nodo j: {nodeTopColumn(0)} Element: Column')
                x += 1

            else:

                ops.element('elasticBeamColumn', x, controlNode(), nodeColumn(0, p + 1, 0), column.area(), column.Emat, column.inertia(), LinearTT)
                # print(f'id: {x} nodo i: {controlNode()} nodo j: {nodeColumn(0, p + 1, 0)} Element: Column')
                x += 1


            if p == 0:

                ops.element('elasticBeamColumn', x, nodeBase(0), controlNode(), column.area(), column.Emat, column.inertia(), LinearTT)
                # print(f'id: {x} nodo i: {nodeBase(0)} nodo j: {controlNode()} Element: Column')
                x += 1

            else:

                ops.element('elasticBeamColumn', x, nodeColumn(0, p, 1), controlNode(), column.area(), column.Emat, column.inertia(), LinearTT)
                # print(f'id: {x} nodo i: {nodeColumn(0, p, 1)} nodo j: {controlNode()} Element: Column')
                x += 1


        elif on_CCR_down:       # Costruisco il link rigido in 2 pezzi con il nodo di controllo dentro

            ops.element('elasticBeamColumn', x, controlNode(), nodeGrid(0, p), column.area(), column.Emat * rigid_factor, column.inertia(), LinearTT)
            # print(f'id: {x} nodo i: {controlNode()} nodo j: {nodeGrid(0, p)} Element: CCR')
            x += 1

            if p == m:

                ops.element('elasticBeamColumn', x, nodeTopColumn(0), controlNode(), column.area(), column.Emat * rigid_factor, column.inertia(), LinearTT)
                # print(f'id: {x} nodo i: {nodeTopColumn(0)} nodo j: {controlNode()} Element: CCR')
                x += 1

            else:

                ops.element('elasticBeamColumn', x, nodeColumn(0, p, 0), controlNode(), column.area(), column.Emat * rigid_factor, column.inertia(), LinearTT)
                # print(f'id: {x} nodo i: {nodeColumn(0, p, 0)} nodo j: {controlNode()} Element: CCR')
                x += 1

        elif on_CCR_up:

            ops.element('elasticBeamColumn', x, controlNode(), nodeColumn(0, p, 1), column.area(), column.Emat * rigid_factor, column.inertia(), LinearTT)
            # print(f'id: {x} nodo i: {controlNode()} nodo j: {nodeColumn(0, p, 1)} Element: CCR')
            x += 1 

            ops.element('elasticBeamColumn', x, nodeGrid(0, p), controlNode(), column.area(), column.Emat * rigid_factor, column.inertia(), LinearTT)
            # print(f'id: {x} nodo i: {nodeGrid(0, p)} nodo j: {controlNode()} Element: CCR')
            x += 1

    return x