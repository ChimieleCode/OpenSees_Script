import time
import math
from ModelBuilder import buildModel
from PostProcessing.Damping import computeDamping

from ModelOptions import run_pushover,run_time_history,run_modal,compute_damping,print_graphs,compute_section_gaps_evnelopes,run_IDA,performance_point
from ImportFromJson import time_history_analysis

from AnalysisDefinition.PushPull import runPushoverAnalysis
from AnalysisDefinition.Modal import runModalAnalysis
from AnalysisDefinition.TimeHistory import runTimeHistory
from IncrementalDynamicAnalysis import incrementalDynamicAnalysis


tStart = round(time.time() * 1000)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# MODEL BUILDER
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

buildModel()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PUSH-PULL ANALYSIS
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

if run_pushover:

    runPushoverAnalysis()
    

if performance_point:

    import PeformancePoint

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# MODAL ANALYSIS
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

if run_modal and ((not run_time_history) and (not run_IDA)):
 
    runModalAnalysis()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TIME-HISTORY ANALYSIS
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

if run_time_history:

    structure_periods = runModalAnalysis()
    runTimeHistory(time_history_analysis,structure_periods)


if run_IDA:

    structure_periods = runModalAnalysis()
    incrementalDynamicAnalysis(time_history_analysis,structure_periods)
    import PostProcessing.IDAProcessing

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PLOT DATA
# -------------------------------------------------------------- -----------------------------------------------------------------------------------------------------

if print_graphs:

    import PlotData


if compute_section_gaps_evnelopes:

    import RunFragility

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# POST PROCESSING
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

if compute_damping:

    computeDamping()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CRONOMETRO
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

tStop = round(time.time() * 1000)
timeSeconds = round((tStop - tStart) / 1000)
timeMinutes = math.floor(timeSeconds / 60)
timeHours = math.floor(timeSeconds / 3600)
timeMinutes = round(timeMinutes - timeHours * 60)
timeSeconds = round(timeSeconds - timeHours * 3600 - timeMinutes * 60)

print(f'-o-o-o- TUTTE LE ANALISI CONCLUSE IN {timeHours}:{timeMinutes}:{timeSeconds} -o-o-o-')