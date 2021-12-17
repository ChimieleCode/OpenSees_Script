# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# MODEL AND OPTIONS
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

# RIGID YOUNG RATIO
rigid_factor = 1000         # Moltiplicatore del modulo di Young per zone rigide

# PARAMETERS OF RIGID LINKS
rigid_stiffness = 1000000000000  # Rigidezza dei link rigidi espressa in kN/m

# NODE OPTIOONS
rigid_joints = False    # Modellare i nodi come rigidi
beta = 0.6             # Rapporto di ricentramento (Necessario a stabilire quanto momento porta il tendon bypassando il nodo)

# LINK OPTIONS
PT_Points = 5             # Extra points for better discretization of PT and N links, Min 0
use_GM = True            # Usre GM? Altrimenti Kinematic
steel_failure = True   # Considera il fallimento dei link S
tendon_failure = True      # Considera il fallimento dei link PT al loro snervamento, Non agisce sui link N
 
# RUN ANALYSIS
run_modal = True
run_pushover = False
run_time_history = False
run_IDA = True

# IDA OPTIONS
initialSa = 0.05
initialstep = 1
maxiterIDA = 6

# OUTPUT OPTIONS
print_graphs = False                     # Salva Grafici come PNG
print_limit_states = False              # Mette a schermo gli stati limite per le sezioni

compute_damping = False                 # calcola il damping per cicli chiusi nelle pushpull
record_section_gaps = False             # Crea un file con i gap delle sezioni esterne per pushover

compute_section_gaps_evnelopes = False   # Calcola il gap massimo delle sezioni nelle TH per la prima verticale 
compute_spectral_response = False        # calcola l'Sa di uno SDOF per il segnale di input

# CONTROL NODE 
tolleranza_di_sovrapposizione = 0.01            # (si considera sovrapposto ad uno esistente entro una tolleranza di 1cm)

# TRANSFORMATIONS
LinearTT = 1

# OTHER OPTIONS
csi = 0.05                  # Valore di csi per il calcolo dello spettro di risposta SDOF dell'accelerogramma (NON E' IL DAMPING PER LE TH!!!!)


