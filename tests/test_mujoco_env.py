"""
Milestone 3.2 stretch goal: automated smoke test.

Unlike scripts/mujoco_smoke_test.py (prints a human-readable result),
this asserts specific pass/fail conditions and exits non-zero on failure —
suitable for CI or a future pre-commit check.
"""

import sys
import mujoco

SCENE_PATH = "scripts/scenes/smoke_scene.xml"


def test_model_loads():
    model = mujoco.MjModel.from_xml_path(SCENE_PATH)
    assert model.nbody > 0, "Model has no bodies"
    return model

def test_simulation_steps(model):
    data = mujoco.MjData(model)
    z_start = data.qpos[2]

    for _ in range(100):
        mujoco.mj_step(model, data)

    assert data.time > 0, "Simulation time did not advance"
    assert data.qpos[2] < z_start, "Object did not fall under gravity"
    return data

def test_no_nan_or_inf(data):
    import numpy as np
    assert np.all(np.isfinite(data.qpos)), "qpos contains NaN/Inf — simulation diverged"
    assert np.all(np.isfinite(data.qvel)), "qvel contains NaN/Inf - simulation diverged"

def main():
    try:
        model = test_model_loads()
        print("[PASS] model loads")

        data = test_simulation_steps(model)
        print("[PASS] simulation steps and sphere falls under gravity")

        test_no_nan_or_inf(data)
        print("[PASS] no NaN/Inf in final state")
    
    except AssertionError as e:
        print(f"[FAIL] {e}")
        sys.exit(1)
    
    print("[PASS] all checks passed")
    sys.exit(0)

if __name__ == "__main__":
    main()