"""
Description: Create a Car class. The constructor __init__ should accept make, model, and year.
Add a @classmethod named from_string(cls, car_string). This method should take a string like "Toyota-Camry-2021" and return a new instance of the Car class.
Add a @staticmethod named is_antique(year). This method should return True if the provided year is older than 25 years from the current year (2025), and False otherwise.
"""

class Car():
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        
    @classmethod
    def from_string(cls, car_string):
        make, model, year = car_string.split('-')
        return cls(make, model, int(year))
    
    @staticmethod
    def is_antique(year):
        return (2025 + year) > 25
    
car_string = input("Enter car details (make-model-year): ")
car = Car.from_string(car_string)
print("Car created:", car.make, car.model, car.year)

year = int(input("Enter a year to check if it's antique: "))
if Car.is_antique(year):
    print("The car is antique.")
else:
    print("The car is not antique.")
