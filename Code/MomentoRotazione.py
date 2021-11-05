from Classes.Links import MultilinearElasticLink, KineticLink, GMSteelLink
from SolverFunctions.Solver import steelYielding, steelFailure, tendonYielding
from BasicFunctions.Moment import steelMoment, tendonMoment, axialLoadMoment
from ImportFromJson import sections, frame
from ModelOptions import use_GM

for section in sections:

    points = []
    
    # Snervamento Armature
    points.append(steelYielding([0.005, 0.2], section))

    # Fallimento Armature
    points.append(steelFailure([0.02, 0.1], section))

    # Snervamento PostTensione [Se Presente]
    if section.tendon != None:

        points.append(tendonYielding([0.05, 0.1], section))


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



    



