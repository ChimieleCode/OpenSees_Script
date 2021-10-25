class Section:

    def __init__(self, h, b, Emat, Fy, E0, strain = [] , stress = [], Hiso = 0, Hkin = 0 ):

        self.h = h              # Altezza della sezione in m
        self.b = b              # Larghezza della Sezione in m
        self.Emat = Emat        # Modulo di Young in kPa
        self.Fy = Fy            # Momento di snervamento della connessione in kNm
        self.E0 = E0            # Rigidezza elastica della connessione in kNm/rad
        self.strain = strain    # Punti Strain del legame ricentrante, default vuoto in rad
        self.stress = stress    # Punti Stress del legame ricentrante, default vuoto in kNm
        self.Hkin = Hkin        # Fattore di incrudimento cinematico
        self.Hiso = Hiso        # Fattore di incrudimento isteretico [lasciare 0]

    
    def area(self):     # Calcola l'area della sezione

        area = self.b * self.h

        return area


    def inertia(self):  # Calcola l'inerzia della sezione 

        inertia = 1/12 * self.b * self.h**3

        return inertia


    def show(self):

        print(f'Sezione {self.h}x{self.b}m con Modulo di Young: {self.Emat}kPa | Parametri Hardening Fy: {self.Fy}kNm E0: {self.E0}kNm/rad Hiso: {self.Hiso} Hkin:{self.Hkin} ---\n--- Curva Stress: {self.stress}kNm Curva Strain: {self.strain}rad \n') 
