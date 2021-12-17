class TimeHistoryAnalysis:

    def __init__(self, id, sf, dt, duration, timestepratio = 1, serializedid = 0):
        self.duration = duration               # Lunghezza del segnale
        self.dt = dt                        # Frequenza di campionamento
        self.id = id                        # Id accelerogramma per trovarlo trai file (vanno chiamati acc_[id].txt e va messa solo la colonna delle accelerazioni)
        self.sf = sf                        # Scale factor, ricorda che al programma servono in m/s2
        self.timestepratio = timestepratio  # Moltiplicatore del dt per il time step di analisi
        self.serializedid = serializedid    # Se la mando con SF diversi, non mi confonde le TS


    def steps(self):

        return round(self.duration / self.dt)

    
    def show(self):

        print(f'ID: {self.id} con ScaleFactor: {self.sf} | Campionamento: {self.dt}s Durata Segnale: {self.duration}s Analizza con un rapporto: {self.timestepratio}') 
