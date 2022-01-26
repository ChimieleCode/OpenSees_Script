from scipy.optimize import fsolve

def interpolator(value , x_series, y_series):

    if not(len(x_series) == len(y_series)):

        print('x and y must have the same lenght')

        return 'ERR'


    for i in range(1, len(x_series)):

        if (value <= x_series[i]) and (value >= x_series[i - 1]):

            return (y_series[i] - y_series[i - 1]) / (x_series[i] - x_series[i - 1]) * (value - x_series[i - 1]) + y_series[i - 1]
        
        else:

            continue

    # Se arrivo qui vuol dire che non ho trovato un match
    print('ERROR: Value out of range')
    return 0


def oldintersection(x1_series, y1_series, x2_series, y2_series, initial_guess = 0):

    if not(len(x1_series) == len(y1_series) and len(x2_series) == len(y2_series)):

        print('x and y must have the same lenght')

        return 'ERR'

    else:

        def objective(x):

            return interpolator(x, x1_series, y1_series) - interpolator(x, x2_series, y2_series)

        x = fsolve(objective, initial_guess)
        y = interpolator(x, x1_series, y1_series)

        return [x, y]


def intersection(x1_series, y1_series, x2_series, y2_series):

    if not(len(x1_series) == len(y1_series) and len(x2_series) == len(y2_series)):

        print('x and y must have the same lenght')

        return 'ERR'

    else:

        step = x1_series[1] - x1_series[0]

        for i in range(1, len(x1_series)):

            yP1 = y1_series[i - 1]
            yP2 = y1_series[i]

            yB1 = interpolator(x1_series[i - 1], x2_series, y2_series)
            yB2 = interpolator(x1_series[i], x2_series, y2_series)

            if (yP1 - yB1)*(yP2 - yB2) < 0:
                
                A = (yP2 - yP1)/step
                B = (yB2 - yB1)/step

                x_intersection = (yB1 - yP1)/(A - B) + x1_series[i - 1]

                return x_intersection, interpolator(x_intersection, x1_series, y1_series)
            
            else:

                continue

