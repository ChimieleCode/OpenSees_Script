# Poly MUST be defined as [ [x_values], [y_values]]

def polyArea(poly):

    n = len(poly[0])
    sum = 0

    for i in range(n - 1):

        sum += 0.5 * (poly[0][i]*poly[1][i + 1] - poly[0][i + 1]*poly[1][i])


    # Punto di chiusura    
    sum += 0.5 * (poly[0][-1]*poly[1][0] - poly[0][0]*poly[1][-1])

    return abs(sum)