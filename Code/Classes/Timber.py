class Timber:

    def __init__(self, parallelStrength, E, G):

        self.parallelStrength = parallelStrength        # fbt in kPa 
        self.E = E                                      # E in kPa 
        self.G = G                                      # G in kPa 


    def epsilonlim(self):

        epsilon = self.parallelStrength / self.E

        return epsilon

    
    def show(self):

        print(f'Strength: {self.parallelStrength}kPa E: {self.E}kPa G: {self.G}kPa') 
