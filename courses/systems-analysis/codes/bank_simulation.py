"""
Bank Queue Simulation
A simple discrete-event simulation of a bank with multiple tellers.

Concepts used:
  - Queue: a waiting line where the first customer in is the first served (FIFO)
  - Events: things that happen at a specific point in time (arrival, departure)
  - Simulation: we skip time from event to event instead of ticking every second

How it works:
  1. Customers arrive at random times throughout the day.
  2. If a teller is free, the customer is served right away.
  3. If all tellers are busy, the customer joins the waiting queue.
  4. When a teller finishes, the next customer in the queue is served.
"""

import random


# Simulation settings
NUM_TELLERS  = 2
ARRIVAL_RATE = 1.5   # average customers arriving per minute
SERVICE_RATE = 0.8   # average customers a single teller serves per minute
SIM_TIME     = 480   # total simulation time in minutes (8-hour bank day)
SEED         = 42    # fixed seed so results are the same every run


# Event type labels
ARRIVAL   = "ARRIVAL"
DEPARTURE = "DEPARTURE"


class Customer:
    """Represents one bank customer."""

    def __init__(self, customer_id, arrival_time):
        self.customer_id  = customer_id
        self.arrival_time = arrival_time


class Queue:
    """
    A simple FIFO queue built on a Python list.

    enqueue  -> add to the back
    dequeue  -> remove from the front
    """

    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


class EventQueue:
    """
    Keeps simulation events ordered by time.

    Each event is stored as a list: [time, event_type, data].
    After adding a new event, we sort by time so the earliest
    event is always at index 0.
    """

    def __init__(self):
        self.events = []

    def schedule(self, time, event_type, data=None):
        self.events.append([time, event_type, data])
        self.events.sort(key=lambda e: e[0])

    def next_event(self):
        return self.events.pop(0)

    def is_empty(self):
        return len(self.events) == 0


class BankSimulation:
    """
    Runs a bank simulation with a fixed number of tellers
    and a single waiting queue for all customers.
    """

    def __init__(self, num_tellers, arrival_rate, service_rate, sim_time):
        self.num_tellers  = num_tellers
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.sim_time     = sim_time

        self.waiting_queue    = Queue()
        self.event_queue      = EventQueue()
        self.free_tellers     = num_tellers

        self.next_id          = 0
        self.total_arrivals   = 0
        self.total_served     = 0
        self.total_wait_time  = 0.0
        self.max_queue_length = 0

    def random_interarrival(self):
        """Random time (in minutes) until the next customer arrives."""
        return random.expovariate(self.arrival_rate)

    def random_service_time(self):
        """Random time (in minutes) needed to serve one customer."""
        return random.expovariate(self.service_rate)

    def run(self):
        """Start the simulation and return a summary of results."""
        now = 0.0

        # Schedule the very first arrival
        self.event_queue.schedule(self.random_interarrival(), ARRIVAL)

        while not self.event_queue.is_empty():
            time, event_type, _ = self.event_queue.next_event()

            if time > self.sim_time:
                break

            now = time

            if event_type == ARRIVAL:
                self.handle_arrival(now)
            elif event_type == DEPARTURE:
                self.handle_departure(now)

        return self.collect_results()

    def handle_arrival(self, now):
        """A new customer has just walked into the bank."""
        self.next_id        += 1
        self.total_arrivals += 1
        customer = Customer(self.next_id, now)

        # Always schedule the next customer arrival
        self.event_queue.schedule(now + self.random_interarrival(), ARRIVAL)

        if self.free_tellers > 0:
            self.serve(customer, now)
        else:
            self.waiting_queue.enqueue(customer)
            if self.waiting_queue.size() > self.max_queue_length:
                self.max_queue_length = self.waiting_queue.size()

    def handle_departure(self, now):
        """A teller has finished serving a customer."""
        self.free_tellers += 1   # teller is now free
        if not self.waiting_queue.is_empty():
            next_customer = self.waiting_queue.dequeue()
            self.serve(next_customer, now)   # serve will decrement free_tellers

    def serve(self, customer, now):
        """Assign a free teller to a customer and schedule their departure."""
        self.free_tellers    -= 1
        wait                  = now - customer.arrival_time
        self.total_wait_time += wait
        self.total_served    += 1
        service_time          = self.random_service_time()
        self.event_queue.schedule(now + service_time, DEPARTURE)

    def collect_results(self):
        avg_wait = (
            self.total_wait_time / self.total_served
            if self.total_served > 0
            else 0.0
        )
        return {
            "total_arrivals": self.total_arrivals,
            "total_served":   self.total_served,
            "avg_wait_time":  avg_wait,
            "max_queue":      self.max_queue_length,
        }


def print_report(results):
    print("=" * 45)
    print("  BANK SIMULATION RESULTS")
    print("=" * 45)
    print(f"  Customers arrived  : {results['total_arrivals']}")
    print(f"  Customers served   : {results['total_served']}")
    print(f"  Average wait time  : {results['avg_wait_time']:.2f} min")
    print(f"  Max queue length   : {results['max_queue']}")
    print("=" * 45)


if __name__ == "__main__":
    random.seed(SEED)

    sim = BankSimulation(NUM_TELLERS, ARRIVAL_RATE, SERVICE_RATE, SIM_TIME)
    results = sim.run()
    print_report(results)
