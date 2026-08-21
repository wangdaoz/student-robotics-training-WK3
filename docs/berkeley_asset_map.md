## License & Attribution

    ● the official Berkeley Humanoid Lite repository 
      url: https://github.com/HybridRobotics/Berkeley-Humanoid-Lite

      - Code (main repo, HybridRobotics/Berkeley-Humanoid-Lite): MIT License
        -- see LICENSE file at <https://github.com/HybridRobotics/Berkeley-Humanoid-Lite/blob/main/LICENCE>

      - Other Assets/CAD models: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
        -- see "License" section in README.md

    ● the official assets repository
      url: https://github.com/HybridRobotics/Berkeley-Humanoid-Lite-Assets

      - Codes (main repo, HybridRobotics/Berkeley-Humanoid-Lite-Assets): Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
        -- see LICENSE file at <https://github.com/HybridRobotics/Berkeley-Humanoid-Lite-Assets/blob/main/LICENCE>

## Release/Tag & Commit SHA
     
    ● the official Berkeley Humanoid Lite repository
       
       Release/Tag: v1.1.0

       Raw Commit SHA: aa93e47

    ● the official assets repository
        
      Release/Tag: v2025.09.03

      Raw Commit SHA: dcde70d

## the Official Berkeley Humanoid Lite repository

    Task #18: Locate all candidate MJCF entry files and identify which one is intended for the full robot

         All MJCF entry files are in the directory: https://github.com/HybridRobotics/Berkeley-Humanoid-Lite-Assets/tree/main/data/robots/berkeley_humanoid/berkeley_humanoid_lite/mjcf 

         The file: berkeley_humanoid_lite.xml is intended for the full robot
            
          ● 22 actuated joints, 22 motor actuators — matching exactly the arm (10) + leg (12) DOF split from the Assets repo's own documentation table

          ● Has the <freejoint name="base_freejoint"/> on the root base body, meaning it's a free-floating robot meant to stand/balance, not a fixed test rig

          ● bhl_scene.xml (the companion scene wrapper with ground plane + lighting) includes it via <include file="berkeley_humanoid_lite.xml" />

        In addition,
                    berkeley_humanoid_lite_biped.xml is the partial variant:
                                                                
                            ● Only 12 actuated joints/actuators — leg joints only (leg_left_hip_roll_joint, leg_right_knee_pitch_joint, etc.), no arm joints at all

                            ● This is the one used by the separate Velocity-Berkeley-Humanoid-Lite-Biped-v0 training task mentioned in the docs

                            ● Its own scene wrapper, bhl_biped_scene.xml, includes it separately

    Task #19: Identify included XML files, mesh directories, and likely working-directory assumptions

            1. Included XML files

               in the directory: Berkeley-Humanoid-Lite-Assets/data/robots/berkeley_humanoid/berkeley_humanoid_lite/mjcf/

                ● bhl_scene.xml includes berkeley_humanoid_lite.xml (adds ground plane, lighting, skybox — the robot file itself has none of this)

                ● bhl_biped_scene.xml includes berkeley_humanoid_lite_biped.xml

                ● berkeley_humanoid_lite.xml and berkeley_humanoid_lite_biped.xml themselves contain no further <include> tags — they're self-contained, single-file robot definitions (worth stating explicitly, since "no includes" is itself a fact someone reproducing this needs to know).

            2. Mesh directories
               
                ● berkeley_humanoid_lite.xml declares <compiler meshdir="assets" .../> — every mesh reference is relative to an 'assets' folder.

                ● Individual mesh entry points in berkeley_humanoid_lite.xml and berkeley_humanoid_lite_biped.xml looks are both in such a format <file="merged/xxx.stl>, rather than "mcjf/assets/xxx.stl", thus, there is an extra subfolder 'merged/'

                ● in the subfolder 'Berkeley-Humanoid-Lite-Assets/data/robots/berkeley_humanoid/berkeley_humanoid_lite/mjcf', no subfolder 'assets/merged/'

                  According to the file: README.md, the meshes are shared under /data/robots/berkeley_humanoid/berkeley_humanoid_lite/meshes/ — a sibling folder to mjcf/, not a subfolder inside mjcf/.

                  But the XML itself says: <compiler meshdir="assets" .../>, and mesh entries reference paths like merged/leg_right_knee_pitch_visual.stl — implying the loader looks for assets/merged/... relative to wherever the XML file sits.

                  The directory: '/data/robots/berkeley_humanoid/berkeley_humanoid_lite/meshes/' indeed exists and contains '.stl' files.

                  Then, in repo, there is a '.gitignore' file and 'assets/' folder is excluded.
                  Thus, in the original local repo, the subfolder: 'Berkeley-Humanoid-Lite-Assets/data/robots/berkeley_humanoid/berkeley_humanoid_lite/mjcf/assets/merged/' is existing to store a copy of meshes. But the contributors didn't commit this subfolder(files inside).

            3. Working Directory Assumptions
               
                ● Loading bhl_scene.xml (or the robot XML directly) in any MuJoCo viewer requires the working directory / file location to keep the mjcf/assets/merged/ structure intact relative to the XML — copying just the .xml file elsewhere without its assets/ sibling folder will break mesh loading.

                ● The main repo's README states commands should be run from the repo root — record that as the assumption governing the scripts (training, deployment), separate from the MJCF file's own path assumption above.

    Task #20 Build a table of major bodies, joints, and actuators using XML inspection or the MuJoCo Python API

        XML inspection

        Table:
      
        Body                          Joint                          Type                     Range                 Actuator
                                                                                               (Rad)
        __________________________________________________________________________________________________________________________
        base                       base_freejoint                      free                      /               none(unactuated)
        __________________________________________________________________________________________________________________________
        imu_2                           /                                /                       /                      /
        __________________________________________________________________________________________________________________________
        arm_left_shoulder_pitch  arm_left_shoulder_pitch_joint         hinge              -1.571 to 0.785 
                                                                                                    arm_left_shoulder_pitch_joint(motor)   
        __________________________________________________________________________________________________________________________
        arm_left_shoulder_roll   arm_left_shoulder_roll_joint          hinge              -0.262 to 1.309
                                                                                                     arm_left_shoulder_roll_joint(motor)
        __________________________________________________________________________________________________________________________
        arm_left_shoulder_yaw    arm_left_shoulder_yaw_joint           hinge              -0.785 to 0.785
                                                                                                      arm_left_shoulder_yaw_joint(motor)
        __________________________________________________________________________________________________________________________
        arm_left_elbow_pitch     arm_left_elbow_pitch_joint            hinge           -4.494e-13 to 1.571
                                                                                                       arm_left_elbow_pitch_joint(motor)
        __________________________________________________________________________________________________________________________
        arm_left_elbow_roll      arm_left_elbow_roll_joint             hinge               -0.785 to 0.785
                                                                                                        arm_left_elbow_roll_joint(motor)
        __________________________________________________________________________________________________________________________arm_left_hand_link               /                               /                        /                     /         __________________________________________________________________________________________________________________________arm_right_shoulder_pitch arm_right_shoulder_pitch_joint        hinge                -0.785 to 1.571
                                                                                                         arm_right_shoulder_pitch_joint(motor)
        __________________________________________________________________________________________________________________________
        arm_right_shoulder_roll  arm_right_shoulder_roll_joint         hinge                -1.309 to 0.262
                                                                                                         arm_right_shoulder_roll_joint(motor)
        __________________________________________________________________________________________________________________________
        arm_right_shoulder_yaw   arm_right_shoulder_yaw_joint          hinge                -0.785 to 0.785
                                                                                                         arm_right_shoulder_yaw_joint(motor)
        __________________________________________________________________________________________________________________________
        arm_right_elbow_pitch    arm_right_elbow_pitch_joint           hinge                -1.571 to -0.0
                                                                                                         arm_right_elbow_pitch_joint(motor)
        __________________________________________________________________________________________________________________________
        arm_right_elbow_roll     arm_right_elbow_roll_joint            hinge                -0.785 to 0.785
                                                                                                        arm_right_elbow_roll_joint(motor)
        __________________________________________________________________________________________________________________________
        arm_right_hand_link                /                             /                          /
        __________________________________________________________________________________________________________________________
        leg_left_hip_roll        leg_left_hip_roll_joint               hinge                -1.745 to 1.571
                                                                                                        leg_left_hip_roll_joint(motor)
        __________________________________________________________________________________________________________________________
        leg_left_hip_yaw         leg_left_hip_yaw_joint                hinge                -0.981 to 0.589
                                                                                                        leg_left_hip_yaw_joint(motor)
        __________________________________________________________________________________________________________________________
        leg_left_hip_pitch       leg_left_hip_pitch_joint              hinge                -1.898 to 0.981
                                                                                                        leg_left_hip_pitch_joint(motor)
        __________________________________________________________________________________________________________________________
        leg_left_knee_pitch      leg_left_knee_pitch_joint             hinge                -2.637 to 2.443
                                                                                                        leg_left_knee_pitch_joint(motor)
        __________________________________________________________________________________________________________________________
        leg_left_ankle_pitch     leg_left_ankle_pitch_joint            hinge                -0.785 to 0.785
                                                                                                        leg_left_ankle_pitch_joint(motor)
        __________________________________________________________________________________________________________________________
        leg_left_ankle_roll      leg_left_ankle_roll_joint             hinge                -0.261 to 0.261
                                                                                                        leg_left_ankle_roll_joint(motor)
        __________________________________________________________________________________________________________________________
        leg_right_hip_roll       leg_right_hip_roll_joint              hinge                -1.571 to 0.175
                                                                                                        leg_right_hip_roll_joint(motor)
        __________________________________________________________________________________________________________________________
        leg_right_hip_yaw        leg_right_hip_yaw_joint               hinge                -0.589 to 0.981
                                                                                                        leg_right_hip_yaw_joint(motor)
        __________________________________________________________________________________________________________________________
        leg_right_hip_pitch      leg_right_hip_pitch_joint             hinge                -1.898 to 0.981
                                                                                                        leg_right_hip_pitch_joint(motor)
        __________________________________________________________________________________________________________________________
        leg_right_knee_pitch     leg_right_knee_pitch_joint            hinge                -1.119 to 2.443
                                                                                                        leg_right_knee_pitch_joint(motor)
        __________________________________________________________________________________________________________________________
        leg_right_ankle_pitch    leg_right_ankle_pitch_joint           hinge                -0.785 to 0.785
                                                                                                      leg_right_ankle_pitch_joint(motor)
        __________________________________________________________________________________________________________________________
        leg_right_ankle_roll     leg_right_ankle_roll_joint            hinge                -0.261 to 0.261
                                                                                                       leg_right_ankle_roll_joint(motor)
        __________________________________________________________________________________________________________________________

        MuJoCo Python API
        '''
           import mujoco

           model = mujoco.MjModel.from_xml_path('berkeley_humanoid_lite.xml')

           # Bodies
           for i in range(model.nbody):
               print(model.body(i).name)

           # Joints — model.jnt_type tells you hinge(3)/free(0)/slide(2)/ball(1)
           for i in range(model.njnt):
               j = model.joint(i)
               print(j.name, model.jnt_type[i], model.jnt_range[i])

           # Actuators
           for i in range(model.nu):
               a = model.actuator(i)
               print(a.name, model.actuator_ctrlrange[i])
        '''
      Note: this executable requires the mesh files that are found missing in task 19 in subfolder: Berkeley-Humanoid-Lite-Assets/data/robots/berkeley_humanoid/berkeley_humanoid_lite/mjcf/assets/merged/

      Thus, Work around it by temporarily stripping the <asset>/mesh references so the model compiles for inspection purposes only (not for rendering/physics use) but I'd flag it clearly in your notes as "structure-only, meshes stripped to work around missing files" so nobody mistakes it for a fully working model.

     Item                                  Value
     ___________________________________________________________________________________________________________________
     Total bodies               27 (includes world, so 26 robot bodies)
     ___________________________________________________________________________________________________________________
     Total joints	              23 (1 free + 22 hinge)
     ___________________________________________________________________________________________________________________
     Total actuators	         22 (all motor-type, one per hinge joint)
     ___________________________________________________________________________________________________________________
     Method used               Method used	MuJoCo Python API (mujoco.MjModel.from_xml_path), 
                                cross-checked against manual XML parsing
     ___________________________________________________________________________________________________________________
     Caveat	                   Original file fails to load due to missing mesh assets (Task 19 finding); 
                               loaded here using a structure-only variant with visual <asset>/mesh geoms stripped 
                               — collision geometry (boxes/cylinders) and all bodies/joints/actuators are untouched and unaffected by this
     ____________________________________________________________________________________________________________________