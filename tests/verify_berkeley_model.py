"""
tests/verify_berkeley_model.py

Verifies the official Berkeley Humanoid Lite MJCF entry file loads
successfully, and that the specific named joint/actuator used in
scripts/control_berkeley_joint.py exist in the compiled model.
"""

import os
import mujoco
import pytest

MODEL_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", 
                            "models/berkeley/Berkeley-Humanoid-Lite-Assets/data/robots/berkeley_humanoid/berkeley_humanoid_lite/mjcf", 
                            "bhl_scene.xml"))

JOINT_NAME = "arm_left_shoulder_pitch_joint"
ACTUATOR_NAME = "arm_left_shoulder_pitch_joint"



@pytest.fixture(scope = "module")
def model():
    """Load once and reuse across tests -- compiling the model is the
    expensive part, and every test below depends on it succeeding."""
    return mujoco.MjModel.from_xml_path(MODEL_PATH)

def test_entry_file_loads(model):
    """A successful load already proves bhl_scene.xml's <include> of
    berkeley_humanoid_lite.xml resolved correctly -- if the include were
    broken or a mesh were missing, from_xml_path would have raised."""
    assert model.nq > 0
    assert model.nu > 0

def test_selected_joint_exists(model):
    joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, JOINT_NAME)
    assert joint_id != -1, f"Joint '{JOINT_NAME}' not found in compiled model"

def test_selected_actuator_exists(model):
    actuator_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, ACTUATOR_NAME)
    assert actuator_id != -1, f"Actuator '{ACTUATOR_NAME}' not found in compiled model"

def test_actuator_drives_the_selected_joint(model):
    """Confirms the actuator and joint aren't just two unrelated names that
    both happen to exist -- the actuator must actually be wired to this
    specific joint via its transmission target."""
    joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, JOINT_NAME)
    actuator_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, ACTUATOR_NAME)
    driven_joint_id = model.actuator_trnid[actuator_id, 0]
    assert driven_joint_id == joint_id

def main():

    model = model()
    test_entry_file_loads(model)
    test_selected_joint_exists(model)
    test_selected_actuator_exists(model)
    test_actuator_drives_the_selected_joint(model)

if __name__ == "__main__":
    main()