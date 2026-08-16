'''
Milestone 3.3 Engineering Task 10: list bodies, joints, actuators, nq, nv, and nu.
'''
import os
import mujoco

MODEL_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "models", "simple_arm.xml"))

def load_model(path: str = MODEL_PATH):
    """Load and compile the MJCF file, returning (model, data)."""
    model = mujoco.MjModel.from_xml_path(path)
    return model

def model_inspection(model):

    data = mujoco.MjData(model)
    """display the model's bodies, joints, actuators, nq, nv, and nu."""
    print(f"Loaded '{MODEL_PATH}' successfully.")
    print(f"bodies(nbody): {model.nbody}")
    print(f"joints(njnt): {model.njnt}")
    print(f"actuators(nu): {model.nu}")
    print(f"qpos size(nq): {model.nq}")
    print(f"qvel size(nv): {model.nv}")
    
    print("\nBodies:")
    for i in range(model.nbody):
        print(f"body {i}: {model.body(i).name}")
    
    print("\nJoints:")
    for i in range(model.njnt):
        print(f"joint {i}: {model.joint(i).name}")
    
    print("\nActuators:")
    for i in range(model.nu):
        print(f"actuator {i}: {model.actuator(i).name}")

    print("\nqpos:")
    for i in range(model.nq):
        print(f"qpos {i}: {data.qpos[i]}")

    print("\nqvel:")
    for i in range(model.nv):
        print(f"qvel {i}: {data.qvel[i]}")


def main():
    model = load_model()
    model_inspection(model)

if __name__ == "__main__":
    main()