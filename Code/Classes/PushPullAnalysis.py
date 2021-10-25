
class PushPullAnalysis:

    def __init__(self, points = [], step = 0.001 , pattern = []):
        
        self.points = points            # Curva degli spostamenti obiettivo per pushover [m]
        self.step = step                # Grandezza step per la transizione [m]
        self.pattern = pattern          # Pattern unitario di forze (solo fuori terra, si esclude il pian terreno)

    def show(self):

        print(f'Points: {self.points} con Step: {self.step} | Pattern di Pushover: {self.pattern}') 