# **Setup Guide for Windows**

This guide is for team members working directly on Windows (PowerShell/CMD).  
This setup is perfect for writing logic, simulation code, and documentation.

## **1. Install uv (Project Manager)**

We use uv to ensure everyone uses the exact same library versions without conflicts.  
Open **PowerShell** and run:
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```
*Note: You may need to restart your terminal after this.*

## **2. Clone & Sync Project**

Navigate to your project folder using PowerShell.  
Clone the repo 
```powershell
git clone git@github.com:shinshARK/fuzzy-traffic-optimization.git 
cd fuzzy-traffic-optimization
```
Install all Python dependencies instantly (including numpy, manim, etc.)  

```
uv sync
```
✅ **You are now ready to code!** You can run the logic scripts using:  
```
uv run src/simulation.py
```
## **3. Setup for Manim (Video Rendering)**

### **A. Install FFmpeg (Required for Video)**

1. Download the "full build" from [gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/).  
2. Extract the ZIP file.  
3. **Crucial:** Add the bin folder (e.g., C:ffmpegbin) to your **Windows System PATH**.  
   * *Search "Edit the system environment variables" -> Environment Variables -> Path -> New -> Paste the path.*  
4. Verify by typing ffmpeg in PowerShell. If you see text describing the version, it works.

### **B. Install MikTeX (Required for Math Equations)**

1. Download and install [MikTeX](https://miktex.org/download).  
2. This allows Manim to render LaTeX equations (like integrals or Greek letters).

### **C. Running Manim on Windows**

Once installed, you can render and preview videos directly:  
```powershell
# -p will automatically open the video player when done  
uv run manim -p -qm src/manim_scene.py SceneName  
```