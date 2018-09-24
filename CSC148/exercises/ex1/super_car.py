# Exercise 1 - Car Simulation
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# Student: Graeme Stroud
# Student number: 1002552944
# ---------------------------------------------
import doctest

class CarManager:
    """A class responsible for keeping track of all cars in the system.
    """
    # === Private Attributes ===
    # @type _cars: dict[str, Car]
    #     A map of unique string identifiers to the corresponding cars.
    def __init__(self):
        """Create a new CarManager.

        Initially there are no cars in the system.

        @type self: CarManager
        @rtype: None
        """
        self._cars = {}

    def add_car(self, id, fuel):
        """Add a new car to the system.

        The new car is identified by the string <id>, and has initial amount
        of fuel <fuel>.

        Do nothing if there is already a car with the given id.

        @type self: CarManager
        @type id: str
        @type fuel: int
        @rtype: None
        """
        # Check to make sure the identifier isn't already used.
        if id not in self._cars:
            # Add the new car here.
            self._cars[id] = Car(fuel,0,0)


    def move_car(self, id, new_x, new_y):
        """Move a car in the system.

        The car called <id> should be moved to position (<new_x>, <new_y>).

        @type self: CarManager
        @type id: str
        @type new_x: int
        @type new_y: int
        @rtype: None
        >>> car_man = CarManager()
        >>> car_man.add_car("Volkswagen",10)
        >>> car_man.move_car("Volkswagen",5,2)
        >>> car_man.get_car_fuel("Volkswagen")
        3
        >>> car_man.get_car_position("Volkswagen")
        (5, 2)

        """
        if id in self._cars:

            car = self._cars[id]

            #Finds the change in position of x and y from tuple (x,y)
            delta_x = abs(new_x - car.coordinates[0])
            delta_y = abs(new_y - car.coordinates[1])

            #Calculates new fuel
            new_fuel = car.fuel - delta_x - delta_y

            #Only move car (and use fuel) if the car has just enough
            if new_fuel >= 0:
                car.fuel = new_fuel
                car.coordinates = (new_x,new_y)
            else:
                pass

    def get_car_position(self, id):
        """Return the position of car <id> in the system.

        Return a tuple of the (x, y) position of the car.

        @type self: CarManager
        @type id: str
        @rtype: (int, int)
        """
        if id in self._cars:
            return self._cars[id].coordinates


    def get_car_fuel(self, id):
        """Return the amount of fuel of car <id> in the system.

        @type self: CarManager
        @type id: str
        @rtype: int
        """
        if id in self._cars:
            return self._cars[id].fuel


class Car:
    """A car in the Super system.

    Fill in the public or private attributes for this class!
    === Public Attributes ===
    @type fuel: int
        The amount of fuel a car has
    @type coordinates: (int,int)
        The (x,y) coordinates of the car

    """
    # === Representation Invariants ===
    #Fuel must be greater or equal to zero

    def __init__(self,fuel,x,y):
        """Initializes a car. Sets fuel and position
        @type fuel: int
        @type x: int
        @type y:int
        @rtype: None
        """
        self.fuel = fuel
        self.coordinates = (x,y)


if __name__ == '__main__':
    car_man = CarManager()
    car_man.add_car("Volkswagen",5)
    car_man.get_car_fuel()
    car_man.get_car_position()
    car_man.move_car(2,2)
    car_man.move_car(3,1)
    car_man.get_car_position()
    doctest.testmod()
