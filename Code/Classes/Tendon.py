class Tendon:
        
    def __init__(self, yieldStress, E, area):

        self.yieldStress = yieldStress                  # fpty in kPa 
        self.E = E                                      # E in kPa 
        self.area = area * 10**-6                        # area va dichiarata in mm quadri


    def yieldStrain(self):

        epsilon = self.yieldStress / self.E

        return epsilon

    
    def show(self):

        print(f'YieldStress: {self.yieldStress}kPa E: {self.E}kPa area: {round(self.area * 10**6)}mm2') 
