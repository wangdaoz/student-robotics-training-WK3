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