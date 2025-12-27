# **👤 Member C: The Visualizer (Manim & Tech Lead)**

**Focus:** Manim Animations, GitHub Management, Final Polish.

## **📅 Day 1: Dec 28 (Sunday)**

**Goal:** The Environment & Base Scene.

* [ ] **Setup:** Ensure uv, ffmpeg, and miktex are working on Windows.  
* [ ] **Code (2h):** Create src/visualizer.py. Draw the Intersection:  
  * Two crossing roads (Lines).  
  * A Traffic Light object (Circle/Rectangle that changes color).  
* [ ] **Git Commit:** feat: create basic manim road scene and traffic light objects

## **📅 Day 2: Dec 29 (Monday)**

**Goal:** Basic Animation Mechanics.

* [ ] **Code (2h):** Create a Car class in Manim (a simple Dot or Rectangle).  
* [ ] **Logic:** Write a function spawn\_car() that moves a Dot from edge to center.  
* [ ] **Git Commit:** feat: implement car animation class and movement logic

## **📅 Day 3: Dec 30 (Tuesday)**

**Goal:** Data-Driven Animation.

* [ ] **Communication:** Ask Member A for the simulation\_data.json format.  
* [ ] **Code (2h):** Write a parser in Manim to read the JSON.  
  * *Logic:* For frame in JSON: if new\_car: spawn\_car().  
* [ ] **Git Commit:** feat: parse simulation json to drive animations

## **📅 Day 4: Dec 31 (Wednesday)**

**Goal:** The "Fuzzy" Visuals.

* [ ] **Code (2h):** Visualize the Logic.  
  * Animate the "Queue Counter" number changing.  
  * Animate the "Timer" counting down.  
  * *(Bonus)*: Show a mini-graph in the corner showing the Fuzzy Membership activation.  
* [ ] **Git Commit:** style: add hud elements (timer, queue counter, graphs)

## **📅 Day 5: Jan 1 (Thursday) through Jan 3 (Saturday)**

**Goal:** Final Rendering & Project Merging.

* [ ] **Tech Lead Task:** Merge all Pull Requests from Member A and B. Resolve conflicts.  
* [ ] **Render:** Run the full render command: manim \-p \-qh src/visualizer.py FinalScene. (High Quality).  
* [ ] **Check:** Ensure the video matches the graphs in the paper.  
* [ ] **Git Commit:** style: final render of project video