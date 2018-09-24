# Exercise 1 - Car Simulation
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Exercise 1 TESTS.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests,
and to be confident your code is correct.
"""
import unittest
from super_car import CarManager, Car


class TestCar(unittest.TestCase):

    def setUp(self):
        self.manager = CarManager()
        self.manager.add_car('car1', 2)
        self.manager.add_car('car2', 10)
        self.manager.add_car('car3', 20)
        self.manager.add_car('car4', 25)

    def test_initial_fuel(self):
        self.assertEqual(self.manager.get_car_fuel('car1'), 2)
        self.assertEqual(self.manager.get_car_fuel('car2'), 10)
        self.assertEqual(self.manager.get_car_fuel('car3'), 20)

    def test_initial_pos(self):
        pos = self.manager.get_car_position('car1')
        self.assertEqual(pos, (0, 0))

    def test_move_simple(self):
        self.manager.move_car('car2', 2, 3)
        pos = self.manager.get_car_position('car2')
        self.assertEqual(pos, (2, 3))
        self.assertEqual(self.manager.get_car_fuel('car2'), 5)

    def test_move_just_enough(self):
        self.manager.move_car('car1', 0, 2)
        pos = self.manager.get_car_position('car1')
        self.assertEqual(pos, (0, 2))
        self.assertEqual(self.manager.get_car_fuel('car1'), 0)

    def test_move_not_enough(self):
        self.manager.move_car('car1', 3, 5)
        pos = self.manager.get_car_position('car1')
        self.assertEqual(pos, (0, 0))
        self.assertEqual(self.manager.get_car_fuel('car1'), 2)


    #Other Test Cases
    #self.manager = CarManager()
    #    self.manager.add_car('car1', 2)
    #    self.manager.add_car('car2', 10)
    #    self.manager.add_car('car3', 20)
    def test_move_one_above(self):
        self.manager.move_car('car3',19,0)


    def test_move_just_one(self):
        self.manager.move_car('car1',3,5)
        self.assertEqual(self.manager.get_car_position('car2'), (0, 0))
        self.assertEqual(self.manager.get_car_fuel('car2'), 10)

        self.assertEqual(self.manager.get_car_position('car3'), (0, 0))
        self.assertEqual(self.manager.get_car_fuel('car3'), 20)




    def test_overlap(self):
        #Makes sure positions are equal
        self.manager.move_car('car2',2,3)
        self.manager.move_car('car3',2,3)
        self.assertEqual(self.manager.get_car_position('car2'),self.manager.get_car_position(('car3')))

    def test_incorrect_overlap(self):
        self.manager.move_car('car1',5,5)
        self.manager.move_car('car2',5,5)
        self.assertNotEqual(self.manager.get_car_position('car1'),self.manager.get_car_position('car2'))
        self.assertEqual(self.manager.get_car_position('car1'),self.manager.get_car_position('car3'))

    def test_negative_position(self):
        self.manager.move_car('car3',-10,-10)
        self.assertEqual((-10, -10),self.manager.get_car_position('car3'))


    def test_move_all_cars(self):
        #Tests just above, just enough, and not enough all at once, as well as negative, postitive, and both
        self.manager.move_car('car1', 5, 5)
        self.manager.move_car('car2', 5, -5)
        self.manager.move_car('car3', -5, 5)
        self.manager.move_car('car4', -5, -5)

        self.assertEqual((0, 0),self.manager.get_car_position('car1'))
        self.assertEqual(2,self.manager.get_car_fuel('car1'))

        self.assertEqual((5, -5),self.manager.get_car_position('car2'))
        self.assertEqual(0,self.manager.get_car_fuel('car2'))

        self.assertEqual((-5, 5),                        self.manager.get_car_position('car3'))
        self.assertEqual(10,self.manager.get_car_fuel('car3'))

        self.assertEqual((-5, -5),self.manager.get_car_position('car4'))
        self.assertEqual(15,self.manager.get_car_fuel('car4'))


    def test_you_only_move_twice(self):
        self.manager.move_car('car4',10,10)
        self.manager.move_car('car4',12,8)

        self.assertEqual((12, 8), self.manager.get_car_position('car4'))
        self.assertEqual(1, self.manager.get_car_fuel('car4'))

        self.manager.move_car('car4',10,10)

        self.assertEqual((12, 8), self.manager.get_car_position('car4'))
        self.assertEqual(1, self.manager.get_car_fuel('car4'))


    def test_from_negative_to_positive(self):
        #test values from +/- 25

        pos = (0, 0)
        fuel = 10
        for i in range(1,100):

            self.manager.move_car('car2',0, i)
            #if fuel is less than how far it needs to go, then the car fuel stays the same
            print(i)


            a=(fuel<abs(i))
            b=(self.manager.get_car_fuel('car2')==fuel and i!=0)
            print(a)
            print(b)

            self.assertEqual(a,b)


            print(self.manager.get_car_position('car2'))
            print(pos)
            a=pos != (self.manager.get_car_position('car2'))
            b=fuel>=abs(i)
            print(a)
            print(b)
            self.assertEqual(a, fuel>=abs(i))

            self.manager._cars['car2'].coordinates = (0,0)
            self.manager._cars['car2'].fuel =10
            #print (self.manager.get_car_position('car2'))
            #print(self.manager.get_car_fuel('car2'))

            #if the car moves, it hass enough fuel
            #if the car doesn't move, it doesn;t have enough fuel

            #if the car moves, it has enough fuel






if __name__ == '__main__':
    unittest.main()
