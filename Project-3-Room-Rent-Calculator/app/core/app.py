class Rent:
    def __init__(self, room_rent, food, wifi, electricity, no_person):
        self.room_rent = room_rent
        self.food = food
        self.wifi = wifi
        self.electricity = electricity
        self.no_person = no_person
        
    def equal_contri(self):
        contri_person = (self.room_rent+self.food+self.wifi+self.electricity)//self.no_person
        return f"Each person will pay {contri_person}" 
    
