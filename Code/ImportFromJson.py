import json

from Classes.Frame import Frame
from Classes.Section import Section
from Classes.PushPullAnalysis import PushPullAnalysis
from Classes.TimeHistoryAnalysis import TimeHistoryAnalysis
from BasicFunctions.InelasticShape import inelasticShape

# ---------------------------------------------------------------------------------------------------------------------------
# Telaio
# ---------------------------------------------------------------------------------------------------------------------------

file = open('Input/Telaio.json')
data = json.load(file)
file.close

frame = Frame
frame = Frame(data['span'], data['storey'], round(data['n']), data['m'], data['r'], data['mass'], data['Heff'])

# NODI
G_joints = data['G_Joints']

# ---------------------------------------------------------------------------------------------------------------------------
# Sezioni
# ---------------------------------------------------------------------------------------------------------------------------
sections_data = data['sections']
sections = []

for data in sections_data:
    section =  dict(zip(data['Keys'], data['Values']))
    element = Section(section['Section'][1], section['Section'][0], section['Material'], section['S'][0], section['S'][1], section['Strain'], section['Stress'], section['S'][2], section['S'][3])
    sections.append(element)

# COLONNE
column = sections[0]

# TRAVI
beams = [Section(0,0,0,0,0,0)]    # Piano terra non ha travi

for j in range(1, frame.m + 1):    # Per il momento tutte travi uguali

    beams.append(sections[j])

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

