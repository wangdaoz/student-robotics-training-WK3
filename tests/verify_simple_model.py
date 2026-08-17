'''
  Milestone 3.3 - loads the model and checks expected named elements
'''

import os
import math
import mujoco

MODEL_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "models", "simple_arm.xml"))

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