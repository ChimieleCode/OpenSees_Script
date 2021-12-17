import openseespy.opensees as ops

from ImportFromJson import frame
from MomentoRotazione import beams,column,edge_column
from ModelOptions import rigid_joints,rigid_stiffness,use_GM,steel_failure,tendon_failure,beta

from BasicFunctions.MaterialFunctions import beamS,beamPT,columnS,columnN,rigidLink,columnS_MinMax,beamS_MinMax,beamPT_MinMax,jointInternalLink,jointExternalLink
from BasicFunctions.NodeFunctions import nodeGrid,nodeRigidBeam,nodePanel,nodeBeam,nodeBase

m = frame.m
n = frame.n

# ---------------------------------------------------------------------------------------------------------------------------
# UniaxialMaterial per i link
# ---------------------------------------------------------------------------------------------------------------------------
def modelDefineLinks(x):

    # DEFINISCO LEGAME N COLONNA INTERNA

    ops.uniaxialMaterial(
        'ElasticMultiLinear',
        columnN(n + 1),                             # n + 1 assicura che non sia ne n ne 0, quindi è da intendersi come pilastro interno, se nonesiste tale pilastro, non verrà mai assegnato questo link
        '-strain', 
        *column.multilinearElasticLink.strain, 
        '-stress', 
        *column.multilinearElasticLink.stress
        )

    # DEFINISCO LEGAME N COLONNA BORDO

    ops.uniaxialMaterial(
        'ElasticMultiLinear',
        columnN(0),                             
        '-strain', 
        *edge_column.multilinearElasticLink.strain,
        '-stress', 
        *edge_column.multilinearElasticLink.stress
        )

    # print(f'Material: {columnN()} Proprietà[strain,stress]: {[column.strain[0], column.strain[1], column.strain[2], column.strain[3], column.strain[4], column.strain[5], column.strain[6]], [column.stress[0], column.stress[1], column.stress[2], column.stress[3], column.stress[4], column.stress[5], column.stress[6]]}')

    # DEFINISCO LEGAME S COLONNA [INTERNA, POI ESTERNA]

    if use_GM:

        ops.uniaxialMaterial(
            'Steel02', 
            columnS(n + 1), 
            column.GMLink.Fy, 
            column.GMLink.E0, 
            column.GMLink.b, 
            column.GMLink.r0,
            column.GMLink.cr1,
            column.GMLink.cr2,
            )

        ops.uniaxialMaterial(
            'Steel02', 
            columnS(0), 
            edge_column.GMLink.Fy, 
            edge_column.GMLink.E0, 
            edge_column.GMLink.b, 
            edge_column.GMLink.r0,
            edge_column.GMLink.cr1,
            edge_column.GMLink.cr2,
            )

        # CONSIDERANDO ROTTURE

        if steel_failure:

            ops.uniaxialMaterial(
                'MinMax',
                columnS_MinMax(n + 1),
                columnS(n + 1),
                '-min',
                -column.GMLink.strainLimit,
                '-max',
                column.GMLink.strainLimit
            )

            ops.uniaxialMaterial(
                'MinMax',
                columnS_MinMax(0),
                columnS(0),
                '-min',
                -edge_column.GMLink.strainLimit,
                '-max',
                edge_column.GMLink.strainLimit
            )


    else:

        ops.uniaxialMaterial(
            'Hardening', 
            columnS(n + 1), 
            column.kineticLink.E0, 
            column.kineticLink.Fy, 
            column.kineticLink.Hiso, 
            column.kineticLink.Hkin
            )

        ops.uniaxialMaterial(
            'Hardening', 
            columnS(0), 
            edge_column.kineticLink.E0, 
            edge_column.kineticLink.Fy, 
            edge_column.kineticLink.Hiso, 
            edge_column.kineticLink.Hkin
            )

        # CONSIDERANDO ROTTURE

        if steel_failure:

            ops.uniaxialMaterial(
                'MinMax',
                columnS_MinMax(n + 1),
                columnS(n + 1),
                '-min',
                -column.kineticLink.strainLimit,
                '-max',
                column.kineticLink.strainLimit
            )

            ops.uniaxialMaterial(
                'MinMax',
                columnS_MinMax(0),
                columnS(0),
                '-min',
                -edge_column.kineticLink.strainLimit,
                '-max',
                edge_column.kineticLink.strainLimit
            )
        
        # ops.uniaxialMaterial('MinMax', beamS_MinMax(j), beamS(j), '-min', -beams[j].kineticLink.strainLimit, '-max', beams[j].kineticLink.strainLimit)
        # print(f'Material: {columnS()} Proprietà[E0,Fy]: {column.E0, column.Fy}')

    # DEFINISCO LEGAMI PT TRAVI E S TRAVI

    for j in range(1, m + 1):       # j da 1 a m

        ops.uniaxialMaterial(
            'ElasticMultiLinear', 
            beamPT(j), 
            '-strain', 
            *beams[j].multilinearElasticLink.strain,
            '-stress', 
            *beams[j].multilinearElasticLink.stress
            )

        if tendon_failure:

            ops.uniaxialMaterial(
                'MinMax',
                beamPT_MinMax(j),
                beamPT(j),
                '-min',
                beams[j].multilinearElasticLink.stress[0],
                '-max',
                beams[j].multilinearElasticLink.stress[-1]
                )

        # print(f'Material: {beamPT(j)} Proprietà[strain,stress]: {[beams[j].strain[0], beams[j].strain[1], beams[j].strain[2], beams[j].strain[3], beams[j].strain[4], beams[j].strain[5], beams[j].strain[6]], [beams[j].stress[0], beams[j].stress[1], beams[j].stress[2], beams[j].stress[3], beams[j].stress[4], beams[j].stress[5], beams[j].stress[6]]}')
        
        if use_GM and beams[j].GMLink != None:

            ops.uniaxialMaterial(
                'Steel02', 
                beamS(j), 
                beams[j].GMLink.Fy, 
                beams[j].GMLink.E0, 
                beams[j].GMLink.b, 
                beams[j].GMLink.r0,
                beams[j].GMLink.cr1,
                beams[j].GMLink.cr2,
                )
                
            if steel_failure:

                ops.uniaxialMaterial(
                    'MinMax',
                    beamS_MinMax(j),
                    beamS(j),
                    '-min',
                    -beams[j].GMLink.strainLimit,
                    '-max',
                    beams[j].GMLink.strainLimit
                )


        elif beams[j].kineticLink != None:

            ops.uniaxialMaterial(
                'Hardening', 
                beamS(j), 
                beams[j].kineticLink.E0, 
                beams[j].kineticLink.Fy, 
                beams[j].kineticLink.Hiso, 
                beams[j].kineticLink.Hkin
                )
                
            if steel_failure:

                ops.uniaxialMaterial(
                    'MinMax',
                    beamS_MinMax(j),
                    beamS(j),
                    '-min',
                    -beams[j].kineticLink.strainLimit,
                    '-max',
                    beams[j].kineticLink.strainLimit
                    )

            # print(f'Material: {beamS(j)} Proprietà[E0,Fy]: {beams[j].E0, beams[j].Fy}')
        


    # DEFINIZIONE DEI LINK DEI NODI SE NON RIGIDI
    if not rigid_joints:
        
        for j in range(1, m + 1):            # j da 1 a m

            # Definisco i nodi esterni
            ops.uniaxialMaterial(
                'Elastic', 
                jointExternalLink(j), 
                (column.h * column.b * beams[j].h * column.timber.G) * 17/30 * (1 - column.h/frame.span)**-1
                )
            
            # Definisco i nodi interni
            ops.uniaxialMaterial(
                'Elastic', 
                jointInternalLink(j), 
                (column.h * column.b * beams[j].h * column.timber.G) * 17/30 * (1 - column.h/frame.span)**-1 * 2/(2 - beta)
                )

            # ops.uniaxialMaterial('Elastic', jointLink(j), (G_joints * column.h**2 * beams[j].h * frame.storey * (frame.span - column.h) * column.b) * 0.5 / (column.h * frame.storey * (frame.span - column.h) - frame.span * beams[j].h * column.h + column.b * frame.span * (frame.storey - beams[j].h) - frame.storey * column.h * column.b))
            # print(f'Material: {jointLink(j)} Rigidezza: {(G_joints * column.h**2 * beams[j].h * frame.storey * (frame.span - column.h) * column.b) * 0.5 / (column.h * frame.storey * (frame.span - column.h) - frame.span * beams[j].h * column.h + column.b * frame.span * (frame.storey - beams[j].h) - frame.storey * column.h * column.b)}')
            

    # DEFINISCO IL LINK RIGIDO DA ASSEGNARE ALLA BASE PER 1 E 2

    ops.uniaxialMaterial('Elastic', rigidLink(), rigid_stiffness)

    # print(f'Material: {rigidLink()} Rigidezza: {rigid_stiffness}')

    # ---------------------------------------------------------------------------------------------------------------------------
    # Definisco i Link
    # ---------------------------------------------------------------------------------------------------------------------------

    # DEFINISCO I LINK DELLE COLONNE VERTICALI N e S
    for i in  range(n + 1):          # i da 0 a n
    
        if steel_failure:

            tagS = columnS_MinMax(i)

        else:

            tagS = columnS(i)


        ops.element('zeroLength', x, nodeGrid(i, 0), nodeBase(i), '-mat', columnN(i), rigidLink(), rigidLink(), '-dir', 6, 1, 2)
        # print(f'id: {x} nodo i: {nodeGrid(i, 0)} nodo j: {nodeBase(i)} Material: {columnN()}')
        x += 1

        ops.element('zeroLength', x, nodeGrid(i, 0), nodeBase(i), '-mat', tagS, rigidLink(), rigidLink(), '-dir', 6, 1, 2)
        # print(f'id: {x} nodo i: {nodeGrid(i, 0)} nodo j: {nodeBase(i)} Material: {columnS()}')
        x += 1

    # DEFINISCO I LINK DELLE TRAVI PT e S a DX e a SX
    for j in range(1, m + 1):        # j da 1 a m

        if steel_failure:

            tagS = beamS_MinMax(j)

        else:

            tagS = beamS(j)

            
        if tendon_failure:

            tagN = beamPT_MinMax(j)

        else:

            tagN = beamPT(j)


        for i in range(1, n + 1):           # i da 1 a n

            ops.element('zeroLength', x, nodeRigidBeam(i, j, 0), nodeBeam(i, j, 0), '-mat', tagN, rigidLink(), rigidLink(), '-dir', 6, 1, 2)     # PT SX
            # print(f'id: {x} nodo i: {nodeRigidBeam(i, j, 0)} nodo j: {nodeBeam(i, j, 0)} Material: {beamPT(j)}')
            x += 1

            ops.element('zeroLength', x, nodeBeam(i, j, 1), nodeRigidBeam(i, j, 1), '-mat', tagN, rigidLink(), rigidLink(), '-dir', 6, 1, 2)     # PT DX
            # print(f'id: {x} nodo i: {nodeBeam(i, j, 1)} nodo j: {nodeRigidBeam(i, j, 1)} Material: {beamPT(j)}')
            x += 1

            try:

                ops.element('zeroLength', x, nodeRigidBeam(i, j, 0), nodeBeam(i, j, 0), '-mat', tagS, rigidLink(), rigidLink(), '-dir', 6, 1, 2)      # S  SX
                # print(f'id: {x} nodo i: {nodeRigidBeam(i, j, 0)} nodo j: {nodeBeam(i, j, 0)} Material: {beamS(j)}')
                x += 1

                ops.element('zeroLength', x, nodeBeam(i, j, 1), nodeRigidBeam(i, j, 1), '-mat', tagS, rigidLink(), rigidLink(), '-dir', 6, 1, 2)      # S  DX
                # print(f'id: {x} nodo i: {nodeBeam(i, j, 1)} nodo j: {nodeRigidBeam(i, j, 1)} Material: {beamS(j)}')
                x += 1

            except:

                continue
            

    # LINK DEI NODI
    for j in range(1, m + 1):        # j da 1 a m

        for i in range(n + 1):           # i da 0 a n

            if rigid_joints:

                # Modello i Joint come Rigidi
                ops.element('zeroLength', x, nodeGrid(i, j), nodePanel(i, j), '-mat', rigidLink(), rigidLink(), rigidLink(), '-dir', 6, 1, 2)
                # print(f'id: {x} nodo i: {nodeGrid(i, j)} nodo j: {nodePanel(i, j)} Material: {rigidLink()}')
                x += 1

            else:

                if i == 0 or i == n:
                    
                    # Joint esterni
                    ops.element('zeroLength', x, nodeGrid(i, j), nodePanel(i, j), '-mat', jointExternalLink(j), rigidLink(), rigidLink(), '-dir', 6, 1, 2) 
                    # print(f'id: {x} nodo i: {nodeGrid(i, j)} nodo j: {nodePanel(i, j)} Material: {jointLink(j)}')
                    x += 1

                else:
                    
                    # Joint interni
                    ops.element('zeroLength', x, nodeGrid(i, j), nodePanel(i, j), '-mat', jointInternalLink(j), rigidLink(), rigidLink(), '-dir', 6, 1, 2) 
                    # print(f'id: {x} nodo i: {nodeGrid(i, j)} nodo j: {nodePanel(i, j)} Material: {jointLink(j)}')
                    x += 1
