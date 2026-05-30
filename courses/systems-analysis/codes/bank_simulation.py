"""
Bank Queue – Discrete Event Simulation
========================================
Event-based simulation of a bank with N tellers (as described in the slides).

Model
-----
  - Customers arrive according to a Poisson process
    (inter-arrival time ~ Exponential(1/lambda)).
  - Service time ~ Exponential(1/mu).
  - Single waiting queue; customers are assigned to the first free teller.
  - Simulation runs for a fixed virtual time horizon.

Concepts from the slides
------------------------
  - Event-based models with stochastic behaviour (Murphy's Law)
  - Embrace randomness: every run produces slightly different results

Usage
-----
  python bank_simulation.py
  python bank_simulation.py --tellers 3 --arrival 2.0 --service 4.5 --time 480

Dependencies: standard library only (no third-party packages required).
"""

import heapq
import random
import math
import argparse

# ---------------------------------------------------------------------------
# Simulation parameters (defaults)
# ---------------------------------------------------------------------------
DEFAULT_TELLERS      = 2
DEFAULT_ARRIVAL_RATE = 1.5    # customers per minute
DEFAULT_SERVICE_RATE = 0.8    # customers per minute per teller
DEFAULT_SIM_TIME     = 480    # minutes (an 8-hour bank day)
SEED                 = None   # set an int for reproducibility


# ---------------------------------------------------------------------------
# Event types
# ---------------------------------------------------------------------------
ARRIVAL  = "ARRIVAL"
DEPARTURE = "DEPARTURE"


# ---------------------------------------------------------------------------
# Exponential random variate helper
# ---------------------------------------------------------------------------
def exp_variate(rate: float) -> float:
    """Return a sample from Exponential(rate)."""
    return random.expovariate(rate)


# ---------------------------------------------------------------------------
# Simulation
# ---------------------------------------------------------------------------
def run_simulation(
    n_tellers: int,
    arrival_rate: float,
    service_rate: float,
    sim_time: float,
    seed: int | None = None,
    verbose: bool = False,
) -> dict:
    if seed is not None:
        random.seed(seed)

    # Event queue: (time, event_type, customer_id)
    events: list = []
    customer_id  = 0

    # Teller state: True = free
    tellers_free = n_tellers

    # Waiting queue (FIFO): list of (arrival_time, customer_id)
    waiting: list = []

    # Statistics collectors
    total_customers  = 0
    total_wait_time  = 0.0
    total_service_time = 0.0
    max_queue_length = 0
    teller_busy_time = [0.0] * n_tellers
    teller_free_since = [0.0] * n_tellers   # time each teller became free

    now = 0.0

    # Schedule first arrival
    heapq.heappush(events, (exp_variate(arrival_rate), ARRIVAL, customer_id))

    while events:
        t, etype, cid = heapq.heappop(events)

        if t > sim_time:
            break

        now = t

        if etype == ARRIVAL:
            total_customers += 1
            customer_id += 1

            # Schedule next arrival
            heapq.heappush(
                events,
                (now + exp_variate(arrival_rate), ARRIVAL, customer_id),
            )

            if tellers_free > 0:
                # Assign immediately to the first free teller
                teller_idx = next(
                    i for i in range(n_tellers) if teller_free_since[i] >= 0
                )
                tellers_free -= 1
                wait = 0.0
                total_wait_time += wait
                svc = exp_variate(service_rate)
                total_service_time += svc
                departure_t = now + svc
                teller_free_since[teller_idx] = -departure_t  # negative = busy
                heapq.heappush(
                    events,
                    (departure_t, DEPARTURE, teller_idx),
                )
                if verbose:
                    print(f"  t={now:7.2f}  Customer {cid:4d} → teller {teller_idx}"
                          f"  wait=0.00  svc={svc:.2f}")
            else:
                waiting.append((now, cid))
                max_queue_length = max(max_queue_length, len(waiting))
                if verbose:
                    print(f"  t={now:7.2f}  Customer {cid:4d} waits"
                          f"  queue={len(waiting)}")

        elif etype == DEPARTURE:
            teller_idx = cid   # 'cid' stores teller index for departures
            dep_time   = -teller_free_since[teller_idx]
            teller_busy_time[teller_idx] += dep_time - max(0.0, dep_time - exp_variate(service_rate))

            if waiting:
                arr_time, wcid = waiting.pop(0)
                wait = now - arr_time
                total_wait_time += wait
                svc = exp_variate(service_rate)
                total_service_time += svc
                departure_t = now + svc
                teller_free_since[teller_idx] = -departure_t
                heapq.heappush(
                    events,
                    (departure_t, DEPARTURE, teller_idx),
                )
                if verbose:
                    print(f"  t={now:7.2f}  Customer {wcid:4d} → teller {teller_idx}"
                          f"  wait={wait:.2f}  svc={svc:.2f}")
            else:
                tellers_free += 1
                teller_free_since[teller_idx] = now

    served = total_customers - len(waiting)
    avg_wait = total_wait_time / served if served else 0.0

    # Utilisation: fraction of sim_time each teller was busy
    utilisation = []
    for i in range(n_tellers):
        if teller_free_since[i] < 0:
            busy = (-teller_free_since[i]) - 0.0   # rough upper bound
        else:
            busy = sim_time - teller_free_since[i]
        utilisation.append(min(busy / sim_time, 1.0))

    return {
        "total_customers": total_customers,
        "served":          served,
        "abandoned":       len(waiting),
        "avg_wait_time":   avg_wait,
        "max_queue":       max_queue_length,
        "avg_utilisation": sum(utilisation) / n_tellers,
        "sim_time":        sim_time,
    }


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def print_report(params: dict, results: dict) -> None:
    sep = "=" * 55
    print(sep)
    print("  BANK SIMULATION — Discrete Event Model")
    print(sep)
    print(f"  Tellers        : {params['tellers']}")
    print(f"  Arrival rate   : {params['arrival_rate']:.2f} customers/min")
    print(f"  Service rate   : {params['service_rate']:.2f} customers/min/teller")
    print(f"  Simulation time: {params['sim_time']} min "
          f"({params['sim_time']/60:.1f} h)")
    print(sep)
    print(f"  Total arrivals : {results['total_customers']}")
    print(f"  Customers served: {results['served']}")
    print(f"  Still waiting  : {results['abandoned']}")
    print(f"  Avg wait time  : {results['avg_wait_time']:.2f} min")
    print(f"  Max queue length: {results['max_queue']}")
    print(f"  Avg teller util: {results['avg_utilisation']*100:.1f} %")
    print(sep)

    # Little's Law sanity check: L = lambda * W
    lam = params['arrival_rate']
    W   = results['avg_wait_time']
    L   = lam * W
    print(f"  [Little's Law]  L = λ·W ≈ {L:.2f} customers in queue")
    print(sep)


# ---------------------------------------------------------------------------
# Scenario sweep helper
# ---------------------------------------------------------------------------
def sweep_tellers(arrival_rate, service_rate, sim_time, max_tellers=6):
    print("\n  --- Teller count sensitivity ---")
    print(f"  {'Tellers':>7}  {'AvgWait(min)':>12}  {'MaxQueue':>9}  {'Util%':>6}")
    for n in range(1, max_tellers + 1):
        r = run_simulation(n, arrival_rate, service_rate, sim_time, seed=42)
        print(f"  {n:>7}  {r['avg_wait_time']:>12.2f}  "
              f"{r['max_queue']:>9}  {r['avg_utilisation']*100:>6.1f}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Bank discrete-event simulation")
    parser.add_argument("--tellers",  type=int,   default=DEFAULT_TELLERS)
    parser.add_argument("--arrival",  type=float, default=DEFAULT_ARRIVAL_RATE)
    parser.add_argument("--service",  type=float, default=DEFAULT_SERVICE_RATE)
    parser.add_argument("--time",     type=float, default=DEFAULT_SIM_TIME)
    parser.add_argument("--seed",     type=int,   default=SEED)
    parser.add_argument("--verbose",  action="store_true")
    parser.add_argument("--sweep",    action="store_true",
                        help="run sensitivity analysis varying teller count")
    args = parser.parse_args()

    params = {
        "tellers":      args.tellers,
        "arrival_rate": args.arrival,
        "service_rate": args.service,
        "sim_time":     args.time,
    }

    results = run_simulation(
        args.tellers, args.arrival, args.service, args.time,
        seed=args.seed, verbose=args.verbose,
    )
    print_report(params, results)

    if args.sweep:
        sweep_tellers(args.arrival, args.service, args.time)


if __name__ == "__main__":
    main()
