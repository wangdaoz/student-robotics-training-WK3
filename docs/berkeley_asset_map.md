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

    Task 18: Locate all candidate MJCF entry files and identify which one is intended for the full robot

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