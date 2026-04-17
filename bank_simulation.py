import argparse
import queue
import threading
from dataclasses import dataclass, field
from typing import Optional

NUM_TELLERS = 3
NUM_CUSTOMERS = 50


@dataclass
class CustomerState:
    customer_id: int
    transaction: str
    assigned_teller: Optional[int] = None
    called_by_teller: threading.Semaphore = field(default_factory=lambda: threading.Semaphore(0))
    introduced_self: threading.Semaphore = field(default_factory=lambda: threading.Semaphore(0))


class BankSimulation:
    def __init__(self, num_customers=NUM_CUSTOMERS):
        self.num_customers = num_customers
        self.print_lock = threading.Lock()

        self.bank_open = threading.Event()
        self.ready_count = 0
        self.ready_lock = threading.Lock()

        self.customer_line = queue.Queue()
        self.teller_threads = []
        self.customer_threads = []

    def log(self, actor_type, actor_id, partner_type, partner_id, msg):
        if partner_type is None or partner_id is None:
            partner = "[]"
        else:
            partner = f"[{partner_type} {partner_id}]"

        with self.print_lock:
            print(f"{actor_type} {actor_id} {partner}: {msg}", flush=True)

    def teller(self, teller_id):
        self.log("Teller", teller_id, None, None, "ready to serve")

        with self.ready_lock:
            self.ready_count += 1
            if self.ready_count == NUM_TELLERS:
                self.bank_open.set()

        self.log("Teller", teller_id, None, None, "waiting for a customer")
        customer = self.customer_line.get()

        customer.assigned_teller = teller_id
        customer.called_by_teller.release()

        customer.introduced_self.acquire()
        self.log("Teller", teller_id, "Customer", customer.customer_id, "serving a customer")

    def customer(self, customer_id):
        self.bank_open.wait()

        state = CustomerState(customer_id=customer_id, transaction="deposit")

        self.log("Customer", customer_id, None, None, "going to bank.")
        self.log("Customer", customer_id, None, None, "getting in line.")

        self.customer_line.put(state)

        state.called_by_teller.acquire()
        teller_id = state.assigned_teller

        self.log("Customer", customer_id, None, None, "selecting a teller.")
        self.log("Customer", customer_id, "Teller", teller_id, "selects teller")
        self.log("Customer", customer_id, "Teller", teller_id, "introduces itself")
        state.introduced_self.release()

    def run(self):
        for teller_id in range(NUM_TELLERS):
            t = threading.Thread(target=self.teller, args=(teller_id,))
            self.teller_threads.append(t)
            t.start()

        for customer_id in range(self.num_customers):
            t = threading.Thread(target=self.customer, args=(customer_id,))
            self.customer_threads.append(t)
            t.start()

        for t in self.customer_threads:
            t.join()

        for t in self.teller_threads:
            t.join()


def main():
    parser = argparse.ArgumentParser(description="CS4348 Project 2 bank simulation")
    parser.add_argument("--customers", type=int, default=NUM_CUSTOMERS)
    args = parser.parse_args()

    sim = BankSimulation(num_customers=args.customers)
    sim.run()


if __name__ == "__main__":
    main()