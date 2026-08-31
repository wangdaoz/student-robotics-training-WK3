•	What did I successfully simulate?

        1. Write scripts/control_simple_arm.py to command a joint through a safe range

           I simulated the motion of the shoulder joint by controling the corresponding actuator.

        2. Write scripts/control_berkeley_joint.py with small, configurable control input and a finite simulation duration.

           I simulated the motion of the arm_right_shoulder_pitch_joint by controling the corresponding actuator.
          
•  What did I learn about MJCF that I did not understand from reading alone?

    MJCF(MuJoCo Configuration Format), many physics properties can be written via tag to define itself. What set of physical properties that MJCF can defined?

•  Which Berkeley asset file became the entry point, and how did I verify that?
        bhl_scene.xml became the entry points
     
    in the directory: Berkeley-Humanoid-Lite-Assets/data/robots/berkeley_humanoid/berkeley_humanoid_lite/mjcf/:
       
       ● bhl_scene.xml includes berkeley_humanoid_lite.xml (adds ground plane, lighting, skybox — the robot file itself has none of this)

       ● bhl_biped_scene.xml includes berkeley_humanoid_lite_biped.xml

       ● berkeley_humanoid_lite.xml and berkeley_humanoid_lite_biped.xml themselves contain no further <include> tags — they're self-contained, single-file robot definitions (worth stating explicitly, since "no includes" is itself a fact someone reproducing this needs to know).

       from milestone 3.4 task #18, the file: berkeley_humanoid_lite.xml is intended for the full robot.
       So the include file: bhl_scene.xml can load the full robot.

       So In milestone 3.5, task #25, the control script: scripts/control_berkeley_joint.py load the model from the path:
       "models/berkeley/Berkeley-Humanoid-Lite-Assets/data/robots/berkeley_humanoid/berkeley_humanoid_lite/mjcf/bhl_scene.xml",
       Thus, the entry point is the asset file: bhl_scene.xml.

•	What was the hardest model-loading or graphics problem?

        Design a model-inspection report using names rather than hard-coded indices:
        Produces a human-readable Markdown inventory of every named joint and actuator in the official Berkeley Humanoid Lite model, resolved entirely through mj_id2name / mj_name2id -- no hard-coded names or indices.

        The logic of codes is complicated. Refer the details in the file: scripts/generate_berkeley_model_report.py.

•	What evidence proves the joint moved?

        The change exceeds noise by a wide margin and is attributable to your control input specifically, which means a scripted assertion, not a manual read-through.

•	Which claim in my documentation is still uncertain?

        According to the file: docs/troubleshooting.md, 
        in milestone 3.2, for stretch goal 1:
        for the error:
                    { Error:
                      Traceback (most recent call last):
                      File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/frame_sequence.py", line 7, in <module>
                      model = mujoco.MjModel.from_xml_path("/tmp/smoke_scene.xml")
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                      ValueError: ParseXML: Error opening file '/tmp/smoke_scene.xml' }

        the quick fix:
                            '''
                               cat > /tmp/smoke_scene.xml << 'EOF'
                               <mujoco>
                                 <worldbody>
                                   <light diffuse=".8 .8 .8" pos="0 0 3"/>
                                   <geom type="plane" size="1 1 0.1" rgba="0.6 0.6 0.6 1"/>
                                   <body pos="0 0 1">
                                     <joint type="free"/>
                                     <geom type="sphere" size="0.1" rgba="0.9 0.2 0.2 1"/>
                                   </body>
                                 </worldbody>
                                 </mujoco>
                                 EOF
                             '''
                        I didn't try it because I choose another fix solution.
           
•	What mistake from Week 2 did I avoid—or repeat?
        Before activate the virtual environmrnt, I remembered to unset the variable PYTHONPATH.
        However, When I ran every documented command in a clean shell, I forgot to avoid the ROS 2.0 PYTHONPATH leak ( I should input the command "unset PYTHONPATH" before activating the venv). Thus, a warning was reported while the shell was running.
        Error Report:
                     {
                        ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
                        launch-ros 0.26.12 requires setuptools, which is not installed.
                     }
        
        
        
•	What should the next engineer do first?
           
        Browse the README.md in the root of the repo;
         For each milestone, read the corresponding setup file, daily reports and troubleshooting file in the directory docs/.