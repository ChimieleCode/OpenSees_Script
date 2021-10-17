class Frame:

    def __init__(self, span, storey, n, m, r = 1, mass = [0], Heff = 1, damping = 0.05):
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


frame = Frame(11, 4, 2, 5, 2, [0, 140.8, 140.8], 4)

m = frame.m

def inelasticShape(frame):
    shape = []
    for j in range(1,m + 1):            # j da 1 a m 
        if m <= 4:
            shape.append(j*frame.storey/frame.height())
        else:
            shape.append(4/3 * (j*frame.storey/frame.height()) * (1 - j*frame.storey/frame.height() * 1/4))
    return shape

print(inelasticShape(frame))