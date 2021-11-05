
class Steel:

    E = 210000000           # Young in kPa

    def __init__(self, yieldStress, r = 0, ultimateStrain = 0.06):
        
        self.yieldStress = yieldStress          # Curva degli spostamenti obiettivo per pushover [m]
        self.r = r                              # Grandezza step per la transizione [m]
        self.ultimateStrain = ultimateStrain    # Pattern unitario di forze (solo fuori terra, si esclude il pian terreno)


    def yieldStrain(self):

        strain = self.yieldStress/self.E

        return strain


    def show(self):

        print(f'YieldStress: {self.yieldStress}kPa r: {self.r} ultimateStrain: {self.ultimateStrain} E: {self.E}kPa') 