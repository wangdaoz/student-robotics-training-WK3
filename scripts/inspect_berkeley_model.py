'''
milestone 3.5
Task 23: Write scripts/inspect_berkeley_model.py to load the model and list model statistics, 
         named joints, named actuators, and ranges
'''
import os
import mujoco

MODEL_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "models/berkeley/Berkeley-Humanoid-Lite-Assets/data/robots/berkeley_humanoid/berkeley_humanoid_lite/mjcf", "bhl_scene.xml"))

model = mujoco.MjModel.from_xml_path(MODEL_PATH)
data = mujoco.MjData(model)

def list_model_statistics(model):
    """Display the model's statistics."""
    print(f"Loaded '{MODEL_PATH}' successfully.")
    print(f"bodies(nbody): {model.nbody}")
    print(f"joints(njnt): {model.njnt}")
    print(f"actuators(nu): {model.nu}")
    print(f"qpos size(nq): {model.nq}")
    print(f"qvel size(nv): {model.nv}")

    for i in range(model.njnt):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i)
        print("joint:", name)

    for i in range(model.nu):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_ACTUATOR, i)
        jnt_id = model.actuator_trnid[i,0]
        lo, hi = model.jnt_range[jnt_id]
        print(f"actuator: {name}  range=({lo:.3f}, {hi:.3f})")

def main():
    list_model_statistics(model)

if __name__ == "__main__":
    main()