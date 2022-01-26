# FUNZIONE PER DEFINIRE LA DEFORMATA DI PUSHOVER (PATTERN)

def inelasticShape(frame):

    m = frame.m

    shape = []

    for j in range(1,m + 1):            # j da 1 a m 

        if m <= 4:

            shape.append(j*frame.storey/frame.height())

        else:

            shape.append(4/3 * (j*frame.storey/frame.height()) * (1 - j*frame.storey/frame.height() * 1/4))

    return shape


def getEffectiveHeight(frame):

    m = frame.m

    shape = inelasticShape(frame)

    mass = frame.mass

    H = [i * frame.storey for i in range(1, m + 1)]

    MD = [a * b for a,b in zip(shape, mass)]

    MDH = [a * b for a,b in zip(MD, H)]
    
    Heff = sum(MDH)/sum(MD)

    return Heff

    
def getEffectiveMass(frame):

    m = frame.m

    shape = inelasticShape(frame)

    mass = frame.mass

    MD = [a * b for a,b in zip(shape, mass)]

    MD2 = [a * b for a,b in zip(MD, shape)]

    Meff = sum(MD)**2/sum(MD2)

    return Meff

