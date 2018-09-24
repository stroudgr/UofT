# Exercise 2 - A Chain of People
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Exercise 2, Task 2 TESTS.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests,
and to be confident your code is correct!

The most important thing is to make sure your code is correct on inputs of any size, including ones that are very very small.



"""
import unittest
from chain import PeopleChain, ShortChainError


class TestPeopleChain(unittest.TestCase):

    def setUp(self):
        self.chain = PeopleChain(['Iron Man', 'Janna', 'Kevan'])
        self.empty_chain = PeopleChain([])
        self.one_chain = PeopleChain(['David'])
        self.two_chain = PeopleChain(['Karen', 'Paul'])

    def test_get_leader_simple(self):
        self.assertEqual(self.chain.get_leader(), 'Iron Man')

    def test_get_second_simple(self):
        self.assertEqual(self.chain.get_second(), 'Janna')

    def test_get_third_simple(self):
        self.assertEqual(self.chain.get_third(), 'Kevan')

    def test_get_third_empty(self):
        # Note: this is a test which checks to see if an error is raised.
        with self.assertRaises(ShortChainError):
            # This code is run. A ShortChainError is expected to be raised here.
            self.empty_chain.get_third()



    def test_get_second_empty(self):
        with self.assertRaises(ShortChainError):
            self.empty_chain.get_second()

    #def test_get_nth_simple(self):

    def test_get_nth_empty(self):
        with self.assertRaises(ShortChainError):
            self.empty_chain.get_nth(4)

    def test_get_nth_simple(self):
        #Iron Man, Janna, Kevan
        self.assertEqual(self.chain.get_nth(1),"Iron Man")
        self.assertEqual(self.chain.get_nth(2),"Janna")
        self.assertEqual(self.chain.get_nth(3),"Kevan")

    def test_nth_equals(self):
        #Tests whether getnth(2) does the same as get2cd

        self.assertEqual(self.two_chain.get_second(),self.two_chain.get_nth(2))
        self.assertEqual(self.chain.get_third(),self.chain.get_nth(3))
        self.assertEqual(self.chain.get_second(),self.chain.get_nth(2))
        self.assertEqual(self.chain.get_leader(),self.chain.get_nth(1))


    def test_leader(self):
        chain = PeopleChain(["Iron Man"])
        self.assertEqual(chain.get_nth(1),"Iron Man")
        self.assertEqual(chain.get_nth(1),chain.get_leader())

    def test_empty_chain(self):
        chain = PeopleChain([])
        with self.assertRaises(ShortChainError):
            a = chain.get_leader()

    def test_limits(self):
        # Test how close it can be while returning false

        names = ['a','b','c','d','e','f','g','h','i','j']

        for i in range(1, len(names)):
            lst = []
            # Adds <i> items to a list, then to the chain
            for j in range(i):
                lst.append(names[j])
            chain = PeopleChain(lst)

            for k in range(i+10):
                # If we're in range of the chain
                if k<i:
                    self.assertEqual(chain.get_nth(k+1),names[k])
                # If were are out of range of the chain
                else:
                    with self.assertRaises(ShortChainError):
                        a = chain.get_nth(k+1)


    def test_everything(self):
        self.chain = PeopleChain(['Iron Man', 'Janna', 'Kevan'])
        self.empty_chain = PeopleChain([])
        self.one_chain = PeopleChain(['David'])
        self.two_chain = PeopleChain(['Karen', 'Paul'])


        self.assertEqual(self.chain.get_leader(),'Iron Man')
        self.assertEqual(self.chain.get_second(),'Janna')
        self.assertEqual(self.chain.get_third(),'Kevan')
        self.assertEqual(self.chain.get_leader(),self.chain.get_nth(1))
        self.assertEqual(self.chain.get_second(),self.chain.get_nth(2))
        self.assertEqual(self.chain.get_third(),self.chain.get_nth(3))
        with self.assertRaises(ShortChainError):
            self.chain.get_nth(4)



        with self.assertRaises(ShortChainError):
            self.empty_chain.get_nth(1)
        with self.assertRaises(ShortChainError):
            self.empty_chain.get_leader()

        self.assertEqual(self.one_chain.get_leader(),'David')
        self.assertEqual(self.one_chain.get_leader(),self.one_chain.get_nth(1))
        with self.assertRaises(ShortChainError):
            self.one_chain.get_nth(2)
        with self.assertRaises(ShortChainError):
            self.one_chain.get_second()


        self.assertEqual(self.two_chain.get_leader(),'Karen')
        self.assertEqual(self.two_chain.get_second(),'Paul')
        self.assertEqual(self.two_chain.get_leader(),self.two_chain.get_nth(1))
        self.assertEqual(self.two_chain.get_second(),self.two_chain.get_nth(2))
        with self.assertRaises(ShortChainError):
            self.two_chain.get_nth(3)

    def test_random_things(self):
        p = PeopleChain(["Graeme", "Robert", "Cheryl","David"])


        self.assertEqual("Graeme",p._leader.name,p.get_leader())
        self.assertEqual(p._leader.name,p.get_leader(),
p.get_nth(1))
        self.assertEqual(p._leader.next.name, "Robert")

        self.assertEqual("Robert",p._leader.next.name,p.get_second())
        self.assertEqual(p._leader.next.name,p.get_second(), p.get_nth(2))
        self.assertEqual(p._leader.next.next.name, "Cheryl")

        self.assertEqual("Cheryl",p._leader.next.next.name,p.get_third())
        self.assertEqual(p._leader.next.next.name,p.get_third(),
p.get_nth(3))
        self.assertEqual(p._leader.next.next.next.name, "David")




if __name__ == '__main__':
    unittest.main(exit=False)
