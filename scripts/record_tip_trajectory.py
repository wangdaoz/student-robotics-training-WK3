"""
Milestone 3.3 Stretch Goal: "Add a position sensor or site and record
its trajectory."

Drives the shoulder and elbow through a safe sweep (same pattern as
control_simple_arm.py) and records the WORLD-frame xyz position of
the arm's tip -- read from tip_position_sensor, not computed by hand
-- at every physics step, producing a continuous trajectory rather
than just a handful of waypoints.

Usage:
    python scripts/record_tip_trajectory.py
"""

import csv
import os
import mujoco

MODEL_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "models", "simple_arm.xml")
)
LOG_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "evidence", "logs", "tip_trajectory.csv")
)

SENSOR_NAME = "tip_position_sensor"


def load_model():
    model = mujoco.MjModel.from_xml_path(MODEL_PATH)
    data = mujoco.MjData(model)
    return model, data


def safe_targets(model, actuator_name, n_waypoints=4, margin_fraction=0.15):
    """Same margin-based sweep pattern as control_simple_arm.py."""
    actuator_id = model.actuator(actuator_name).id
    low, high = model.actuator_ctrlrange[actuator_id]
    margin = margin_fraction * (high - low)
    low, high = low + margin, high - margin
    step = (high - low) / (n_waypoints - 1)
    up = [low + step * i for i in range(n_waypoints)]
    return up + list(reversed(up))[1:]


def record_trajectory(settle_steps=150):
    model, data = load_model()

    sensor_id = model.sensor(SENSOR_NAME).id
    adr, dim = model.sensor_adr[sensor_id], model.sensor_dim[sensor_id]
    assert dim == 3, f"expected a 3D position sensor, got dim={dim}"

    shoulder_id = model.actuator("shoulder_actuator").id
    elbow_id = model.actuator("elbow_actuator").id

    shoulder_targets = safe_targets(model, "shoulder_actuator")
    elbow_targets = safe_targets(model, "elbow_actuator")
    # Drive both joints together through a shared sweep so the tip
    # actually traces a 2D path, not just an up-down line.
    n_waypoints = min(len(shoulder_targets), len(elbow_targets))

    trajectory = []  # (time, x, y, z)
    for i in range(n_waypoints):
        data.ctrl[shoulder_id] = shoulder_targets[i]
        data.ctrl[elbow_id] = elbow_targets[i]
        for _ in range(settle_steps):
            mujoco.mj_step(model, data)
            x, y, z = data.sensordata[adr:adr + dim]
            trajectory.append((data.time, x, y, z))

    return trajectory


def write_csv(trajectory, path=LOG_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "tip_x", "tip_y", "tip_z"])
        writer.writerows(trajectory)


def main():
    trajectory = record_trajectory()
    write_csv(trajectory)

    xs = [row[1] for row in trajectory]
    zs = [row[3] for row in trajectory]
    print(f"Recorded {len(trajectory)} trajectory points -> {LOG_PATH}")
    print(f"tip_x range: {min(xs):.4f} to {max(xs):.4f}")
    print(f"tip_z range: {min(zs):.4f} to {max(zs):.4f}")
    print(f"first point: {trajectory[0]}")
    print(f"last point:  {trajectory[-1]}")


if __name__ == "__main__":
    main()
