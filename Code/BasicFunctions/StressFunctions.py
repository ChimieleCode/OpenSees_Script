from BasicFunctions.StrainFunctions import tendonStrain, timberStrain, steelStrain


def tendonStress(theta, neutralAxis, section):

    strain = tendonStrain(theta, neutralAxis, section)

    if section.tendon == None:

        stress = 0

    else:
    
        stress = strain * section.tendon.E * section.postTensionArea()

    return stress


def steelStress(theta, neutralAxis, section):

    strains = steelStrain(theta, neutralAxis, section)
    yield_strain = section.steel.yieldStrain()

    stresses = []

    for strain in strains:

        if abs(strain) <= yield_strain:

            stresses.append(strain * section.steelArea() * section.steel.E)

        else:

            sign = abs(strain) / strain
            stresses.append(sign * section.steelArea() * section.steel.yieldStress * ( 1 + section.steel.r * (strain / yield_strain -1)) )
        

    return stresses


def timberStress(theta, neutralAxis, section):

    strain = timberStrain(theta, neutralAxis)

    limit_strain = section.timber.epsilonlim()

    if strain <= limit_strain:

        stress = 0.5 * section.connectionE() * strain * section.b * neutralAxis
        
    else:

        plastic = max(0, neutralAxis * (strain - limit_strain)/limit_strain)
        stress = limit_strain * 0.5 * section.b * section.connectionE() * (plastic + neutralAxis)

    return stress


def stressBalance(theta, neutralAxis, section):

    balance = timberStress(theta, neutralAxis, section) - sum(steelStress(theta, neutralAxis, section)) - tendonStress(theta, neutralAxis, section) - section.axialLoad

    return balance


def stressBalancePostFailure(theta, neutralAxis, section):

    balance = timberStress(theta, neutralAxis, section) - tendonStress(theta, neutralAxis, section) - section.axialLoad

    return balance







