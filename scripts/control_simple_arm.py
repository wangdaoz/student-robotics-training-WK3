"""
Milestone 3.3, Engineering Task 11.
 
Command the shoulder joint through a safe range using its position
actuator, and check that the actuator is driving the joint we think
it is -- not just moving something.
 
Key idea: we write to data.ctrl (the actuator's target), never to
data.qpos directly. Setting qpos directly teleports the joint and
bypasses physics entirely -- it is not "control."
"""

import os
import mujoco

MODEL_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "models", "simple_arm.xml")
)

# Named once, up front, so the rest of the script looks elements up by
# name instead of assuming fixed indices (see Common Mistakes).
TARGET_JOINT = "shoulder_joint"
TARGET_ACTUATOR = "shoulder_actuator"
ISOLATION_JOINT = "elbow_joint"  # should stay ~put while we drive the shoulder

def load_model(path: str = MODEL_PATH):
    """Load and compile the MJCF file, returning (model, data)."""
    model = mujoco.MjModel.from_xml_path(path)
    data = mujoco.MjData(model)
    return model, data


def safe_targets(model, actuator_name, n_waypoints=5, margin_fraction=0.1):
    """
    Build a sweep of control targets that stay safely inside the
    actuator's own ctrlrange (read from the model, not re-typed by
    hand), with a small margin so we're clearly inside the limit
    rather than grazing it.
    """
    actuator_id = model.actuator(actuator_name).id
    low, upper = model.actuator_ctrlrange[actuator_id]
    margin = margin_fraction * (upper - low)
    low, upper = low + margin, upper - margin
    
    step = (upper - low) / (n_waypoints - 1)
    up = [low + step * i for i in range(n_waypoints)]
    down = list(reversed(up))
    return up + down[1:] # sweep low -> high -> low, no repeated endpoint

def command_joint(model, data, actuator_name, joint_name, targets, settle_steps=100):
    """
    Drive `joint_name` (via `actuator_name`) through each target,
    letting the physics settle for `settle_steps` before recording and
    moving to the next target. Returns a log of (time, target, qpos, qvel).
    """
    actuator_id = model.actuator(actuator_name).id
    qpos_addr = model.jnt_qposadr[model.joint(joint_name).id]

    log = []
    for target in targets:
        data.ctrl[actuator_id] = target
        for _ in range(settle_steps):
            mujoco.mj_step(model, data)
        log.append((data.time, target, data.qpos[qpos_addr], data.qvel[qpos_addr]))

    return log

def main():
    model, data = load_model()

    # Isolation check setup: record the OTHER joint's starting position
    # so we can confirm afterward that it stayed put.
    isolation_qpos_addr = model.jnt_qposadr[model.joint(ISOLATION_JOINT).id]
    isolation_start = data.qpos[isolation_qpos_addr]

    targets = safe_targets(model, TARGET_ACTUATOR)

    print(f"Driving '{TARGET_ACTUATOR}' -> '{TARGET_JOINT}' "
          f"through {len(targets)} safe waypoints\n")
    print(f"{'time':>8} {'target':>8} {'qpos':>8} {'qvel':>8}")

    log = command_joint(model, data, TARGET_ACTUATOR, TARGET_JOINT, targets)
    for t, target, qpos, qvel in log:
        print(f"{t:8.3f} {target:8.3f} {qpos:8.3f} {qvel:8.3f}")

    isolation_end = data.qpos[isolation_qpos_addr]
    print(f"\nIsolation check on '{ISOLATION_JOINT}': "
          f"{isolation_start:.4f} -> {isolation_end:.4f}")
    print("(should stay close to its start -- proves the actuator is "
          "driving only the intended joint)")

if __name__ == "__main__":
    main()