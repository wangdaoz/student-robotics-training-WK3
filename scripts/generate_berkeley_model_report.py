"""
scripts/generate_berkeley_model_report.py

Produces a human-readable Markdown inventory of every named joint and
actuator in the official Berkeley Humanoid Lite model, resolved entirely
through mj_id2name / mj_name2id -- no hard-coded names or indices.
"""

import os
import time
import mujoco

MODEL_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", 
             "models/berkeley/Berkeley-Humanoid-Lite-Assets/data/robots/berkeley_humanoid/berkeley_humanoid_lite/mjcf", "bhl_scene.xml"))

OUTPUT_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..",
                                       "evidence/logs/", "berkeley_model_report.md"))

JOINT_TRANSMISSION_TYPES = {int(mujoco.mjtTrn.mjTRN_JOINT), int(mujoco.mjtTrn.mjTRN_JOINTINPARENT)}

# mjtJoint enum -> (readable label, #qpos slots, #qvel/dof slots)
JOINT_TYPE_INFO = {
    mujoco.mjtJoint.mjJNT_FREE:   ("free (floating base)", 7, 6),
    mujoco.mjtJoint.mjJNT_BALL:   ("ball", 4, 3),
    mujoco.mjtJoint.mjJNT_SLIDE:  ("slide", 1, 1),
    mujoco.mjtJoint.mjJNT_HINGE:  ("hinge", 1, 1),
}

def build_actuator_index(model):
    """Reverse map: joint_id -> list of actuator names driving it.
    Built by scanning every actuator once -- MuJoCo only stores the
    actuator->joint direction natively, so the reverse direction has
    to be assembled here, not assumed from naming conventions."""

    joint_to_actuators = {}
    for ac_id in range(model.nu):
        if model.actuator_trntype[ac_id] not in JOINT_TRANSMISSION_TYPES:
            continue
        
        j_id = model.actuator_trnid[ac_id, 0]
        ac_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_ACTUATOR, ac_id)
        joint_to_actuators.setdefault(j_id,[]).append(ac_name)

    return joint_to_actuators

def joint_table(model, joint_to_actuators):
    lines = [
         "| Joint Name | Type | qpos addr | dof addr | Range (rad) | Driven by |",
         "|---|---|---|---|---|---|"
    ]

    for j_id in range(model.njnt):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, j_id)
        jtype = model.jnt_type[j_id]
        label, n_qpos, n_dof = JOINT_TYPE_INFO[jtype]
        qpos_adr = model.jnt_qposadr[j_id]

        if jtype == mujoco.mjtJoint.mjJNT_FREE:
            range_str = "N/A (free joint)"
        elif model.jnt_limited[j_id]:
            lo, hi = model.jnt_range[j_id]
            range_str = f"{lo: .3f}, {hi: .3f}"
        else:
            range_str = "unlimited"

        drivers = ", ".join(joint_to_actuators.get(j_id, ["None"]))
        lines.append(
            f"| {name} | {jtype} | {qpos_adr} "
            f"({n_qpos} slots) | {model.jnt_dofadr[j_id]} ({n_dof} slots) "
            f"| {range_str} | {drivers} |"
        )

    return "\n".join(lines)

def actuator_table(model):
    lines = [
        "| Actuator name | Drives joint | Force range (N*m) | Ctrl range |",
        "|---|---|---|---|",
    ]

    for ac_id in range(model.nu):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_ACTUATOR, ac_id) or "(unnamed)"

        if model.actuator_trntype[ac_id] in JOINT_TRANSMISSION_TYPES:
            j_id = model.actuator_trnid[ac_id,0]
            joint_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, j_id)
        else:
            joint_name = "(not joint-driven)"

        lo_f, hi_f = model.actuator_forcerange[ac_id]
        force_str = f"{lo_f: .1f}, {hi_f: .1f}"

        if model.actuator_ctrllimited[ac_id]:
            lo_c, hi_c = model.actuator_ctrlrange[a_id]
            ctrl_str = f"[{lo_c:.3f}, {hi_c:.3f}]"
        else:
            ctrl_str = "unbounded (clipped by force range)"
        
        lines.append(f"| {name} | {joint_name} | {force_str} | {ctrl_str} |")
    return "\n".join(lines)

def main():
    model = mujoco.MjModel.from_xml_path(MODEL_PATH)
    joint_to_actuators = build_actuator_index(model)

    report = f"""# Berkeley Humanoid Lite — Model Inspection Report

Generated: {time.strftime("%Y-%m-%dT%H:%M:%S")}
Source model: `{MODEL_PATH}`

## Model statistics

| Stat | Value |
|---|---|
| Generalized positions (nq) | {model.nq} |
| Generalized velocities (nv) | {model.nv} |
| Actuators (nu) | {model.nu} |
| Bodies (nbody) | {model.nbody} |
| Joints (njnt) | {model.njnt} |
| Timestep (s) | {model.opt.timestep} |

## Joints

{joint_table(model, joint_to_actuators)}

## Actuators

{actuator_table(model)}
"""

    with open(OUTPUT_PATH, "w") as f:
        f.write(report)
    print(f"Report written to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()