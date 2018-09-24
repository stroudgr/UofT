"""Assignment 1 - Grocery Store Simulation

CSC148 Fall 2015, University of Toronto
Instructor: David Liu
Student: Graeme Stroud
Student number: 1002552944
---------------------------------------------

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""

from container import PriorityQueue
from event import *


class GroceryStoreSimulation:
    """A Grocery Store simulation.
    """
    # === Private Attributes ===
    # @type _events: PriorityQueue[Event]
    #     A sequence of events arranged in priority determined by the event
    #     sorting order.
    # @type _store: GroceryStore
    #     The grocery store associated with the simulation.
    def __init__(self, store_file):
        """Initialize a GroceryStoreSimulation from a file.

        @type store_file: str
            A file containing the configuration of the grocery store.
        @rtype: None
        """
        self._events = PriorityQueue()
        self._store = GroceryStore(store_file)

    def run(self, event_file):
        """Run the simulation on the events stored in <event_file>.

        Return a dictionary containing statistics of the simulation,
        according to the specifications in the assignment handout.

        @type self: GroceryStoreSimulation
        @type event_file: str
            A filename referring to a raw list of events.
            Precondition: the event file is a valid list of events.
        @rtype: dict[str, object]
        """
        # Initialize statistics
        stats = {
            'num_customers': 0,
            'total_time': 0,
            'max_wait': -1
        }

        initial_events = create_event_list(event_file)

        # The initial events tells us how many customers went through the
        # simulation, since new Customers only join a line through a file.
        for event in initial_events:
            if type(event) == AddCustomerEvent:
                stats['num_customers'] += 1

        for item in initial_events:
            self._events.add(item)

        while not self._events.is_empty():

            current_event = self._events.remove()

            # Adds spawned events from doing the current event to the
            # simulation's PriorityQueue.
            new_events = current_event.do(self._store)
            for item in new_events:
                self._events.add(item)

            if type(current_event) == CheckOutCompleted:
                customer_time = current_event.wait_time
                if customer_time > stats['max_wait']:
                    stats['max_wait'] = customer_time

            # If current event is the final event, then the time it ends is the
            # amount of time the simulation took.
            if self._events.is_empty():
                stats['total_time'] = current_event.timestamp

        return stats


# We have provided a bit of code to help test your work.
if __name__ == '__main__':
    sim = GroceryStoreSimulation('config.json')
    final_stats = sim.run('events.txt')
    print(final_stats)
