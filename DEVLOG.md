## DEVLOG
## April 16, 2026 – 10:00AM

### What I worked on
Today I started the bank simulation project. I created the main Python file and added the base constants for the number of tellers and customers.

### What I completed
- Created bank_simulation.py
- Added project constants
- Added a basic main() function
- Verified the file runs correctly

### Notes
This commit is just the starting point. The goal was to set up the file cleanly before adding threads and synchronization.

### Next step
Add helper logging and argument parsing so the simulation can be tested more easily.
-----------------------------------------------------------------------------------------

## April 16, 2026 – 11:30 PM

### What I worked on
I added a logging helper so every thread action can be printed in the required format. I also added command line argument support so I can test the program with fewer customers during development.

### What I completed
- Added BankSimulation class
- Added thread-safe log() function
- Added command line argument parsing
- Tested sample output formatting

### Notes
The print lock is important because multiple threads will print at the same time later. This helps avoid mixed or broken output lines.

### Next step
Start the teller and customer thread setup.
________________________________________________________________________
## April 17, 2026 – 8:30AM

### What I worked on
I added the teller and customer threads and implemented the rule that the bank only opens after all three tellers are ready.

### What I completed
- Added teller thread function
- Added customer thread function
- Added bank_open event
- Added teller readiness counting
- Started and joined all threads

### Notes
This matches the requirement that customers cannot enter the bank before it is open. I used an event to handle that synchronization cleanly.

### Next step
Add the shared customer line and actual teller-customer interaction.


____________________________________________________________________________________________
## April 17, 2026 – 2:59 PM

### What I worked on
I implemented the customer line and the first real interaction between a customer and a teller. Customers now wait in a queue and a teller pulls the next one when ready.

### What I completed
- Added CustomerState structure
- Added shared queue for waiting customers
- Added semaphore for teller calling customer
- Added semaphore for customer introduction
- Implemented basic teller assignment flow

### Notes
This was an important step because the project is mainly about coordination between customer and teller threads. I kept the transaction logic simple at this stage to focus on interaction.

### Next step
Add deposit and withdrawal communication between the customer and the teller.

