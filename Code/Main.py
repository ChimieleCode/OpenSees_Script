
from ModelOptions import run_pushover,run_time_history,run_modal,compute_damping,print_graphs,compute_section_gaps_evnelopes,run_IDA
from ImportFromJson import time_history_analysis

from ModelDefinition.Initialize import modelInitialize
from ModelDefinition.NodesDefinition import modelDefineNodes
from ModelDefinition.Restraints import modelRestraints
from ModelDefinition.Constraints import modelConstraints
from ModelDefinition.Transformation import modelTransformation
from ModelDefinition.FrameElements import modelDefineElements
from ModelDefinition.Links import modelDefineLinks
from ModelDefinition.TimeSeries import modelTimeSeries
from ModelDefinition.Masses import modelAssignMasses

from AnalysisDefinition.PushPull import runPushoverAnalysis
from AnalysisDefinition.Modal import runModalAnalysis
from AnalysisDefinition.TimeHistory import runTimeHistory
from IncrementalDynamicAnalysis import incrementalDynamicAnalysis

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# MODEL BUILDER
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Initialize Model
modelInitialize()

# Define model's nodes
modelDefineNodes()
 
# Assign Base Restraints
modelRestraints()

# Assign Diaphragm Constraints
modelConstraints()

# Define Transformation
modelTransformation()

# Define ElasticBeamColumn Elements
last_element = modelDefineElements()

# Define ElasticBeamColumn Elements
modelDefineLinks(last_element)
 
# Define a TimeSeries
modelTimeSeries()

# Define Mass Source
modelAssignMasses()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PUSH-PULL ANALYSIS
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

if run_pushover:

    runPushoverAnalysis()

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

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PLOT DATA
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

if print_graphs:

    import PlotData


if compute_section_gaps_evnelopes:

    import Fragility

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# POST PROCESSING
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

if compute_damping:

    import PostProcessing.Damping
