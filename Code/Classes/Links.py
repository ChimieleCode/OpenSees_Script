class KineticLink:

    def __init__(self, Fy, E0, Hiso = 0, Hkin = 0, strainLimit = 3.14):

        self.Fy = Fy                                # Momento di snervamento
        self.E0 = E0                                # Rigidezza elastica
        self.Hiso = Hiso                            # Parametro di incrudimento isteretico
        self.Hkin = Hkin                            # Parametro di incrudimento plastico
        self.strainLimit = strainLimit              # Rotazione a rottura dei dissipatori
        

    def show(self):

        print(f'Parametri Hardening Fy: {self.Fy}kNm E0: {self.E0}kNm/rad Hiso: {self.Hiso} Hkin:{self.Hkin}') 


    
class MultilinearElasticLink:

    def __init__(self, strain = [0], stress = [0]):

        self.strain = strain                        # Rotazioni in rad
        self.stress = stress                        # Momenti in kNm
        

    def show(self):

        print(f'Punti Strain: {self.strain}rad Stress: {self.stress}kNm') 



class GMSteelLink:

    def __init__(self, Fy, E0, b, r0 = 20, cr1 = 0.925, cr2 = 0.15, strainLimit = 3.14):

        self.Fy = Fy                                # Momento di snervamento
        self.E0 = E0                                # Rigidezza elastica
        self.b = b                                  # Rapporto tra rigidezza plastica ed elastica
        self.r0 = r0
        self.cr1 = cr1
        self.cr2 = cr2
        self.strainLimit = strainLimit              # Rotazione che porta al fallimento i dissipatori
        

    def show(self):

        print(f'Parametri G-M Fy: {self.Fy}kNm E0: {self.E0}kNm/rad b: {self.b} r0: {self.r0} cr1: {self.cr1} cr2: {self.cr2}') 
