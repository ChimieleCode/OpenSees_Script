from ModelDefinition.Initialize import modelInitialize
from ModelDefinition.NodesDefinition import modelDefineNodes
from ModelDefinition.Restraints import modelRestraints
from ModelDefinition.Constraints import modelConstraints
from ModelDefinition.Transformation import modelTransformation
from ModelDefinition.FrameElements import modelDefineElements
from ModelDefinition.Links import modelDefineLinks
from ModelDefinition.TimeSeries import modelTimeSeries
from ModelDefinition.Masses import modelAssignMasses
from ModelDefinition.Weights import modelAssignWeights

def buildModel():
    
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

    # Define Verical Loads
    modelAssignWeights()