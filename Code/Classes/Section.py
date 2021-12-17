import math

class Section:

    lambdaBar = 60

    def __init__(self, h, b, kcon, steelBarNumber, steelBarDiameter, c, timber, steel, tendon = None, ptNumber = 0, ptTension = 0, axialLoad = 0, multilinearElasticLink = None, kineticLink = None, GMLink = None, isBeam = None):

        self.h = h                                  # Altezza della sezione in m
        self.b = b                                  # Larghezza della Sezione in m
        self.c = c                                  # Distance between top reinforcement and top of the section [negative means external bars]
        self.kcon = kcon                            # k connessione [in base al tipo]
        self.steelBarNumber = steelBarNumber        # Numero di dissipatori per lato (considerati simmetrici)
        self.steelBarDiameter = steelBarDiameter    # Diametro della signola barra
        self.ptNumber = ptNumber                    # Numero di cavi di post-tensione
        self.ptTension = ptTension                  # Initial tension
        self.timber = timber                        # Timber
        self.steel = steel                          # Steel
        self.tendon = tendon                        # Cable
        self.axialLoad = axialLoad                  # Carico assiale sulla sezione
        self.multilinearElasticLink = multilinearElasticLink
        self.kineticLink = kineticLink
        self.GMLink = GMLink
        self.isBeam = isBeam                        # Se è una trave == True
        
    
    def area(self):     # Calcola l'area della sezione

        area = self.b * self.h

        return area


    def inertia(self):  # Calcola l'inerzia della sezione 

        inertia = 1/12 * self.b * self.h**3

        return inertia


    def steelArea(self):    # Calcola l'area dell'acciaio

        area = (self.steelBarDiameter * 0.001)**2 * math.pi * self.steelBarNumber/4

        return area

    
    def postTensionArea(self):      # Calcola l'area del tendon

        try:

            area = self.tendon.area * self.ptNumber
        
        except:

            area = 0

        return area

    
    def tendonInitialStrain(self):

        try:

            strain = self.ptTension / (self.ptNumber * self.tendon.area * self.tendon.E)

        except:

            strain = 0

        return strain


    def connectionE(self):

        E = self.timber.E * self.kcon

        return E
        

    def barLength(self):

        length = self.steelBarDiameter * (10**-3) * self.lambdaBar/4

        return length


    def d(self):

        d = self.h - self.c

        return d


    def show(self):

        print(f'Sezione {self.h}x{self.b}m Connessione: {self.kcon} | Armature: {self.steelBarNumber}f{self.steelBarDiameter} Copriferro: {self.c}m | Tpti: {self.ptTension}kN Trefoli: {self.ptNumber} Assiale: {self.axialLoad} \n Timber: {self.timber} Tendon: {self.tendon} Steel: {self.steel} Link ricentrante: {self.multilinearElasticLink} Link dissipante: {self.kineticLink}') 
