"""
Milestone 3.2 engineering task smoke test script for MuJoCo.

loads a minimal MJCF model, steps the simulation, and prints a concise
pass/fail result. This is a sanity check that the environment (Python
version, mujoco package) is installed correctly — not a physics test.
"""

import mujoco

MODEL_XML = "<mujoco><worldbody/></mujoco>"
NUM_STEPS = 100

def main():
    # MjModel: the static, compiled description of the scene (from MJCF).
    # It doesn't change during simulation.
    model = mujoco.MjModel.from_xml_string(MODEL_XML)

    # MjData: the mutable simulation state (time, qpos, qvel, ctrl, etc.)
    # that changes every mj_step call.
    data = mujoco.MjData(model)

    # Advance the simulation NUM_STEPS times.
    for _ in range(NUM_STEPS):
        mujoco.mj_step(model, data)

    print(f"[PASS] mujoco smoke test: {NUM_STEPS} steps completed")
    print(f"       simulation_time={data.time:.4f}")
    print(f"       mujoco version={mujoco.__version__}")


if __name__ == "__main__":
    main()