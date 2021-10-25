import openseespy.opensees as ops

# ---------------------------------------------------------------------------------------------------------------------------
# Definisco una TimeSeries per l'applicazione dei carichi
# ---------------------------------------------------------------------------------------------------------------------------

def modelTimeSeries():

    ops.timeSeries('Linear', 1, '-factor', 1.0)
