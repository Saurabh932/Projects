class Rent:
    def __init__(self, room_rent, food, wifi, elec_bill, no_person):
        self.room_rent = room_rent
        self.food = food
        self.wifi = wifi
        self.elec_bill = elec_bill
        self.no_person = no_person
        
    def equal_contri(self):
        contri_person = (self.room_rent+self.food+self.wifi+self.elec_bill)//self.no_person
        return f"Each person will pay {contri_person}" 
    
