# **👤 Member A: The Architect (Simulation & Math)**

**Focus:** Numpy, Data Generation, Simulation Loop, Graphs.

## **📅 Day 1: Dec 28 (Sunday)**

**Goal:** Create the traffic generator.

* [x] **Setup:** Clone Repo & Run uv sync.  
* [x] **Code (1h):** Create src/traffic\_gen.py. Implement generate\_arrivals(lambda\_rate) using numpy.random.poisson.  
* [x] **Code (1h):** Create src/intersection.py. Define a Class Intersection with properties: queue, green\_timer, is\_green.  
* [x] **Git Commit:** feat: implement poisson traffic generator and intersection class

## **📅 Day 1.5: Dec 28 (Sunday Evening)**

**Goal:** Refactor for Realism.

* [x] **Refactor:** Update Intersection to support 4 Queues (N, S, E, W) and Phases (NS, EW).
* [x] **Test:** Update tests to verify multi-queue logic.

## **📅 Day 2: Dec 29 (Monday)**

**Goal:** Build the Simulation Loop (The Engine).

* [x] **Code (2h):** Create src/simulation.py. Write a time-step loop ($t=0$ to $1000$).  
* [x] **Logic:** Implement basic queue math: Queue \= Queue \+ Arrivals \- Departures.  
* [x] **Test:** Print the queue length to console to ensure it grows/shrinks.  
* [x] **Git Commit:** feat: implement main discrete event simulation loop

## **📅 Day 3: Dec 30 (Tuesday)**

**Goal:** Connect with Member B (Fuzzy) & Export Data.

* [x] **Integration (1h):** Import get\_green\_duration from Member B's code. Call it inside the loop when the light changes.  
* [x] **Code (1h):** Save the simulation history (Time, Queue Length, Signal State) to a JSON/CSV file. (Member C needs this\!).  
* [ ] **Git Commit:** feat: integrate fuzzy logic and export simulation data to json

## **📅 Day 4: Dec 31 (Wednesday)**

**Goal:** Run Experiments (Comparison).

* [ ] **Code (2h):** Run the simulation twice:  
  1. Scenario A: Fixed Timer (30s Green, 30s Red).  
  2. Scenario B: Fuzzy Logic Adaptive Timer.  
* [ ] **Analysis:** Calculate "Total Waiting Time" for both.  
* [ ] **Git Commit:** feat: add comparison mode (fixed vs fuzzy)

## **📅 Day 5: Jan 1 (Thursday)**

**Goal:** Visualization Graphs.

* [ ] **Code (1h):** Use matplotlib to plot "Queue Length vs Time" (Blue line \= Fixed, Red line \= Fuzzy).  
* [ ] **Deliverable:** Save the plot as results\_graph.png for the Paper.  
* [ ] **Git Commit:** docs: generate comparative performance graphs