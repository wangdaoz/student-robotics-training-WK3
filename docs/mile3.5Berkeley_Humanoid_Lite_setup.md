## Computer
   - Operating system: WSL 
   - Python version: Python 3.12.3
   - Git version: 2.43.0
   - VS Code installed: yes
   - Claude Code installed: yes

## Steps Completed && Commands Used

 Suppose your local repo didn't have the submodule repo: Berkeley Humanoid Lite Assets repo.

Engineering tasks:

         Task #23: Write scripts/inspect_berkeley_model.py to load the model and list model statistics, named joints, named actuators, and ranges.

            Steps:
              1. From your training repo root, run the following command:
                 '''
                    git submodule add https://github.com/HybridRobotics/Berkeley-Humanoid-Lite-Assets.git models/berkeley/Berkeley-Humanoid-Lite-Assets
                 '''

                 Expected Results:
                                   [
                                    Cloning into '/home/kevin-lianhu/student-robotics-training-WK3/models/berkeley/Berkeley-Humanoid-Lite-Assets'...
                                    remote: Enumerating objects: 171, done.
                                    remote: Counting objects: 100% (44/44), done.
                                    remote: Compressing objects: 100% (30/30), done.
                                    remote: Total 171 (delta 23), reused 14 (delta 14), pack-reused 127 (from 3)
                                    Receiving objects: 100% (171/171), 64.01 MiB | 5.02 MiB/s, done.
                                    Resolving deltas: 100% (46/46), done.
                                   ]   
              
              2. Pin to a specific commit
                 '''
                    cd models/berkeley/Berkeley-Humanoid-Lite-Assets
                    git log -1 --format=%H
                 '''
                   Expected Result: 
                                   fc90fedd008b1e56a22e3c5221548d6b24f49707

              3. Run the scripts
                 '''
                    unset PYTHONPATH
                    source .venv/bin/activate
                    python scripts/inspect_berkeley_model.py
                    python scripts/inspect_berkeley_model.py | tee evidence/logs/inspect_berkeley_model.csv
                 '''

         Task #24, #25, #26
                 '''
                    unset PYTHONPATH
                    source .venv/bin/activate
                    python scripts/control_berkeley_joint.py --ctrl 1.5 --duration 3.0

         Task #27
                 '''
                    unset PYTHONPATH
                    source .venv/bin/activate
                    python scripts/control_berkeley_joint.py --ctrl 1.5 --duration 3.0 --record
                 '''
                 
               Expected Results:
                               {
                                 "timestamp": "2026-08-25T16:59:54",
                                 "joint_name": "arm_right_shoulder_pitch_joint",
                                 "actuator_name": "arm_right_shoulder_pitch_joint",
                                 "joint_range_min_rad": -0.7853981633975158,
                                 "joint_range_max_rad": 1.570796326794829,
                                 "control_input_Nm": 1.5,
                                 "duration_s": 3.0,
                                 "n_steps": 1500,
                                 "freeze_base": false,
                                 "initial_qpos_rad": 0.0,
                                 "final_qpos_rad": 1.5724852975044492,
                                 "delta_qpos_rad": 1.5724852975044492,
                                 "initial_qvel_rad_s": 0.0,
                                 "final_qvel_rad_s": 0.00016599798800603764
                               }

         Task #28
                 '''
                    source .venv/bin/activate
                    python -m pytest tests/verify_berkeley_model.py -v
                 '''
            Expected Results:
                              [
=================================================================== test session starts ===================================================================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0 -- /home/kevin-lianhu/student-robotics-training-WK3/.venv/bin/python
cachedir: .pytest_cache
rootdir: /home/kevin-lianhu/student-robotics-training-WK3
plugins: anyio-4.14.2
collected 4 items                                                                                                                                         

tests/verify_berkeley_model.py::test_entry_file_loads PASSED                                                                                        [ 25%]
tests/verify_berkeley_model.py::test_selected_joint_exists PASSED                                                                                   [ 50%]
tests/verify_berkeley_model.py::test_selected_actuator_exists PASSED                                                                                [ 75%]
tests/verify_berkeley_model.py::test_actuator_drives_the_selected_joint PASSED                                                                      [100%]

==================================================================== 4 passed in 0.93s ====================================================================
                              ]

## Problems encounted

## Notes for Future Students

        1. Task #23:
            in the file: scripts/inspect_berkeley_model.py:

            <name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i)>
            <name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_ACTUATOR, i)> 

          - The core idea: MUJOCO complies your model into flat arrays

           When MuJoCo loads your MJCF, it doesn't keep a tree of named XML elements around at runtime. Instead, it compiles everything into flat, numbered arrays for speed — joint 0, joint 1, joint 2, ... actuator 0, actuator 1, ... and so on. Your <joint name="leg_right_hip_roll_joint" .../> tag becomes, internally, just "joint index 14" (or whatever number it lands on based on where it appears in the body tree).

           The names you wrote in the XML aren't thrown away — they're stored in a separate lookup table so you can still ask "what's the name of joint #14?" or the reverse, "what's the index of the joint named X?" That's what mj_id2name and mj_name2id are for.

           - mujoco.mjtObj.mjOBJ_JOINT

             this tells MuJoCo which category of object you're asking about. MuJoCo has separate numbering for joints, actuators, bodies, geoms, sensors, etc. — joint index 3 and actuator index 3 are completely unrelated objects. mjtObj is an enum listing all these categories (mjOBJ_JOINT, mjOBJ_ACTUATOR, mjOBJ_BODY, mjOBJ_GEOM, ...), so you have to specify which namespace i refers to.

           - mujoco.mjtObj.mjOBJ_ACTUATOR

             same as mentioned above, tell MuJoCo, you ask're asking about autuator category (mjOBJ_ACTUATOR) 

           - Return value of mujoco.mj_id2name(...)
              the string name you gave that that joint/actuator in XML(e.g. "leg_right_hip_roll_joint"), or None if that joint/actuator was never given a "name= " attribute.

           2. <joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, name="leg_right_hip_roll_joint")>

      
        2. Task #27

             ● <Image.fromarray(renderer.render()).save("evidence/screenshots/before.png")>

                -- renderer.render()
                   tell MuJoCo "renderer" to render the current scene;
                   The result is typically an image represented as a NumPy array, containing pixel data.

                -- Image.fromarray(renderer.render())

                   takes the NumPy array produced by (renderer.render()) and converts it into a Pillow image object.

                -- .save("evidence/screenshots/before.png")

                   saves the Pillow image as a file.

             ● <imageio.mimsave("evidence/screenshots/control_sequence.gif", frames, fps=10)>
                """Save multiple images as an animated image/video."""
            