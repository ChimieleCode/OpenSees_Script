# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# MODEL AND OPTIONS
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

# RIGID YOUNG RATIO
rigid_factor = 1000         # Moltiplicatore del modulo di Young per zone rigide

# PARAMETERS OF RIGID LINKS
rigid_stiffness = 1000000000000  # Rigidezza dei link rigidi espressa in kN/m

# NODE OPTIOONS
rigid_joints = True    # Modellare i nodi come rigidi

# LINK OPTIONS
use_GM = True            # Usre GM? Altrimenti Kinematic
steel_failure = False     # Considera il fallimento dei link S
tendon_failure = False      # Considera il fallimento dei link PT al loro snervamento, Non agisce sui link N
 
# RUN ANALYSIS
run_modal = False
run_pushover = False
run_time_history = True

# CONTROL NODE 
tolleranza_di_sovrapposizione = 0.01            # (si considera sovrapposto ad uno esistente entro una tolleranza di 1cm)

# TRANSFORMATIONS
LinearTT = 1


