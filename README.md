# Lab_07_Plotly

Complete submission artifacts for the Plotly lab.

## Environment

- Workspace venv used: `venv`
- Python: 3.12.0
- Installed for this lab: `plotly`, `kaleido`
- Existing packages reused: `pandas`, `numpy`, `gradio`

## What Was Implemented

### 1) First demo (provided dashboard)

- Implemented in `first_demo_app.py` using the provided chart/callback structure.
- Smoke-tested successfully without launching a long-running server.

### 2) Five recreations from "100 data visualisations"

Generated files:

- `outputs/100_dataviz/01_lollipop_ranking.png`
- `outputs/100_dataviz/02_dumbbell_comparison.png`
- `outputs/100_dataviz/03_waffle_composition.png`
- `outputs/100_dataviz/04_radial_profile.png`
- `outputs/100_dataviz/05_stream_area.png`

Design and implementation notes:

- Data structures were kept simple and explicit (categorical lists, percentages, monthly sequences).
- Custom color palettes were set manually per figure to stay close to intentional design choices.
- Matching exact references is difficult without source SVG specs or exact font assets; closest visual equivalents were used with tuned spacing/backgrounds.
- Some visualizations can be done without chart libraries (e.g., waffle or dumbbell via SVG/CSS/canvas), but Plotly gives fast iteration and export.

### 3) Real data: Hemianopsia (3D)

Generated files:

- `outputs/hemianopsia/hemianopsia_3d.png`
- `outputs/hemianopsia/hemianopsia_example_rendition.png`

Details:

- Seen and unseen stimuli are plotted in the same 3D scene.
- Reaction times are mapped to marker color for seen points.
- A second panel shows reaction time progression by stimulus order.

### 4) Real data: Motor Amplification

Input sessions used:

- `005774.json`
- `479379.json`
- `926818.json`

Generated files:

- `outputs/motor_amplification/Motor-005774_trajectories.png`
- `outputs/motor_amplification/Motor-239716_trajectories.png`
- `outputs/motor_amplification/Motor-926818_trajectories.png`
- `outputs/motor_amplification/motor_rom_summary.png`

Details:

- Actual hand trajectories (`handData`) and adapted trajectories (`adaptedHandData`) are overlaid.
- Horizontal movement is shown in x-z space and vertical movement in y-z space.
- A summary chart compares range-of-motion span (actual vs adapted) per hand and session.

## Optional Star Cancellation

- Executed using the real `341980.json` dataset (object coordinates, selected sequence, and metadata).
- Generated files:
  - `outputs/star_cancellation/star_cancellation_experiment.png`
  - `outputs/star_cancellation/star_cancellation_3d.png`
- GLB asset used: `Board.glb/Board.glb`.

## Optional First Demo Screenshot

- Generated files:
  - `outputs/optional/first_demo_screenshot.png`

## Automation Script

- Main generator: `generate_visualizations.py`

Run command:

```bash
venv\Scripts\python.exe generate_visualizations.py
```

Optional (if interactive HTML files are desired):

```bash
set LAB07_SAVE_HTML=1
venv\Scripts\python.exe generate_visualizations.py
```

## Hand-in Checklist Status

- [x] Optional: screenshot of first demo.
- [x] At least 5 data visualizations of the "100 data visualizations".
- [x] 3D visualization with Hemianopsia data.
- [x] Chart of Motor Amplification.
- [x] Optional: Star cancellation experiments.
