from ImportFromJson import frame

# USEFULL CONSTANTS
m = frame.m

# MATERIAL FUNCTIONS
def columnN():

    return 1


def columnS():

    return 2


def beamPT(j):

    return 2*j + 1


def beamS(j):

    return 2*(j + 1)


def jointLink(j):       # Assunto che tutti i link allo stesso piano siano uguali

    return 2*(m + 1) + j


def rigidLink():

    return 3*(m + 1)
