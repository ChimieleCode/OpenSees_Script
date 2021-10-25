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