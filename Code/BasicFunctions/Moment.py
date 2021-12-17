from BasicFunctions.StrainFunctions import timberStrain
from BasicFunctions.StressFunctions import steelStress, tendonStress


def timberBarycentre(theta, neutralAxis, section):

    strain = timberStrain(theta, neutralAxis, section) 
    
    plastic = max(0, neutralAxis * (strain - section.timber.epsilonlim(section.kcon))/section.timber.epsilonlim(section.kcon))

    barycentre = ((neutralAxis**2 - 2 * plastic**2 + plastic * neutralAxis)  * 1/3 + plastic**2)/ (plastic + neutralAxis)
    
    return barycentre


def steelMoment(theta, neutralAxis, section):

    stresses = steelStress(theta, neutralAxis, section)

    barycentre = timberBarycentre(theta, neutralAxis, section)

    moment = stresses[1] * (section.c - barycentre) + stresses[0] * (section.d() - barycentre)      # 0 Bottom, 1 Top

    return moment


def tendonMoment(theta, neutralAxis, section):

    stress = tendonStress(theta, neutralAxis, section)

    barycentre = timberBarycentre(theta, neutralAxis, section)

    moment = (section.h/2 - barycentre) * stress

    return moment


def axialLoadMoment(theta, neutralAxis, section):

    barycentre = timberBarycentre(theta, neutralAxis, section)

    moment = (section.h/2 - barycentre) * section.axialLoad

    return moment


