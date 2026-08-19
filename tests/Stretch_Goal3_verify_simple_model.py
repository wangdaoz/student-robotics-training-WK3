"""
Milestone 3.3, Engineering Task 14.

Load models/simple_arm.xml and check that the specific named elements
the rest of the codebase depends on -- bodies, joints, actuators --
actually exist and have the properties they're supposed to. This
turns the Task 8 "Required Model Elements" checklist into automated
proof, keyed to the concrete names chosen when the model was built.

Runs standalone (no pytest required), but each test_* function is
also independently pytest-discoverable if pytest is installed:
    python tests/Stretch_Goal3_verify_simple_model.py
    pytest tests/Stretch_Goal3_verify_simple_model.py
"""

import math
import os
import mujoco

MODEL_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "models", "simple_arm.xml")
)

EXPECTED_BODIES = ["base", "upper_arm", "forearm"]
EXPECTED_JOINTS = ["shoulder_joint", "elbow_joint"]
EXPECTED_ACTUATORS = ["shoulder_actuator", "elbow_actuator"]

# Which actuator is supposed to drive which joint -- this is what makes
# the actuator-to-joint test meaningful instead of just checking counts.
ACTUATOR_TO_JOINT = {
    "shoulder_actuator": "shoulder_joint",
    "elbow_actuator": "elbow_joint",
}


def load_model():
    return mujoco.MjModel.from_xml_path(MODEL_PATH)


def test_model_loads():
    """Required Model Elements: the file compiles at all."""
    model = load_model()
    assert model is not None


def test_worldbody_and_nested_bodies():
    """Required Model Elements: worldbody + at least two nested bodies."""
    model = load_model()
    assert model.body(0).name == "world"

    for name in EXPECTED_BODIES:
        assert model.body(name) is not None, f"body '{name}' not found by name"

    # Confirm real nesting (each body's parent is the previous one),
    # not just three unrelated bodies floating in the worldbody.
    base_id = model.body("base").id
    upper_arm_id = model.body("upper_arm").id
    forearm_id = model.body("forearm").id
    assert model.body_parentid[upper_arm_id] == base_id, (
        "'upper_arm' should be nested inside 'base'"
    )
    assert model.body_parentid[forearm_id] == upper_arm_id, (
        "'forearm' should be nested inside 'upper_arm'"
    )


def test_expected_joints_are_hinges():
    """Required Model Elements: at least one hinge joint."""
    model = load_model()
    for name in EXPECTED_JOINTS:
        joint = model.joint(name)
        assert joint.type == mujoco.mjtJoint.mjJNT_HINGE, (
            f"'{name}' expected hinge, got type {joint.type}"
        )


def test_joint_limits_are_reasonable():
    """Required Model Elements: reasonable joint limits."""
    model = load_model()
    for name in EXPECTED_JOINTS:
        joint_id = model.joint(name).id
        assert model.jnt_limited[joint_id], f"'{name}' should be limited"

        low, high = model.jnt_range[joint_id]
        assert high > low, f"'{name}' range is degenerate: {low} to {high}"

        # Reject an accidental full rotation -- usually means degrees
        # were typed where radians were expected (see compiler angle).
        assert (high - low) <= 2 * math.pi, (
            f"'{name}' range spans more than a full turn: "
            f"{low:.3f} to {high:.3f} -- check units"
        )


def test_expected_actuators_exist():
    """Required Model Elements: at least one actuator."""
    model = load_model()
    for name in EXPECTED_ACTUATORS:
        assert model.actuator(name) is not None, f"actuator '{name}' not found"


def test_actuators_drive_expected_joints():
    """
    The specific check from Task 11's isolation test, made permanent:
    prove each actuator is wired to the joint we intend, not just that
    *an* actuator and *a* joint both happen to exist.
    """
    model = load_model()
    for actuator_name, joint_name in ACTUATOR_TO_JOINT.items():
        actuator_id = model.actuator(actuator_name).id
        expected_joint_id = model.joint(joint_name).id
        # actuator_trnid[:, 0] holds the id of the element the actuator
        # transmits force to, when transmission type is a joint.
        actual_joint_id = model.actuator_trnid[actuator_id][0]
        assert actual_joint_id == expected_joint_id, (
            f"'{actuator_name}' drives joint id {actual_joint_id}, "
            f"expected '{joint_name}' (id {expected_joint_id})"
        )


def test_actuator_command_moves_target_joint_toward_target():
    """
    Behavioral proof, independent of test_actuators_drive_expected_joints:
    actually command each actuator toward both ends of its ctrlrange and
    confirm the intended joint follows -- not just moves, but moves
    TOWARD the commanded direction. This does not read actuator_trnid
    at all, so it catches a miswiring even if that structural check
    somehow had a blind spot.
    """
    model = load_model()
    for actuator_name, joint_name in ACTUATOR_TO_JOINT.items():
        actuator_id = model.actuator(actuator_name).id
        qpos_addr = model.jnt_qposadr[model.joint(joint_name).id]
        low, high = model.actuator_ctrlrange[actuator_id]
        # Margin-based, not "* 0.8" -- a multiply-by-fraction shortcut only
        # works for ranges centered near zero. elbow_actuator's range
        # (-2.09 to 0) isn't, so interpolate properly instead.
        margin = 0.1 * (high - low)

        # "Converged near the target" implicitly proves both correct
        # direction and correct magnitude in one measurement -- more
        # precise than separately checking "moved enough" (which breaks
        # for asymmetric ranges/targets close to the resting position)
        # and "moved the right way".
        CONVERGENCE_TOLERANCE = 0.15  # rad; observed overshoot settles well inside this
        for target, label in [(high - margin, "high"), (low + margin, "low")]:
            data = mujoco.MjData(model)
            data.ctrl[actuator_id] = target
            for _ in range(300):
                mujoco.mj_step(model, data)
            end = data.qpos[qpos_addr]
            assert abs(end - target) < CONVERGENCE_TOLERANCE, (
                f"commanding '{actuator_name}' toward {target:.3f} ({label} "
                f"end) settled '{joint_name}' at {end:.3f} -- not close to "
                f"target (off by {abs(end - target):.3f} rad)"
            )


def test_actuator_isolation():
    """
    Commanding one actuator should leave every OTHER joint close to its
    starting position. The tolerance (0.1 rad) is set well above the
    natural gravity-sag noise floor (~0.02 rad over 300 steps, measured
    empirically) but far below any real actuated movement (~1+ rad), so
    it distinguishes "unactuated drift" from "unintended coupling."
    """
    model = load_model()
    ISOLATION_TOLERANCE = 0.1  # radians

    for actuator_name, driven_joint in ACTUATOR_TO_JOINT.items():
        data = mujoco.MjData(model)
        other_joints = [j for j in EXPECTED_JOINTS if j != driven_joint]
        starts = {
            j: data.qpos[model.jnt_qposadr[model.joint(j).id]]
            for j in other_joints
        }

        actuator_id = model.actuator(actuator_name).id
        low, high = model.actuator_ctrlrange[actuator_id]
        data.ctrl[actuator_id] = high - 0.1 * (high - low)
        for _ in range(300):
            mujoco.mj_step(model, data)

        for j in other_joints:
            end = data.qpos[model.jnt_qposadr[model.joint(j).id]]
            drift = abs(end - starts[j])
            assert drift < ISOLATION_TOLERANCE, (
                f"commanding '{actuator_name}' moved unrelated joint "
                f"'{j}' by {drift:.4f} rad (> {ISOLATION_TOLERANCE}) -- "
                f"possible miswiring or unintended coupling"
            )


def test_tip_sensor_matches_forward_kinematics():
    """
    Stretch goal: tip_position_sensor should report the same world-frame
    position as the site it's attached to (an independent cross-check,
    not just "does calling it not crash"), and that position should
    actually change when the arm moves.
    """
    model = load_model()
    data = mujoco.MjData(model)

    sensor_id = model.sensor("tip_position_sensor").id
    adr, dim = model.sensor_adr[sensor_id], model.sensor_dim[sensor_id]
    site_id = model.site("tip_site").id

    mujoco.mj_forward(model, data)
    sensor_reading = data.sensordata[adr:adr + dim].copy()
    assert (sensor_reading == data.site_xpos[site_id]).all(), (
        "tip_position_sensor disagrees with the site's own site_xpos"
    )

    rest_position = sensor_reading.copy()
    data.ctrl[model.actuator("shoulder_actuator").id] = 1.0
    for _ in range(300):
        mujoco.mj_step(model, data)
    moved_position = data.sensordata[adr:adr + dim]

    assert not (moved_position == rest_position).all(), (
        "tip position did not change after commanding the shoulder"
    )


def test_actuator_ctrlrange_within_joint_range():
    """A commandable target should never exceed what the joint allows."""
    model = load_model()
    for actuator_name, joint_name in ACTUATOR_TO_JOINT.items():
        actuator_id = model.actuator(actuator_name).id
        joint_id = model.joint(joint_name).id
        ctrl_low, ctrl_high = model.actuator_ctrlrange[actuator_id]
        joint_low, joint_high = model.jnt_range[joint_id]
        assert ctrl_low >= joint_low - 1e-6, (
            f"'{actuator_name}' ctrlrange low ({ctrl_low}) exceeds "
            f"joint range low ({joint_low})"
        )
        assert ctrl_high <= joint_high + 1e-6, (
            f"'{actuator_name}' ctrlrange high ({ctrl_high}) exceeds "
            f"joint range high ({joint_high})"
        )


def test_has_geoms():
    """Required Model Elements: visual or collision geoms."""
    model = load_model()
    assert model.ngeom > 0, "expected at least one geom in the model"


def test_model_steps_without_exploding():
    """Sanity check: the model is numerically stable, not just well-named."""
    model = load_model()
    data = mujoco.MjData(model)
    for _ in range(50):
        mujoco.mj_step(model, data)
    assert all(abs(v) < 1e6 for v in data.qvel), (
        "simulation velocities exploded -- check damping and gains"
    )


ALL_TESTS = [
    test_model_loads,
    test_worldbody_and_nested_bodies,
    test_expected_joints_are_hinges,
    test_joint_limits_are_reasonable,
    test_expected_actuators_exist,
    test_actuators_drive_expected_joints,
    test_actuator_command_moves_target_joint_toward_target,
    test_actuator_isolation,
    test_tip_sensor_matches_forward_kinematics,
    test_actuator_ctrlrange_within_joint_range,
    test_has_geoms,
    test_model_steps_without_exploding,
]


def main():
    passed, failed = 0, 0
    for test_fn in ALL_TESTS:
        name = test_fn.__name__
        try:
            test_fn()
            print(f"PASS  {name}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL  {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR {name}: {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
