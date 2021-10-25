import openseespy.opensees as ops

from ModelOptions import LinearTT

# Transformation ID
def modelTransformation():

    ops.geomTransf('Linear', LinearTT)