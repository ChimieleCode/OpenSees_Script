import json
import copy

from BasicFunctions.InelasticShape import inelasticShape
from Classes.Frame import Frame
from Classes.Section import Section
from Classes.Tendon import Tendon
from Classes.Timber import Timber
from Classes.Steel import Steel
from Classes.PushPullAnalysis import PushPullAnalysis
from Classes.TimeHistoryAnalysis import TimeHistoryAnalysis

# ---------------------------------------------------------------------------------------------------------------------------
# Acciaio
# ---------------------------------------------------------------------------------------------------------------------------

file = open('Input/Steel.json')
data = json.load(file)
file.close

B450C = Steel(
    yieldStress = data['YieldStress'], 
    r = data['r']
    )

# ---------------------------------------------------------------------------------------------------------------------------
# Tendon
# ---------------------------------------------------------------------------------------------------------------------------

file = open('Input/Tendon.json')
data = json.load(file)
file.close

tendon = Tendon(
    yieldStress = data['YieldStress'], 
    E = data['Young'], 
    area = data['Area']
    )

# ---------------------------------------------------------------------------------------------------------------------------
# Timber
# ---------------------------------------------------------------------------------------------------------------------------

file = open('Input/Timber.json')
data = json.load(file)
file.close

LVL = Timber(
    parallelStrength = data['YieldStress'], 
    E = data['Young'], 
    G = data['G']
    )

# ---------------------------------------------------------------------------------------------------------------------------
# Telaio
# ---------------------------------------------------------------------------------------------------------------------------

file = open('Input/Telaio.json')
data = json.load(file)
file.close

frame = Frame(
    span =data['span'],
    storey = data['storey'], 
    n = round(data['n']), 
    m = data['m'], 
    r = data['r'],
    mass = data['mass'], 
    Heff = data['Heff']
    )

# ---------------------------------------------------------------------------------------------------------------------------
# Sezioni
# ---------------------------------------------------------------------------------------------------------------------------

sections_data = data['sections']
sections = []

for data in sections_data:

    section =  dict(zip(data['Keys'], data['Values']))

    element = Section(
        h = section['h'],
        b = section['b'],
        c = section['c'],
        kcon = section['Kcon'],
        axialLoad = section['AxialLoad'],
        steelBarNumber = section['Reinforcement'][1],
        steelBarDiameter = section['Reinforcement'][0],
        ptNumber = section['Tensioning'][0],
        ptTension = section['Tensioning'][1],
        timber = LVL,
        steel = B450C
        )
    
    if element.kcon != 0.55:

        element.tendon = tendon
    

    sections.append(element)

# Pilastro Esterno

sections.append(copy.deepcopy(sections[0]))             # Creo una nuova istanza identica ed indipendente

if frame.n > 2:
    
    sections[-1].axialLoad = sections[-1].axialLoad/2     # Assumo che per i pilsatri esterni l'assiale sia la metà a meno che non esistano pilastri interni


# ---------------------------------------------------------------------------------------------------------------------------
# Pushover
# ---------------------------------------------------------------------------------------------------------------------------

file = open('Input/Pushover.json')
data = json.load(file)
file.close

push_pull = PushPullAnalysis(data['points'],data['step'],inelasticShape(frame))

# ---------------------------------------------------------------------------------------------------------------------------
# TimeHistory
# ---------------------------------------------------------------------------------------------------------------------------

file = open('Input/TimeHistory.json')
data = json.load(file)
file.close

time_history_analysis = []

for serie in data['TimeHistory']:
    dictionary = dict(zip(serie['Keys'],serie['Values']))
    timehistory = TimeHistoryAnalysis(dictionary['id'], dictionary['sf'], dictionary['dt'], dictionary['duration'], dictionary['TimeStepRatio'])
    time_history_analysis.append(timehistory)

