class Commande():
    def __init__(self, date, prix, quant, coute, no_comm):
        self.date = date
        self.prix = prix
        self.quant = quant
        self.coute = 0.0
        self.no_comm = ''
        self.valide = 
    
    def valide(self):
        if (self.coute == '') or (self.no_comm == ''):
            return False
        
        self.coute = float()
        
