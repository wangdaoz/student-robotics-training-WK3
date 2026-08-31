# student-robotics-training-WK3

## Quick-Start

     Milestone 3.2:
            
            Task #2, #3
                            '''
                                cd ~/student-robotics-training-WK3
                                python3 --version
                                python3 -m venv .venv
                            '''

                            '''
                               source .venv/bin/activate
                               python --version
                            '''

                            '''
                               pip install --upgrade pip
                               pip install mujoco
                               pip freeze > requirements.txt
                               grep -n "venv" .gitignore
                            '''
            Task #4
                     '''
                        source .venv/bin/activate
                        pip install jupyter
                     '''
                     '''
                        mkdir -p ~/scratch/mujoco-tutorial
                        cd ~/scratch/mujoco-tutorial
                        unset PYTHONPATH
                        source ~/student-robotics-training-WK3/.venv/bin/activate
                        curl -O https://raw.githubusercontent.com/google-deepmind/mujoco/main/python/tutorial.ipynb
                        jupyter notebook --no-browser --port=8888
                     '''

            Task #5
                     '''
                        cd ~/student-robotics-training-WK3
                        nano scripts/mujoco_smoke_test.py

                        unset PYTHONPATH
                        source .venv/bin/activate
                        python scripts/mujoco_smoke_test.py

                        
                        mkdir -p evidence/logs
                        python scripts/mujoco_smoke_test.py | tee evidence/logs/smoke_test_output.txt
                     '''
            Task #6
                     '''
                        unset PYTHONPATH
                        source .venv/bin/activate
                        python -m mujoco.viewer 2>&1 | tee evidence/logs/viewer_attempt.txt
                     '''

            Stretch Goals:

                    1. Save a short rendered video or frame sequence

                        ● Frame Sequence:
                                       '''
                                          unset PYTHONPATH
                                          source .venv/bin/activate
                                          python scripts/save_frame_sequence.py
                                       '''
                        ● Short Rander Video:
                                        '''
                                           unset PYTHONPATH
                                           source .venv/bin/activate
                                           python scripts/rand_video.py
                                        '''         
                    2. Inspect model statistics such as number of bodies, joints, actuators, qpos, and qvel
                                     '''
                                        unset PYTHONPATH
                                        source .venv/bin/activate
                                        python scripts/stretchgoal2_model_stats.py | tee evidence/logs/stretchgoal2_model_stats.txt
                                     '''

                    3. Add a small automated smoke test
                              '''
                                 nano/touch tests/test_mujoco_env.py
                                 source .venv/bin/activate
                                 python tests/test_mujoco_env.py
                                 echo "exit code: $?"
                              '''

     Milestone 3.3:
                       #9
                       '''
                          unset PYTHONPATH
                          source .venv/bin/activate
                          python scripts/load_simple_arm.py
                          python scripts/load_simple_arm.py --headless | tee  evidence/logs/load_simple_arm.txt
                       '''

                       #10

                       '''
                          unset PYTHONPATH
                          source .venv/bin/activate
                          python scripts/inspect_model.py
                       '''

                       #11
                        '''
                           unset PYTHONPATH
                           source .venv/bin/activate
                           python scripts/control_simple_arm.py
                        '''

                       Task #14

                         '''
                            unset PYTHONPATH
                            source .venv/bin/activate
                            python tests/verify_simple_model.py
                         '''

                Scratch Goal #3:
                      '''
                          unset PYTHONPATH
                          source .venv/bin/activate
                          python scripts/record_tip_trajectory.py
                          python teste/verify_simple_model_actuator_joint.py
                      '''
     Milestone 3.5

                Task #23:
                          '''
                             git submodule add https://github.com/HybridRobotics/Berkeley-Humanoid-Lite-Assets.git models/berkeley/Berkeley-Humanoid-Lite-Assets
                          '''

                          '''
                             cd models/berkeley/Berkeley-Humanoid-Lite-Assets
                             git log -1 --format=%H
                          '''

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
                          '''

                Task #27
                        '''
                           unset PYTHONPATH
                           source .venv/bin/activate
                           python scripts/control_berkeley_joint.py --ctrl 1.5 --duration 3.0 --record
                        '''

                Task #28
                         '''
                            source .venv/bin/activate
                            python -m pytest tests/verify_berkeley_model.py -v
                         '''


     AI Exploration:
              '''
                 unset PYTHONPATH
                 source .venv/bin/activate
                 python scripts/generate_berkeley_model_report.py
              '''
       
      
      Stretch Goals

            #1:
                 '''
                    unset PYTHONPATH
                    source .venv/bin/activate
                    python scripts/mile3.5stretch_goal1_Control_2_joints.py --ctrl 1.0 --duration 2.0
                 '''

            #3:
                 '''
                    unset PYTHONPATH
                    source .venv/bin/activate
                    python scripts/mile3.5_stretch_3_contr_berekeley_joint.py --target-joint "arm_left_shoulder_pitch_joint" --ctrl 1.0 --duration 2.0
                 '''