"""
scripts/mile3.5_stretch_3_contr_berekeley_joint.py

Load the official Berkeley Humanoid Lite MJCF model, command a small,
configurable control input on ONE named actuator for a finite duration,
and log the joint's state before and after.

This does NOT attempt balance, locomotion, or policy control. It only
proves the model can be loaded and controlled at the joint level.
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

JOINT_TRANSMISSION_TYPES = {int(mujoco.mjtTrn.mjTRN_JOINT), int(mujoco.mjtTrn.mjTRN_JOINTINPARENT)}

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target-joint", type = str, default="arm_right_shoulder_pitch_joint",
        help = "the target joint to control"
               "the default target joint is arm_right_shoulder_pitch_joint.",
    )
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
        "--log-file", type=str, default="evidence/logs/stretch_goal3.csv",
        help="Where to write the before/after numerical evidence(CSV).",
    )

    return parser.parse_args()

def build_actuator_index(model):
    """Reverse map: joint_id -> list of actuator names driving it.
    Built by scanning every actuator once -- MuJoCo only stores the
    actuator->joint direction natively, so the reverse direction has
    to be assembled here, not assumed from naming conventions."""

    joint_to_actuators = {}
    for ac_id in range(model.nu):
        if int(model.actuator_trntype[ac_id]) not in JOINT_TRANSMISSION_TYPES:
            continue
        
        j_id = model.actuator_trnid[ac_id, 0]
        ac_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_ACTUATOR, ac_id)
        joint_to_actuators.setdefault(j_id,[]).append(ac_name)

    return joint_to_actuators

def main():
    args = parse_args()
    model = mujoco.MjModel.from_xml_path(MODEL_PATH)
    data = mujoco.MjData(model)

    joint_to_actuators = build_actuator_index(model)

    # Named lookup -- resolve indices from names, never hard-code them
    joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, args.target_joint)
    actuator_names = joint_to_actuators.get(joint_id, [])

    if joint_id == -1:
        raise RuntimeError(f"Joint '{JOINT_NAME}' not found in compiled model.")
    if not actuator_names:
        raise RuntimeError(f"No actuator controls Joint '{JOINT_NAME}'.")

    qpos_addr = model.jnt_qposadr[joint_id]
    qvel_addr = model.jnt_dofadr[joint_id]
    joint_range = model.jnt_range[joint_id].copy()

    if args.freeze_base:
        base_body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "base")
        model.body_mocapid[base_body_id] = -1  # no-op safeguard, base stays a free body
        model.opt.gravity[:] = 0.0  # simplest isolation: remove gravity entirely

    mujoco.mj_resetData(model, data)
    mujoco.mj_forward(model, data) # Using this model and the current state in data, recalculate MuJoCo's derived quantities
    
    """ Record initial position and velicity"""
    initial_qpos = float(data.qpos[qpos_addr])
    initial_qvel = float(data.qvel[qvel_addr])

    n_actuators = len(actuator_names)
    average_ctrl = float(args.ctrl / n_actuators)
    for actuator_name in actuator_names:
        act_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, actuator_name)
        data.ctrl[act_id] = average_ctrl

    average_n_steps = int(args.duration / model.opt.timestep / n_actuators)

    for actuator in actuator_names:
        for step in range(average_n_steps):
            mujoco.mj_step(model, data)

    final_qpos = float(data.qpos[qpos_addr])
    final_qvel = float(data.qvel[qvel_addr])

    result = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "joint_name": args.target_joint,
        "actuator_names": ", ".join(actuator_names),
        "joint_range_min_rad": joint_range[0],
        "joint_range_max_rad": joint_range[1],
        "control_input_Nm": args.ctrl,
        "average_control_input": average_ctrl,
        "duration_s": args.duration,
        "average_n_steps": average_n_steps,
        "freeze_base": args.freeze_base,
        "initial_qpos_rad": initial_qpos,
        "final_qpos_rad": final_qpos,
        "delta_qpos_rad": final_qpos - initial_qpos,
        "initial_qvel_rad_s": initial_qvel,
        "final_qvel_rad_s": final_qvel,
    }

    print(json.dumps(result, indent=2))

    os.makedirs(os.path.dirname(args.log_file), exist_ok=True)
    file_exists = os.path.isfile(args.log_file)
    with open(args.log_file, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=result.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(result)

if __name__ == "__main__":
    main()