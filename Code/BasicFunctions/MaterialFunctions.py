from ImportFromJson import frame

# USEFULL CONSTANTS
m = frame.m
n = frame.n

# MATERIAL FUNCTIONS
def columnN(i):

    if i == 0 or i == n:

        return 1
    
    else:

        return 0


def columnS(i):

    if i == 0 or i == n:

        return 3
    
    else:

        return 2


def beamPT(j):

    return 2*(j + 1)


def beamS(j):

    return 2*(j + 1) + 1


def jointInternalLink(j):  

    return 2*(m + 1) + (j + 1)


def jointExternalLink(j):

    return 3*(m + 1) + j


def rigidLink():

    return 4*(m + 1)

def columnS_MinMax(i):

    if i == 0 or i == n:

        return 4*(m + 1) + 1
    
    else:

        return 4*(m + 1) + 2  


def beamS_MinMax(j):

    return 4*(m + 1) + 2*(j + 1) - 1


def beamPT_MinMax(j):

    return 4*(m + 1) + 2*(j + 1) 
