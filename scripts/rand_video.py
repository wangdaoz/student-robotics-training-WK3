import os
os.environ["MUJOCO_GL"] = "egl"  # set before importing mujoco

import mujoco
from PIL import Image

import imageio

SCENE_PATH = "scripts/scenes/smoke_scene.xml"
OUTPUT_DIR = "evidence/logs"
N_FRAMES = 10

def main():
    model = mujoco.MjModel.from_xml_path(SCENE_PATH)
    data = mujoco.MjData(model)
    renderer = mujoco.Renderer(model, height=480, width=640)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    writer = imageio.get_writer(f"{OUTPUT_DIR}/sphere_drop.mp4", fps=30)
    for i in range(N_FRAMES):
        mujoco.mj_step(model, data)
        renderer.update_scene(data)
        writer.append_data(renderer.render())

    writer.close()
    print(f"[PASS] saved {N_FRAMES} frames to {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()