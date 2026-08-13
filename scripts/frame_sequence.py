"""
Milestone 3.2 stretch goal: save a frame sequence from a headless render.
"""

import os
os.environ["MUJOCO_GL"] = "egl"  # set before importing mujoco

import mujoco
from PIL import Image

SCENE_PATH = "scripts/scenes/smoke_scene.xml"
OUTPUT_DIR = "evidence/frames"
N_FRAMES = 60


def main():
    model = mujoco.MjModel.from_xml_path(SCENE_PATH)
    data = mujoco.MjData(model)
    renderer = mujoco.Renderer(model, height=480, width=640) # create a renderer for the model that the rendered image is 480x640 pixels

    os.makedirs(OUTPUT_DIR, exist_ok=True) # exist_ok=True tells Python not to raise an error if the directory already exists

    for i in range(N_FRAMES):
        mujoco.mj_step(model, data)
        renderer.update_scene(data)
        Image.fromarray(renderer.render()).save(f"{OUTPUT_DIR}/frame_{i:03d}.png")

    print(f"[PASS] saved {N_FRAMES} frames to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()