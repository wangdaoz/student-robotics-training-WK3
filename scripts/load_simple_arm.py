"""
Milestone 3.3, Engineering Task 9.
 
Load models/simple_arm.xml and confirm it runs, first attempting the
interactive viewer, then falling back to a headless step loop if no
display is available. This mirrors the viewer/headless pattern from
Milestone 3.2 and sets up the model-loading code that
scripts/inspect_model.py and scripts/control_simple_arm.py will reuse
in Tasks 10-11.
 
Usage:
    python scripts/load_simple_arm.py            # try viewer, else headless
    python scripts/load_simple_arm.py --headless # skip the viewer entirely
"""

import os
import sys
import mujoco

MODEL_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "models", "simple_arm.xml"))

def load_model(path: str = MODEL_PATH):
    """Load and compile the MJCF file, returning (model, data)."""
    model = mujoco.MjModel.from_xml_path(path)
    data = mujoco.MjData(model)
    return model, data

def run_headless(model, data, n_steps: int = 200):
    """Step the simulation with no rendering and report the final state."""
    for _ in range(n_steps):
        mujoco.mj_step(model, data)

    print(f"Loaded '{MODEL_PATH}' successfully (headless).")
    print(f"simulation_time = {data.time:.4f} s")
    print(f"qpos = {data.qpos}")
    print(f"qvel = {data.qvel}")

def run_viewer(model, data):
    """Open the interactive viewer. Raises if no display is available."""
    import mujoco.viewer
    
    with mujoco.viewer.launch_passive(model, data) as viewer:
        print(f"Viewer launched for '{MODEL_PATH}'. Close the window to exit.")
        while viewer.is_running():
            mujoco.mj_step(model, data)
            viewer.sync()


def main():
    model, data = load_model()

    if "--headless" in sys.argv:
        run_headless(model, data)
        return

    # NOTE: on GLFW init failure, mujoco.viewer does not raise a normal,
    # catchable Python exception -- it terminates the process directly.
    # A try/except around run_viewer() will NOT save you here. Checking
    # for a display up front is the reliable way to detect a headless
    # environment before ever touching the viewer.
    if not os.environ.get("DISPLAY"):
        print("No DISPLAY environment variable found -- assuming headless "
              "environment (e.g. WSL, CI, or a remote container).")
        print("Skipping viewer; running headless verification instead.")
        run_headless(model, data)
        return

    run_viewer(model, data)


if __name__ == "__main__":
    main()