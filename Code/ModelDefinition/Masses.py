import openseespy.opensees as ops

from ImportFromJson import frame

from BasicFunctions.NodeFunctions import nodeGrid

m = frame.m
n = frame.n

# ---------------------------------------------------------------------------------------------------------------------------
# Definisco le masse dei nodi
# ---------------------------------------------------------------------------------------------------------------------------

def modelAssignMasses():

    try:

        for j in range(1, m + 1):        # j da 1 a m

            for i in range(n + 1):           # i da 0 a n

                if i == 0 or i == n:

                    ops.mass(nodeGrid(i, j), frame.mass[j]/(2*n*frame.r), 0, 0)
                    # print(f'nodo: {nodeGrid(i, j)} Mass: {frame.mass[j]/(2*n*frame.r)}ton')

                else:

                    ops.mass(nodeGrid(i, j), frame.mass[j]/(n*frame.r), 0, 0)
                    # print(f'nodo: {nodeGrid(i, j)} Mass: {frame.mass[j]/(n*frame.r)}ton')

    except:

        print('Errore: il numero di masse di piano definite non corrisponde al numero di piani')