# Berkeley Humanoid Lite - Model Source

## Primary asset source
   Berkeley Humanoid Lite main repository: https://github.com/HybridRobotics/Berkeley-Humanoid-Lite 
   
   Version/Commit SHA: v2025.09.03/dcde70d

   MJCF entry file: data/robots/berkeley_humanoid/berkeley_humanoid_lite/mjcf/bhl_scene.xml

   License: Creative Commons Attribution Share Alike 4.0 International (CC BY-SA 4.0)

## Parent workspace (pins the above as a submodule)
   Berkeley Humanoid Lite Assets repository: https://github.com/HybridRobotics/Berkeley-Humanoid-Lite-Assets

   Version/Commit SHA: v1.1.0 / aa93e47

   License: 
            - Code (main repo, HybridRobotics/Berkeley-Humanoid-Lite): MIT License
            - Other Assets/CAD models: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)

## How Obtained
    Clone Repo:
                    '''
                       git clone --recurse-submodules https://github.com/HybridRobotics/Berkeley-Humanoid-Lite.git
                       cd Berkeley-Humanoid-Lite
                    '''

    Checkout the pinned version used for this asset map:
                    '''
                       git checkout v1.1.0 or git checkout aa93e47
                       git submodule update --init --recursive
                    '''

## Quick Start

     For milestone 3.5:

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

         Stretch Goals:
            #1:
                 '''
                    unset PYTHONPATH
                    source .venv/bin/activate
                    python scripts/mile3.5stretch_goal1_Control_2_joints.py --ctrl 1.0 --duration 2.0
                 '''
            
            #2:
               '''
                  unset PYTHONPATH
                  source .venv/bin/activate
                  python scripts/generate_berkeley_model_report.py
               '''
            #3:
                 '''
                    unset PYTHONPATH
                    source .venv/bin/activate
                    python scripts/mile3.5_stretch_3_contr_berekeley_joint.py --target-joint "arm_left_shoulder_pitch_joint" --ctrl 1.0 --duration 2.0
                 '''