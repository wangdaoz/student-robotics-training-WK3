"""
Milestone 3.2 stretch goal: inspect model statistics.
"""

import mujoco

SCENE_PATH = "scripts/scenes/smoke_scene.xml"

def main():
    model = mujoco.MjModel.from_xml_path(SCENE_PATH)

    print(f"Model Statistics:{SCENE_PATH}")
    print(f" bodies (nbody):   {model.nbody}")
    print(f" joints (njnt):    {model.njnt}")
    print(f" geoms (ngeom):    {model.ngeom}")
    print(f" actuators (nu):   {model.nu}")
    print(f" qpos size (nq):   {model.nq}")
    print(f" qvel size (nv):   {model.nv}")

    # Name each joint and its type, since type determines its qpos/qvel width
    joint_types = {0: "free", 1: "ball", 2: "slide", 3: "hinge"}
    for i in range(model.njnt):
        jtype = joint_types.get(model.jnt_type[i], "unknown")
        print(f" joint {i}: type={jtype}, name={model.joint(i).name}")

if __name__ == "__main__":
    main()