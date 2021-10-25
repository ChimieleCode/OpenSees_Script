import openseespy.opensees as ops

from ImportFromJson import frame

from BasicFunctions.NodeFunctions import nodeGrid

m = frame.m
n = frame.n

# ---------------------------------------------------------------------------------------------------------------------------
# Definisco i restraint
# ---------------------------------------------------------------------------------------------------------------------------

def modelRestraints():
    
    for i in range(n + 1):          # i da 0 a n

        ops.fix(nodeGrid(i, 0), 1, 1, 1)
        # print(f'nodo: {nodeGrid(i, 0)} DOF Fixed: {[1, 1, 1]} ') 