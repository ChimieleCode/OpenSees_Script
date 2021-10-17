import openseespy.opensees as ops
import time

class Frame:

    def __init__(self, span, storey, n, m, r = 1, mass = [0], Heff = 1, damping = 0.05):

        self.span = span                # Altezza di interpiano
        self.storey = storey            # Lunghezza della campata
        self.n = n                      # Numero di campate
        self.m = m                      # Numero di piani
        self.r = r                      # Numero di Telai in parallelo
        self.damping = damping          # Damping del Telaio per Rayleigh
        self.Heff = Heff                # Heff dello SDOF
        self.mass = mass                # Masse di piano da piano terra in tonnellate (La prima entrata viene ignorata, si raccomanda di mettere 0)



    def height(self):       # Calcola l'altezza del telaio

        height = self.m * self.storey

        return height

    def length(self):       # Calcola la lunghezza del telaio

        length = self.n * self.span 

        return length

    def show(self):

        print(f'Telaio Campata: {self.span}m Altezza di interpiano: {self.storey}m Piani: {self.m} Campate: {self.n} Telai in Parallelo: {self.r} Heff: {self.Heff} Damping: {self.damping} Masse di piano: {self.mass}ton') 

class Section:

    def __init__(self, h, b, Emat, Fy, E0, strain = [] , stress = [], Hiso = 0, Hkin = 0 ):

        self.h = h              # Altezza della sezione in m
        self.b = b              # Larghezza della Sezione in m
        self.Emat = Emat        # Modulo di Young in kPa
        self.Fy = Fy            # Momento di snervamento della connessione in kNm
        self.E0 = E0            # Rigidezza elastica della connessione in kNm/rad
        self.strain = strain    # Punti Strain del legame ricentrante, default vuoto in rad
        self.stress = stress    # Punti Stress del legame ricentrante, default vuoto in kNm
        self.Hkin = Hkin        # Fattore di incrudimento cinematico
        self.Hiso = Hiso        # Fattore di incrudimento isteretico [lasciare 0]

    
    def area(self):     # Calcola l'area della sezione

        area = self.b * self.h

        return area


    def inertia(self):  # Calcola l'inerzia della sezione 

        inertia = 1/12 * self.b * self.h**3

        return inertia


    def show(self):

        print(f'Sezione {self.h}x{self.b}m con Modulo di Young: {self.Emat}kPa | Parametri Hardening Fy: {self.Fy}kNm E0: {self.E0}kNm/rad Hiso: {self.Hiso} Hkin:{self.Hkin} ---\n--- Curva Stress: {self.stress}kNm Curva Strain: {self.strain}rad \n') 

class PushPullAnalysis:

    def __init__(self, points = [], step = 0.001 , pattern = []):
        
        self.points = points            # Curva degli spostamenti obiettivo per pushover [m]
        self.step = step                # Grandezza step per la transizione [m]
        self.pattern = pattern          # Pattern unitario di forze (solo fuori terra, si esclude il pian terreno)


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ /
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INPUT
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ /
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

# TELAIO
frame = Frame(11, 4, 2, 2, 2, [0, 140.8, 140.8], 6)

# COLONNA
column = Section(0.6, 0.4, 33346000, 122.9, 109766.68, [-0.0336 ,-0.00112 ,-0.0001 ,0.0 ,0.0001 ,0.00112 ,0.0336 ], [-100.8 ,-96.7 ,-70.4 ,0.0 ,70.4 ,96.7 ,100.8 ], 0, 452.99)

# TRAVI
beams = [Section(0,0,0,0,0,0)]    # Piano terra non ha travi

for j in range(frame.m + 1):    # Per il momento tutte travi uguali

    beams.append(Section(0.6, 0.4, 33346000, 57.8, 63211.97, [-0.0237 ,-0.000915 ,-0.0001 ,0.0 ,0.0001 ,0.000915 ,0.0237 ], [-127.1 ,-97.9 ,-36.0 ,0.0 ,36.0 ,97.9 ,127.1 ], 0, 740.86))


# TRANSFORMATION
LinearTT = 1

# PARAMETRI FRAME RIGIDI
rigid_factor = 1000         # Moltiplicatore del modulo di Young per zone rigide

# PARAMETRI LINK RIGIDI
rigid_stiffness = 1000000000000  # Rigidezza dei link rigidi espressa in kN/m

# ANALISI [ANCORA NON OPERATIVI]
run_pushover = True
run_time_history = False

# ---------------------------------------------------------------------------------------------------------------------------
# Funzioni Utili
# ---------------------------------------------------------------------------------------------------------------------------

n = frame.n
m = frame.m

# FUNZIONI DEI NODI

def nodeGrid(i, j):

    return j*(n + 1) + i


def nodeBase(i):

    return (m + 1)*(n + 1) + i


def nodePanel(i, j):

    return (m + j + 1)*(n + 1) + i


def nodeRigidBeam(i, j, l):

    return (2*m + 1)*(n + 1) + n*(2*j - 1) + 2*i - (1 - l)


def nodeBeam(i, j, l):

    return (2*m + 1)*(2*n + 1) + 2*n*(j - 1) + 2*i - (1 - l)


def nodeColumn(i, j, l):

    return 2*(i + (j - 1)*(n + 1) + n*m + 1) + (2*m + 1)*(2*n + 1) - (1 - l)


def nodeTopColumn(i):

    return 4*m*(2*n + 1) + i

    # Nodo di controllo più avanti

# FUNZIONI DEI MATERIALI

def columnN():

    return 1


def columnS():

    return 2


def beamPT(j):

    return 2*j + 1


def beamS(j):

    return 2*(j + 1)


def jointLink(j):       # Assunto che tutti i link allo stesso piano siano uguali

    return 2*(m + 1) + j


def rigidLink():

    return 3*m +2


# FUNZIONE PER DEFINIRE LA DEFORMATA DI PUSHOVER (PATTERN)

def inelasticShape(frame):

    shape = []

    for j in range(1,m + 1):            # j da 1 a m 

        if m <= 4:

            shape.append(j*frame.storey/frame.height())

        else:

            shape.append(4/3 * (j*frame.storey/frame.height()) * (1 - j*frame.storey/frame.height() * 1/4))

    return shape


# ---------------------------------------------------------------------------------------------------------------------------
# Nodo di Controllo
# ---------------------------------------------------------------------------------------------------------------------------

# VERIFICA CHE IL NODO DI CONTROLLO NON CAPITI SU UN NODO ESISTENTE (si considera sovrapposto entro una tolleranza di 1cm)
controlNode_override = False        # True --> il nodo di controllo è sovrapposto ad un esistente
controlNode_id = 0
tolleranza_di_sovrapposizione = 0.01            # (si considera sovrapposto entro una tolleranza di 1cm)

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

def controlNode():

    if controlNode_override:

        return controlNode_id

    else:

        return 4*m*(2*n + 1) + (n + 1)

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

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ /
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DEFINIZIONE DEL MODELLO
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ /
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

ops.wipe()

ops.model('basic','-ndm',2,'-ndf',3)

# ---------------------------------------------------------------------------------------------------------------------------
# Definisco i nodi
# ---------------------------------------------------------------------------------------------------------------------------

# # NODI GRIGLIA
for j in range(m + 1):          # j da 0 a m

    for i in range(n + 1):          # i da 0 a n

        ops.node(nodeGrid(i, j), i * frame.span, j * frame.storey)      # Nodo Griglia

# NODI BASE E COLONNA TOP
for i in range(n + 1):          # i da 0 a n

    ops.node(nodeBase(i), i * frame.span, 0)     # Nodo Base

    ops.node(nodeTopColumn(i), i * frame.span, m * frame.storey - beams[m].h / 2)     # Nodo Colonna Top

# NODI PANNELLO
for j in range(1, m + 1):       # j da 1 a m

    for i in range(n + 1):          # i da 0 a n

        ops.node(nodePanel(i, j), i * frame.span, j * frame.storey)     # Nodo Pannello


# NODI RIGID BEAM E BEAM
for j in range(1, m + 1):        # j da 1 a m

    for i in range(1, n + 1):           # i da 1 a n

        ops.node(nodeRigidBeam(i, j, 0), (i - 1) * frame.span + column.h / 2, j * frame.storey)     # Nodo Rigid Beam Sx ( l = 0 )

        ops.node(nodeBeam(i, j, 0), (i - 1) * frame.span + column.h / 2, j * frame.storey)          # Nodo Beam Sx ( l = 0 )

        ops.node(nodeRigidBeam(i, j, 1), i * frame.span - column.h / 2, j * frame.storey)           # Nodo Rigid Beam Sx ( l = 1 )

        ops.node(nodeBeam(i, j, 1), i * frame.span - column.h / 2, j * frame.storey)                # Nodo Beam Sx ( l = 1 )

# NODI COLUMN 
for j in range(1, m):        # j da 1 a m - 1

    for i in range(n + 1):           # i da 0 a n

       ops.node(nodeColumn(i, j, 0), i * frame.span, j * frame.storey - beams[j].h / 2)               # Nodo Colonna Sotto ( l = 0 ) 

       ops.node(nodeColumn(i, j, 1), i * frame.span, j * frame.storey + beams[j].h / 2)               # Nodo Colonna Sopra ( l = 0 ) 

# NODO DI CONTROLLO
if not controlNode_override:

    ops.node(controlNode(), 0, frame.Heff)

# ---------------------------------------------------------------------------------------------------------------------------
# Definisco i restraint
# ---------------------------------------------------------------------------------------------------------------------------

for i in range(n + 1):          # i da 0 a n

    ops.fix(nodeGrid(i, 0), 1, 1, 1)

# ---------------------------------------------------------------------------------------------------------------------------
# Vincoli diaframma
# ---------------------------------------------------------------------------------------------------------------------------

# for j in range(1, m + 1):        # j da 1 a m

#     for i in range(1, n + 1):           # i da 1 a n

#         ops.equalDOF(nodeGrid(i - 1, j), nodeGrid(i, j), 1)     # Diaframma come equalDOF campata per campata, piano per piano

# ---------------------------------------------------------------------------------------------------------------------------
# EqualDof Nodi link
# ---------------------------------------------------------------------------------------------------------------------------

# LINK PER TRAVI
for j in range(1, m + 1):        # j da 1 a m

    for i in range(1, n + 1):           # i da 1 a n

        ops.equalDOF(nodeRigidBeam(i, j, 0), nodeBeam(i, j, 0), 1, 2)

        ops.equalDOF(nodeRigidBeam(i, j, 1), nodeBeam(i, j, 1), 1, 2)

# LINK PER NODI [Al momento non modellati]
for j in range(1, m + 1):        # j da 1 a m

    for i in range(n + 1):           # i da 0 a n

        ops.equalDOF(nodeGrid(i, j), nodePanel(i, j), 1, 2, 3) # Il 3 andrà rimosso quando modello i nodi

# ---------------------------------------------------------------------------------------------------------------------------
# Funzione di trasformazione
# ---------------------------------------------------------------------------------------------------------------------------

ops.geomTransf('Linear', LinearTT)

# ---------------------------------------------------------------------------------------------------------------------------
# Elementi ElasticBeamColumn
# ---------------------------------------------------------------------------------------------------------------------------

x = 0  # Variabile ausiliaria per la numerazione degli elementi, attualmente non vi è la necessità di avere formule, l'importante è che venga sempre incrementato ad ogni nuova definizione

# COLONNE DI BASE
for i in range(n + 1):          # i da 0 a n

    if (p == 0) and on_Column and i == 0: # Se il nodo di controllo giace su questo elemento, non definirlo

        continue

    else:

        if m == 1:

            ops.element('elasticBeamColumn', x, nodeBase(i), nodeTopColumn(i), column.area(), column.Emat, column.inertia(), LinearTT)
            x += 1

        else:

            ops.element('elasticBeamColumn', x, nodeBase(i), nodeColumn(i ,1, 0), column.area(), column.Emat, column.inertia(), LinearTT)
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
                    x += 1

                else:

                    ops.element('elasticBeamColumn', x, nodeColumn(i ,j, 1), nodeColumn(i ,j + 1, 0), column.area(), column.Emat, column.inertia(), LinearTT)
                    x += 1

# TRAVE PIANO j CAMPATA i
for j in range(1, m + 1):        # j da 1 a m

    for i in range(1, n + 1):           # i da 1 a n

        ops.element('elasticBeamColumn', x, nodeBeam(i ,j, 0), nodeBeam(i ,j, 1), beams[j].area(), beams[j].Emat, beams[j].inertia(), LinearTT)
        x += 1

# CONNESSIONE COLONNA RIGIDA SOTTO VERTICALE i PIANO j
for j in range(1, m + 1):       # j da 1 a m

    for i in range(n + 1):          # i da 0 a n

        if on_CCR_down and i == 0: # Se il nodo di controllo giace su questo elemento, non definirlo

            continue

        else:

            if j == m:

                ops.element('elasticBeamColumn', x, nodeTopColumn(i), nodeGrid(i, j), column.area(), column.Emat * rigid_factor, column.inertia(), LinearTT)
                x += 1 

            else:

                ops.element('elasticBeamColumn', x, nodeColumn(i ,j, 0), nodeGrid(i, j), column.area(), column.Emat * rigid_factor, column.inertia(), LinearTT)
                x += 1 

# CONNESSIONE COLONNA RIGIDA SOPRA VERTICALE i PIANO j
for j in range(1, m):       # j da 1 a m - 1

    for i in range(n + 1):          # i da 0 a n

        if on_CCR_up and i == 0: # Se il nodo di controllo giace su questo elemento, non definirlo

            continue

        else:

            ops.element('elasticBeamColumn', x, nodeGrid(i, j), nodeColumn(i ,j, 1), column.area(), column.Emat * rigid_factor, column.inertia(), LinearTT)
            x += 1 

# CONNESSIONE TRAVE RIGIDA SX e DX PIANO j CAMPATA i
for j in range(1, m + 1):        # j da 1 a m

    for i in range(1, n + 1):           # i da 1 a n

        ops.element('elasticBeamColumn', x, nodePanel(i - 1, j), nodeRigidBeam(i, j, 0), beams[j].area(), beams[j].Emat * rigid_factor, beams[j].inertia(), LinearTT)
        x += 1

        ops.element('elasticBeamColumn', x, nodeRigidBeam(i, j, 1), nodePanel(i, j), beams[j].area(), beams[j].Emat * rigid_factor, beams[j].inertia(), LinearTT)
        x += 1

# HANDLER DEL NODO DI CONTROLLO
if not controlNode_override:

    if on_Column:           # Costruisco la colonna in 2 pezzi con il nodo di controllo dentro

        if p == m - 1:

            ops.element('elasticBeamColumn', x, controlNode(), nodeTopColumn(0), column.area(), column.Emat, column.inertia(), LinearTT)
            x += 1

        else:

            ops.element('elasticBeamColumn', x, controlNode(), nodeColumn(0, p + 1, 0), column.area(), column.Emat, column.inertia(), LinearTT)
            x += 1


        if p == 0:

            ops.element('elasticBeamColumn', x, nodeBase(0), controlNode(), column.area(), column.Emat, column.inertia(), LinearTT)
            x += 1

        else:

            ops.element('elasticBeamColumn', x, nodeColumn(0, p, 1), controlNode(), column.area(), column.Emat, column.inertia(), LinearTT)
            x += 1


    elif on_CCR_down:       # Costruisco il link rigido in 2 pezzi con il nodo di controllo dentro

        ops.element('elasticBeamColumn', x, controlNode(), nodeGrid(0, p), column.area(), column.Emat, column.inertia(), LinearTT)
        x += 1

        if p == m:

            ops.element('elasticBeamColumn', x, nodeTopColumn(0), controlNode(), column.area(), column.Emat, column.inertia(), LinearTT)
            x += 1

        else:

            ops.element('elasticBeamColumn', x, nodeColumn(0, p, 0), controlNode(), column.area(), column.Emat, column.inertia(), LinearTT)
            x += 1

    elif on_CCR_up:

        ops.element('elasticBeamColumn', x, controlNode(), nodeColumn(0, p, 1), column.area(), column.Emat, column.inertia(), LinearTT)
        x += 1 

        ops.element('elasticBeamColumn', x, nodeGrid(0, p), controlNode(), column.area(), column.Emat, column.inertia(), LinearTT)
        x += 1

# ---------------------------------------------------------------------------------------------------------------------------
# UniaxialMaterial per i link
# ---------------------------------------------------------------------------------------------------------------------------

# DEFINISCO LEGAME N COLONNA
ops.uniaxialMaterial('ElasticMultiLinear', columnN(), '-strain', column.strain[0], column.strain[1], column.strain[2], column.strain[3], column.strain[4], column.strain[5], column.strain[6], '-stress', column.stress[0], column.stress[1], column.stress[2], column.stress[3], column.stress[4], column.stress[5], column.stress[6])

# DEFINISCO LEGAME S COLONNA
ops.uniaxialMaterial('Hardening', columnS(), column.E0, column.Fy, column.Hiso, column.Hkin)

# DEFINISCO LEGAMI PT TRAVI E S TRAVI
for j in range(1, m + 1):       # j da 1 a m

    ops.uniaxialMaterial('ElasticMultiLinear', beamPT(j), '-strain', beams[j].strain[0], beams[j].strain[1], beams[j].strain[2], beams[j].strain[3], beams[j].strain[4], beams[j].strain[5], beams[j].strain[6], '-stress', beams[j].stress[0], beams[j].stress[1], beams[j].stress[2], beams[j].stress[3], beams[j].stress[4], beams[j].stress[5], beams[j].stress[6])

    ops.uniaxialMaterial('Hardening', beamS(j), beams[j].E0, beams[j].Fy, beams[j].Hiso, beams[j].Hkin)

# SALTO LA DEFINIZIONE DEI LINK NODI

# DEFINISCO IL LINK RIGIDO DA ASSEGNARE ALLA BASE PER 1 E 2
ops.uniaxialMaterial('Elastic', rigidLink(), rigid_stiffness)

# ---------------------------------------------------------------------------------------------------------------------------
# Definisco i Link
# ---------------------------------------------------------------------------------------------------------------------------

# DEFINISCO I LINK DELLE COLONNE VERTICALI N e S
for i in  range(n + 1):          # i da 0 a n

    ops.element('zeroLength', x, nodeGrid(i, 0), nodeBase(i), '-mat', columnN(), rigidLink(), rigidLink(), '-dir', 6, 1, 2)
    x += 1

    ops.element('zeroLength', x, nodeGrid(i, 0), nodeBase(i), '-mat', columnS(), rigidLink(), rigidLink(), '-dir', 6, 1, 2)
    x += 1

# DEFINISCO I LINK DELLE TRAVI PT e S a DX e a SX
for j in range(1, m + 1):        # j da 1 a m

    for i in range(1, n + 1):           # i da 1 a n

        ops.element('zeroLength', x, nodeRigidBeam(i, j, 0), nodeBeam(i, j, 0), '-mat', beamPT(j), '-dir', 6)     # PT SX
        x += 1

        ops.element('zeroLength', x, nodeRigidBeam(i, j, 0), nodeBeam(i, j, 0), '-mat', beamS(j), '-dir', 6)      # S  SX
        x += 1 

        ops.element('zeroLength', x, nodeBeam(i, j, 1), nodeRigidBeam(i, j, 1), '-mat', beamPT(j), '-dir', 6)     # PT DX
        x += 1

        ops.element('zeroLength', x, nodeBeam(i, j, 1), nodeRigidBeam(i, j, 1), '-mat', beamS(j), '-dir', 6)      # S  DX
        x += 1

# LINK DEI NODI NON DEFINITI

# ---------------------------------------------------------------------------------------------------------------------------
# Definisco una TimeSeries per l'applicazione dei carichi
# ---------------------------------------------------------------------------------------------------------------------------

ops.timeSeries('Linear', 1, '-factor', 1.0)

# ---------------------------------------------------------------------------------------------------------------------------
# Definisco le masse dei nodi
# ---------------------------------------------------------------------------------------------------------------------------

try:

    for j in range(1, m + 1):        # j da 1 a m

        for i in range(n + 1):           # i da 0 a n

            if i == 0 and i == n:

                ops.mass(nodeGrid(i, j), frame.mass[j]/(2*n*frame.r), 0, 0)

            else:

                ops.mass(nodeGrid(i, j), frame.mass[j]/(n*frame.r), 0, 0)

except:

    print('Errore: il numero di masse di piano definite non corrisponde al numero di piani')


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ /
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ANALISI PUSH-PULL
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ /
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------
# Definisco le Push-Pull
# ---------------------------------------------------------------------------------------------------------------------------

push_pull = PushPullAnalysis([0.1, -0.1, 0.15, -0.15, 0.2, -0.2, 0.25, -0.25, 0.25], 0.001, inelasticShape(frame))

# Setto i recorders
ops.recorder('Node', '-file', 'Pushover\Pushover_Base_Reactions.out', '-time', '-node', 0, 1, 2, '-dof', 1, 'reaction')     # Da Automatizzare o Base reaction
ops.recorder('Node', '-file', 'Pushover\Pushover_Storey_Drift.out', '-time', '-node', controlNode(), '-dof', 1, 'disp')

# ---------------------------------------------------------------------------------------------------------------------------
# Inizio la definizione della prima Push
# ---------------------------------------------------------------------------------------------------------------------------

print(f'-o-o-o- Analisi Push-Pull 1/{len(push_pull.points)} -o-o-o-')

# Parte il cronometro
tStart = round(time.time() * 1000)

# Definisco i Parametri 
direzione = push_pull.points[0]/abs(push_pull.points[0])
spostamento = direzione * push_pull.points[0]
step = direzione * push_pull.step
total_steps = round(spostamento/step)

# ---------------------------------------------------------------------------------------------------------------------------
# Definisco il Pattern di spinta
# ---------------------------------------------------------------------------------------------------------------------------

ops.pattern('Plain', 1, 1)

for j in range(m):          # j da 0 a m - 1

    try:

        ops.load(nodeGrid(0, j + 1), direzione * push_pull.pattern[j], 0., 0.)  # Applico la forza j al piano j + 1 poiché salto il piano 0

    except:

        print('Errore: Il numero di forze del pattern differisce dal numero di piani fuori terra')

# ---------------------------------------------------------------------------------------------------------------------------
# Opzioni di analisi
# ---------------------------------------------------------------------------------------------------------------------------

ops.constraints('Transformation')
ops.numberer('RCM')
ops.system('BandGen')
ops.test('NormDispIncr', 0.000001, 100)
ops.algorithm('NewtonLineSearch', True, False, False, False, 0.8, 1000, 0.1, 10)
ops.integrator('DisplacementControl', controlNode(), 1, step)
ops.analysis('Static')

# ---------------------------------------------------------------------------------------------------------------------------
# Mando l'analisi
# ---------------------------------------------------------------------------------------------------------------------------
ops.record()
ops.analyze(total_steps)

# Info sulle Performance
tStop = round(time.time() * 1000)
totalTime = (tStop - tStart)/1000

print(f'-o-o-o- Analisi conclusa 1/{len(push_pull.points)} dopo {totalTime} sec -o-o-o- ')

# ---------------------------------------------------------------------------------------------------------------------------
# Punti successivi
# ---------------------------------------------------------------------------------------------------------------------------

if len(push_pull.points) > 1:

    for v in range(1,len(push_pull.points)):

        print(f'-o-o-o- Analisi Push-Pull {v + 1}/{len(push_pull.points)} -o-o-o-')

        # Parte il cronometro
        tStart = round(time.time() * 1000)

        # Definisco i Parametri 
        try:

            direzione = abs(push_pull.points[v] - push_pull.points[v - 1]) / (push_pull.points[v] - push_pull.points[v - 1])
            spostamento = push_pull.points[v] - push_pull.points[v - 1]
            step = direzione * push_pull.step
            total_steps = round(spostamento/step)

        except:

            print('Errore nella definizione dei punti: controllare che non ci siano punti successivi di egual spostamento')
            break

        # Opzioni di Analisi
        ops.numberer('RCM')
        ops.system('BandGen')
        ops.test('NormDispIncr', 0.000001, 100)
        ops.algorithm('NewtonLineSearch', True, False, False, False, 0.8, 1000, 0.1, 10)
        ops.integrator('DisplacementControl', controlNode(), 1, step)
        ops.analysis('Static')

        # Mando l'analisi
        ops.record()
        ops.analyze(total_steps)

        # Info sulle Performance
        tStop = round(time.time() * 1000)
        totalTime = (tStop - tStart)/1000

        print(f'-o-o-o- Analisi conclusa {v + 1}/{len(push_pull.points)} dopo {totalTime} sec -o-o-o- ')

ops.wipeAnalysis()


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ /
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ANALISI TIME-HISTORY
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ /
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
