import argparse
import threading

NUM_TELLERS = 3
NUM_CUSTOMERS = 50


class BankSimulation:
    def __init__(self, num_customers=NUM_CUSTOMERS):
        self.num_customers = num_customers
        self.print_lock = threading.Lock()

    def log(self, actor_type, actor_id, partner_type, partner_id, msg):
        if partner_type is None or partner_id is None:
            partner = "[]"
        else:
            partner = f"[{partner_type} {partner_id}]"

        with self.print_lock:
            print(f"{actor_type} {actor_id} {partner}: {msg}", flush=True)

    def run(self):
        self.log("Teller", 0, None, None, "ready to serve")
        self.log("Customer", 0, None, None, "going to bank.")


def main():
    parser = argparse.ArgumentParser(description="CS4348 Project 2 bank simulation")
    parser.add_argument("--customers", type=int, default=NUM_CUSTOMERS)
    args = parser.parse_args()

    sim = BankSimulation(num_customers=args.customers)
    sim.run()


if __name__ == "__main__":
    main()