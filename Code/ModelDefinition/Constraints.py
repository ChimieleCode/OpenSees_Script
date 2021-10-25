import openseespy.opensees as ops

from ImportFromJson import frame

from BasicFunctions.NodeFunctions import nodeGrid

m = frame.m
n = frame.n

# ---------------------------------------------------------------------------------------------------------------------------
# Vincoli diaframma
# ---------------------------------------------------------------------------------------------------------------------------

def modelConstraints():
    for j in range(1, m + 1):        # j da 1 a m

        for i in range(1, n + 1):           # i da 1 a n

            ops.equalDOF(nodeGrid(0, j), nodeGrid(i, j), 1)
            # print(f'nodo master: {nodeGrid(0, j)} nodo slave: {nodeGrid(i, j)} DOF Fixed: {[1]} ') 