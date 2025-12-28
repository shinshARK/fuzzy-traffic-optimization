# **👤 Member B: The Theorist (Fuzzy Logic & Paper)**

**Focus:** Scikit-Fuzzy Rules, Typst Documentation, Analysis.

## **📅 Day 1: Dec 28 (Sunday)**

**Goal:** Define the Logic.

* [x] **Setup:** Clone Repo & Run uv sync.  
* [ ] **Research (1h):** Read 2 papers on Fuzzy Traffic Control. Decide inputs (Queue Length, Arrival Rate).  
* [x] **Code (1h):** Create src/fuzzy\_brain.py. Define Membership functions (Trapezoidal/Triangular) for "Short", "Medium", "Long".  
* [x] **Git Commit:** feat: define fuzzy membership functions

## **📅 Day 2: Dec 29 (Monday)**

**Goal:** The Rule Base.

* [ ] **Code (2h):** Implement the Rules in src/fuzzy\_brain.py.  
  * *Example:* IF Queue is Long AND Arrival is High THEN Green is Extended.  
* [ ] **Test:** Run a script testing specific values (e.g., Input 50 cars \-\> Output 45 seconds).  
* [ ] **Git Commit:** feat: implement fuzzy inference rules and defuzzification

## **📅 Day 3: Dec 30 (Tuesday)**

**Goal:** Paper Draft (Bab 1 & 2).

* [ ] **Writing (2h):** Open Typst.  
  * **Bab 1:** Latar Belakang (Why fixed lights are bad).  
  * **Bab 2:** Teori (Poisson Distribution, Euler Method, Fuzzy Logic).  
* [ ] **Git Commit:** docs: draft chapters 1 and 2 in typst

## **📅 Day 4: Dec 31 (Wednesday)**

**Goal:** Methodology.

* [ ] **Writing (1h):** Write **Bab 3 (Metodologi)**. Create a flowchart of the system (Input \-\> Fuzzification \-\> Inference \-\> Defuzzification \-\> Output).  
* [ ] **Git Commit:** docs: complete methodology chapter

## **📅 Day 5: Jan 1 (Thursday)**

**Goal:** Results & Discussion.

* [ ] **Writing (2h):** Take the Graphs from Member A. Explain why the Fuzzy line is lower (better) than the Fixed line.  
* [ ] **Writing:** Calculate the % efficiency gain.  
* [ ] **Git Commit:** docs: write results and analysis chapter