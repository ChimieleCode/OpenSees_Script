from ImportFromJson import sections, frame 


def tendonStrain(theta, neutralAxis, section):

    delta = theta * ( section.h/2 - neutralAxis)

    unbonded_length = frame.n * frame.span + sections[0].h

    delta_strain = delta * frame.n * 2 / unbonded_length

    strain = delta_strain + section.tendonInitialStrain()

    return strain


def steelStrain(theta, neutralAxis, section):

    deltas = []

    deltas.append(theta * (section.d() - neutralAxis))      # Bottom
    deltas.append(theta * (section.c  - neutralAxis))        # Top

    strains = []

    for delta in deltas:
        
        strains.append(delta / section.barLength())

    return strains


def timberStrain(theta, neutralAxis, section):

    Lcant = 0

    if section.isBeam:

        Lcant = (frame.span - sections[0].h) / 2        # Se è una trave Lcant = Ltrave - hc
    
    else:

        Lcant = (frame.storey - sections[1].h) / 2      # Se è colonna di base Lcant = Hcolumn - hbeam,1
        

    strain = neutralAxis * ( 3 * theta / Lcant)

    return strain

