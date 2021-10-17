
class Frame:

    def __init__(self, span, storey, n, m, Heff = 0, mass = [0], r = 1, damping = 0.05):
        self.span = span                # Altezza di interpiano
        self.storey = storey            # Lunghezza della campata
        self.n = n                      # Numero di campate
        self.m = m                      # Numero di piani
        self.r = r                      # Numero di Telai in parallelo
        self.damping = damping          # Damping del Telaio per Rayleigh
        self.Heff = Heff                # Heff dello SDOF
        self.mass = mass                # Masse di piano da piano terra in tonnellate (La prima entrata viene ignorata, si raccomanda di mettere 0)

    def height(self):       # Calcola l'altezza del telaio
        height = self.m * self.storey
        return height

    def length(self):       # Calcola la lunghezza del telaio
        length = self.n * self.span 
        return length

    def show(self):
        print(f'Telaio Campata: {self.span}m Altezza di interpiano: {self.storey}m Piani: {self.m} Campate: {self.n} Telai in Parallelo: {self.r} Heff: {self.Heff} Damping: {self.damping} Masse di piano: {self.mass}ton') 
