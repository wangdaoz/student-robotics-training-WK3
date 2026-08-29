"""
scripts/mile3.5stretch_goal1_Control_2_joints.py

Load the official Berkeley Humanoid Lite MJCF model, command a small,
configurable control input on two named actuators for a finite duration,
and log the joint's state before and after.
"""

import csv
import os
import argparse
import json
import time

import mujoco
import numpy as np

MODEL_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", 
                            "models/berkeley/Berkeley-Humanoid-Lite-Assets/data/robots/berkeley_humanoid/berkeley_humanoid_lite/mjcf", 
                            "bhl_scene.xml"))

# Chosen ahead of time by name, per the inventory from inspect_berkeley_model.py.
# leg_left_hip_roll_joint: hinge, range ~[-10deg, +90deg], starts well
# leg_right_hip_roll_joint: hinge, range ~ [-90deg, +10deg]
# inside its range at qpos=0 (not sitting at a limit), and moving it doesn't
# touch the floor or affect balance -- a safe, simple single-joint demo.
JOINT_NAMES = ["leg_left_hip_roll_joint", "leg_right_hip_roll_joint"]
ACTUATOR_NAMES = ["leg_left_hip_roll_joint", "leg_right_hip_roll_joint"]  # motor names == joint names in this MJCF

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ctrl", type=float, default=2.0,
        help="Control input (N*m) sent to the actuator. "
             "Actuator forcerange in this model is +/-20 N*m; "
             "default of 2.0 is a conservative 10%% of that limit.",
    )
    parser.add_argument(
        "--duration", type=float, default=2.0,
        help="Simulation duration in seconds (finite; sim halts after this).",
    )
    parser.add_argument(
        "--freeze-base", action="store_true",
        help="Weld the floating base to the world so only the selected "
             "joint moves, isolating the measurement from the robot "
             "free-falling under gravity. Documented, code-only change -- "
             "does not modify the official MJCF file on disk.",
    )
    parser.add_argument(
        "--log-file", type=str, default="evidence/logs/stretch_goal_1_control_berkeley_j2oints.csv",
        help="Where to write the before/after numerical evidence(CSV).",
    )

    return parser.parse_args()

def main():
    args = parse_args()

    # Safety check: keep control input small relative to the actuator's
    # forcerange, per "Do not command large control values."
    MAX_SAFE_CTRL = 5.0  # N*m, well under the +/-20 N*m forcerange
    if abs(args.ctrl) > MAX_SAFE_CTRL:
        raise ValueError(
        f"--ctrl={args.ctrl} exceeds the safe cap of {MAX_SAFE_CTRL} N*m "
        f"for this task. Use a smaller value."
        )

    model = mujoco.MjModel.from_xml_path(MODEL_PATH)
    data = mujoco.MjData(model)
    
    if args.freeze_base:
        model.opt.gravity[:] = 0.0  # simplest isolation: remove gravity entirely

    all_results = []

    for joint_name, actuator_name in zip(JOINT_NAMES, ACTUATOR_NAMES):
        # Fresh state for every joint's trial -- otherwise the second
        # joint's "initial" state would reflect the first joint's final
        # position, not a true baseline.
        mujoco.mj_resetData(model, data)
        mujoco.mj_forward(model, data)
   
        # Named lookup -- resolve indices from names, never hard-code them.
        joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, joint_name)
        actuator_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, actuator_name)
        if joint_id == -1:
            raise RuntimeError(f"Joint '{joint_name}' not found in compiled model.")
        if actuator_id == -1:
            raise RuntimeError(f"Actuator '{actuator_name}' not found in compiled model.")

        # A hinge joint has exactly 1 qpos/qvel slot; jnt_qposadr/jnt_dofadr give
        # the correct offset regardless of how many free/floating joints precede
        # it in the model (the base_freejoint alone uses 7 qpos / 6 qvel slots).
        qpos_adr = model.jnt_qposadr[joint_id]
        qvel_adr = model.jnt_dofadr[joint_id]
        joint_range = model.jnt_range[joint_id].copy()


        initial_qpos = float(data.qpos[qpos_adr])
        initial_qvel = float(data.qvel[qvel_adr])

        # Hold a constant, small control input for the whole run.
        data.ctrl[actuator_id] = args.ctrl

        n_steps = int(args.duration / model.opt.timestep)
        for step in range(n_steps):
            mujoco.mj_step(model, data)

        final_qpos = float(data.qpos[qpos_adr])
        final_qvel = float(data.qvel[qvel_adr])

        result = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "joint_name": joint_name,
            "actuator_name":actuator_name,
            "joint_range_min_rad": joint_range[0],
            "joint_range_max_rad": joint_range[1],
            "control_input_Nm": args.ctrl,
            "duration_s": args.duration,
            "n_steps": n_steps,
            "freeze_base": args.freeze_base,
            "initial_qpos_rad": initial_qpos,
            "final_qpos_rad": final_qpos,
            "delta_qpos_rad": final_qpos - initial_qpos,
            "initial_qvel_rad_s": initial_qvel,
            "final_qvel_rad_s": final_qvel,
        }

        print(json.dumps(result, indent=2))
        all_results.append(result)

    os.makedirs(os.path.dirname(args.log_file), exist_ok=True)
    file_exists = os.path.isfile(args.log_file)
    with open(args.log_file, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
        if not file_exists:
            writer.writeheader()
        writer.writerows(all_results)

if __name__ == "__main__":
    main()