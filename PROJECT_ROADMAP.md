# **🚦 Project Roadmap: Adaptive Traffic Optimization**

**Course:** Numerical Methods  
**Deadline:** January 6, 2026  
**Tools:** Python (uv), Manim, Typst, Scikit-Fuzzy

## **🧠 Project Context (The "Why" & "How")**

### **The Problem**

Traditional traffic lights use fixed timers, leading to inefficiencies (waiting at an empty red light). We aim to optimize the **Green Light Duration** based on real-time queue length.

### **The Scientific Approach**

1. **Data Generation (Monte Carlo):** Instead of using static datasets, we simulate traffic arrivals using the **Poisson Distribution** ($P(k) = \frac{\lambda^k e^{-\lambda}}{k!}$) to model stochastic arrival events.

2. **The Numerical Method (Simulation):** We use Euler's Method (Discrete Time Stepping) to simulate the queue dynamics over time:
   $$Q_{t+1} = Q_t + (\text{Arrivals}_t - \text{Departures}_t)$$

3. **The Optimizer (Fuzzy Logic):** A **Mamdani Fuzzy Inference System** determines the optimal green light duration.
   * *Inputs:* Queue Length, Arrival Rate.
   * *Output:* Green Duration extension.

4. **Verification:** We compare the **Average Waiting Time** (Area under the Curve) of our Fuzzy System vs. a Fixed Timer System.

### **Tech Stack**

* **Environment:** uv (Python 3.12+)  
* **Logic:** numpy (Poisson), scikit-fuzzy (Logic), matplotlib (Analysis)  
* **Visualization:** manim (Video Rendering)  
* **Documentation:** typst (Paper)

## **📅 Daily Timeline**

### **Phase 1: Foundations**

* **Dec 28 (Sun):** Core Logic Implementation (Poisson \+ Basic Fuzzy \+ Road Scene).  
* **Dec 29 (Mon):** The Simulation Loop (Connecting Traffic Gen to Queue Logic).

### **Phase 2: Integration**

* **Dec 30 (Tue):** connecting the "Brain" (Fuzzy) to the "Body" (Simulation). Exporting data.  
* **Dec 31 (Wed):** Visualizing the Data (Manim reads the Simulation logs). *Happy New Year\!*

### **Phase 3: Analysis & Drafting**

* **Jan 1 (Thu):** Running Experiments (Fixed vs. Fuzzy). Generating Graphs.  
* **Jan 2 (Fri):** Drafting the Paper (Methodology & Results).

### **Phase 4: Polish & Render**

* **Jan 3 (Sat):** Final Video Rendering (High Quality).  
* **Jan 4 (Sun):** Final Paper Polish (Typst).  
* **Jan 5 (Mon):** Buffer Day (Review, Print, Upload).  
* **Jan 6 (Tue):** 🚀 **SUBMISSION DAY**