import math
from ModelOptions import csi
from BasicFunctions.ConsistentTimeSeries import consistentTimeSeries

g = 9.81

def spectralAcceleration(time_history, structure_period):

    # Ottengo l'accelerogramma da fare con consistent TH
    base_acc = consistentTimeSeries(timehistory = time_history)

    base_acc = [(a / g) for a in base_acc]

    # Calcolo parametri per SDOF direct integration
    omega_0 = 2 * math.pi / structure_period
    unit_mass = 1
    force = [(-unit_mass * a * g) for a in base_acc]
    k = unit_mass * omega_0**2
    c = 2 * csi * unit_mass * omega_0

    # Parametri di integrazione
    A = unit_mass / time_history.dt**2
    B = c / (2 * time_history.dt)

    # Inizializzo i vettori, per motivi di integrazione alcuni zeri vanno dati
    u_r = [0., 0.]
    a_r = [0.]

    # Calcolo gli spostamenti relativi
    for i in range(1, len(base_acc) - 1):

        u_r.append(1/(A + B) * (force[i] - u_r[i] * (k - 2*A) - u_r[i - 1] * (A - B)))


    # Calcolo le accelerazioni relative
    for i in range(1, len(base_acc) - 1):

        a_r.append((u_r[i + 1] + u_r[i - 1] - 2*u_r[i]) / (time_history.dt**2 * g))

    # Serve per portare a_r alla stessa grandezza di base_acc
    a_r.append(0.)

    # Calcolo il Max dell'accelerazione assoluta
    Sa = max([abs(a_r[i] + base_acc[i]) for i in range(len(a_r))])

    return Sa

    
