from ImportFromJson import frame,beams
from ModelOptions import tolleranza_di_sovrapposizione

from BasicFunctions.NodeFunctions import nodeGrid,nodeTopColumn,nodeColumn

# USEFULL CONSTANTS
n = frame.n
m = frame.m

# ---------------------------------------------------------------------------------------------------------------------------
# Verifica Sovrapposizione Nodo di Cotrollo
# ---------------------------------------------------------------------------------------------------------------------------

controlNode_override = False        # True --> il nodo di controllo è sovrapposto ad un esistente
controlNode_id = 0

if frame.Heff % frame.storey <= tolleranza_di_sovrapposizione:          # Il punto di controllo è sovrapposto ad un nodo di griglia?

    controlNode_id = nodeGrid(0, round(frame.Heff/frame.storey))
    controlNode_override = True

else:

    for j in range(1, m + 1):

        if abs(frame.Heff - j*frame.storey + beams[j].h/2) <= tolleranza_di_sovrapposizione:         # Il punto di controllo è sovrapposto ad un nodo di colonna?

            if j == m:

                controlNode_id = nodeTopColumn(0)
                controlNode_override = True

            else:

                controlNode_id = nodeColumn(0, j, 0)
                controlNode_override = True

            break

        elif abs(frame.Heff - j*frame.storey - beams[j].h/2) <= tolleranza_di_sovrapposizione:

            controlNode_id = nodeColumn(0, j, 1)
            controlNode_override = True

            break

# ---------------------------------------------------------------------------------------------------------------------------
# Definisce ID del nodo di controllo (se sovrapposto restituisce l'ID del nodo esistente)
# ---------------------------------------------------------------------------------------------------------------------------

def controlNode():

    if controlNode_override:

        return controlNode_id

    else:

        return 4*m*(2*n + 1) + (n + 1)

# ---------------------------------------------------------------------------------------------------------------------------
# Verifica Piano e Elemento in cui il Nodo di Controllo è contenuto
# ---------------------------------------------------------------------------------------------------------------------------

p = -1
on_CCR_up = False
on_CCR_down = False
on_Column = False

if not controlNode_override:
    # Cerco il piano a cui si trova il nodo
    j = 0

    while j <= m - 1:

        if frame.Heff >= max(0, j*frame.storey - beams[j].h/2) and frame.Heff <= min(m*frame.storey, (j + 1)*frame.storey - beams[j + 1].h/2):

            p = j

            break

        else:

            j += 1

    on_Column = (p == 0)            # Se si trova al pian terreno sta necessariamente su un elemento colonna

    h_point = frame.Heff - p*frame.storey

    if h_point <= 0 and not on_Column:

        on_CCR_down = True

    elif h_point <= beams[p].h/2 and not on_Column:

        on_CCR_up = True

    else:

        on_Column = True
