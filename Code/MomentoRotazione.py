from Classes.Links import MultilinearElasticLink, KineticLink, GMSteelLink
from SolverFunctions.Solver import steelYielding, steelFailure, tendonYielding, computePoint, timberYielding
from BasicFunctions.Moment import steelMoment, tendonMoment, axialLoadMoment
from ImportFromJson import sections
from ModelOptions import use_GM, PT_Points, print_limit_states

timberDS = []
sezioni = []

for section in sections:

    points = []
    
    # Snervamento Armature
    points.append(steelYielding([0.005, 0.3], section))
    # print('Armature S')

    # Legno, mi interessa solo theta per ds
    timberDS.append(timberYielding([0.02, 0.15], section)[0])
    # print('Timber')

    # Fallimento Armature
    points.append(steelFailure([0.02, 0.2], section))
    # print('Armature F')

    # Snervamento PostTensione [Se Presente]
    if section.tendon != None:

        points.append(tendonYielding([0.05, 0.1], section))
        # print('Trefoli')


    # Punti aggiuntivi
    delta_theta = (points[1][0] - points[0][0]) / (PT_Points + 1)   # (Theta_s - Thesta_y) / ...
    
    for i in range(PT_Points):   # Da 0 a PT_Points - 1

        theta = delta_theta * (i + 1) + points[0][0]        # dTheta * (i+1) + Theta_y
        neutralAxis = computePoint(initialGuess = [points[1][1]], section = section, theta = theta)

        points.append([theta, neutralAxis[0]])

    # --------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Multilinear Elastic
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    # Inizializzo
    strain_points = [0]
    stress_points = [0]

    # Punto di decompressione
    
    decompression_strain = 0.0004
    decompression_stress = 1/6 * (section.ptTension + section.axialLoad) * section.h

    strain_points.append(decompression_strain)
    strain_points.append(-decompression_strain)

    stress_points.append(decompression_stress)
    stress_points.append(-decompression_stress)

    for point in points:

        strain_points.append(point[0])
        strain_points.append(-point[0])

        stress_points.append(tendonMoment(point[0], point[1], section) + axialLoadMoment(point[0], point[1], section))
        stress_points.append(-(tendonMoment(point[0], point[1], section) + axialLoadMoment(point[0], point[1], section)))

    strain_points.sort()
    stress_points.sort()

    # print(strain_points)
    # print(stress_points)

    multilinearElasticLink = MultilinearElasticLink(strain = strain_points, stress = stress_points)
    section.multilinearElasticLink = multilinearElasticLink

    # --------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Multilinear Plastic
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    # Fy e E0
    yielding_moment = steelMoment(points[0][0], points[0][1], section)

    elastic_stiffness = yielding_moment / points[0][0]                  
    
    plastic_stiffness = (steelMoment(points[1][0], points[1][1], section) - yielding_moment) / (points[1][0]-points[0][0])       # points 1 0 è theta alla rottura e points 0 0 è allo snervamento  

    # Link type
    if abs(elastic_stiffness) <= 10**-6:

        print('Sezione Senza Armatura')

    else:

        # Link type
        if use_GM:

            b = plastic_stiffness/elastic_stiffness

            GM_link = GMSteelLink(Fy = yielding_moment, E0 = elastic_stiffness, b = b, strainLimit = points[1][0])

            section.GMLink = GM_link


        else:

            Hkin = elastic_stiffness * plastic_stiffness / (elastic_stiffness - plastic_stiffness)

            kineticLink = KineticLink(Fy = yielding_moment, E0 = elastic_stiffness, Hkin = Hkin, strainLimit = points[1][0])

            section.kineticLink = kineticLink



# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DEFINITION OF SECTIONS
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

# COLONNE
column = sections[0]        # Primo elemento

edge_column = sections[-1]  # Ultimo elemento

# TRAVI
beams = [None]    # Piano terra non ha travi

for j in range(1, len(sections) - 1):    # L'ultimo indice è il pilastro esterno

    beams.append(sections[j])


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PRINT DS
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Calcolo i damage state Capacity
damage_state = []

damage_state.append([edge_column.GMLink.strainLimit, None, timberDS[-1]])
damage_state.append([column.GMLink.strainLimit, None, timberDS[0]])

for i, beam in enumerate(beams):

    if i == 0:

        continue

    else:
        
        if beam.GMLink != None:

            damage_state.append([beam.GMLink.strainLimit, beam.multilinearElasticLink.strain[-1], timberDS[i]])
            damage_state.append([beam.GMLink.strainLimit, beam.multilinearElasticLink.strain[-1], timberDS[i]])

        else:

            damage_state.append([None, beam.multilinearElasticLink.strain[-1], timberDS[i]])
            damage_state.append([None, beam.multilinearElasticLink.strain[-1], timberDS[i]])


# print(damage_state)

# Metto a schermo i damage state
if print_limit_states:

    print(f'Column DS1: {column.GMLink.strainLimit}')
    print(f'EdgeColumn DS1: {edge_column.GMLink.strainLimit}')
        
    for i, beam in enumerate(beams):

        if i == 0:

            continue

        else:

            print(f'Beam{i} DS1: {beam.GMLink.strainLimit} DS2: {beam.multilinearElasticLink.strain[-1]}')


