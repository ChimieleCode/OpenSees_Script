from ImportFromJson import frame

# USEFULL CONSTANTS
n = frame.n
m = frame.m

# NODES FUNCTIONS
def nodeGrid(i, j):

    return j*(n + 1) + i


def nodeBase(i):

    return (m + 1)*(n + 1) + i


def nodePanel(i, j):

    return (m + j + 1)*(n + 1) + i


def nodeRigidBeam(i, j, l):

    return (2*m + 1)*(n + 1) + n*(2*j - 1) + 2*i - (1 - l)


def nodeBeam(i, j, l):

    return (2*m + 1)*(2*n + 1) + 2*n*(j - 1) + 2*i - (1 - l)


def nodeColumn(i, j, l):

    return 2*(i + (j - 1)*(n + 1) + n*m + 1) + (2*m + 1)*(2*n + 1) - (1 - l)


def nodeTopColumn(i):

    return 4*m*(2*n + 1) + i
