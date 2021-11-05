from BasicFunctions.StressFunctions import stressBalance, stressBalancePostFailure
from BasicFunctions.StrainFunctions import steelStrain, tendonStrain, timberStrain

from scipy.optimize import fsolve

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# Snervamento dell'acciaio
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

def steelYielding(initialGuess, section):

    def objectiveYielding(input):

        theta = input[0]
        neutralAxis = input[1]

        output = []

        output.append(stressBalance(theta, neutralAxis, section))

        output.append(steelStrain(theta, neutralAxis, section)[0] - section.steel.yieldStrain())

        return output

    x = fsolve(objectiveYielding, initialGuess, xtol= 10**-6, maxfev=10000)
    # print(x)
    return x

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# Fallimento dell'acciaio
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

def steelFailure(initialGuess, section):

    def objectiveFailure(input):

        theta = input[0]
        neutralAxis = input[1]

        output = []

        output.append(stressBalance(theta, neutralAxis, section))

        output.append(steelStrain(theta, neutralAxis, section)[0] - section.steel.ultimateStrain)

        return output

    x = fsolve(objectiveFailure, initialGuess, xtol= 10**-6, maxfev=10000)
    # print(x)
    return x

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# Snervamento del cavo
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

def tendonYielding(initialGuess, section):

    def objectiveTendon(input):

        theta = input[0]
        neutralAxis = input[1]

        output = []

        output.append(stressBalancePostFailure(theta, neutralAxis, section))

        output.append(tendonStrain(theta, neutralAxis, section) - section.tendon.yieldStrain())

        return output

    x = fsolve(objectiveTendon, initialGuess, xtol= 10**-6, maxfev=10000)
    # print(x)
    return x

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# Snervamento del Legno
# --------------------------------------------------------------------------------------------------------------------------------------------------------------

def timberYielding(initialGuess, section):

    def objectiveTimber(input):

        theta = input[0]
        neutralAxis = input[1]

        output = []

        output.append(stressBalance(theta, neutralAxis, section))

        output.append(timberStrain(theta, neutralAxis) - section.timber.epsilonlim())

        return output

    x = fsolve(objectiveTimber, initialGuess, xtol= 10**-6, maxfev=10000)
    # print(x)
    return x

