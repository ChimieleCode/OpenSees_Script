import openseespy.opensees as ops

from ModelOptions import LinearTT, PDeltaTT

# Transformation ID
def modelTransformation():

    ops.geomTransf('Linear', LinearTT)
    ops.geomTransf('PDelta', PDeltaTT)