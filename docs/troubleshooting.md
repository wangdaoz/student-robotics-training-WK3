Milestone 3.2 
    Engineering Task 4
     Issue #1:
       In case: run locally in your Linux/WSL python virtual environment

       After you inputted: <pip install jupyter>

       During the installation of the jupyter package, there maybe an error:
         [
            ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
            launch-ros 0.26.12 requires setuptools, which is not installed.
         ]

        Why:
            launch-ros is a ROS2 package — it has nothing to do with MuJoCo or jupyter. Its presence in a warning about your venv almost always means one thing: your shell is sourcing a ROS2 environment script (commonly source /opt/ros/humble/setup.bash or similar in your ~/.bashrc), which sets a PYTHONPATH environment variable. That variable leaks into every Python environment you activate — including a fresh venv — because venv isolates site-packages, but it does not clear PYTHONPATH. So pip is seeing a mix of your clean venv and your system ROS installation, and flagging an unrelated inconsistency in the ROS side.

            To Confirm this cause:
             '''
                echo $PYTHONPATH
             '''
            Expected Result:
                    prints something like /opt/ros/humble/lib/python3.10/site-packages:..., that's the source.
        Solutions:
            1. Check jupyter actually installed 
               '''
                  jupyter --version
               '''
               Expected Results:
                        Selected Jupyter core packages...
                        IPython          : 9.16.1
                        ipykernel        : 7.3.0
                        ipywidgets       : 8.1.8
                        jupyter_client   : 8.9.1
                        jupyter_core     : 5.9.1
                        jupyter_server   : 2.20.0
                        jupyterlab       : 4.6.2
                        nbclient         : 0.11.0
                        nbconvert        : 7.17.1
                        nbformat         : 5.11.0
                        notebook         : 7.6.1
                        qtconsole        : not installed
                        traitlets        : 5.16.1
                 Note:
                       ● [qtconsole : not installed]
                           This item is not installed is normal and harmless. 
                           qtconsole is a standalone desktop GUI app for Jupyter that almost nobody uses anymore (you'll use the browser-based notebook/lab interface instead). It's not a dependency of anything you need.

                       ● The earlier launch-ros/setuptools warning didn't break anything — confirmed, since jupyter is fully installed and reporting versions across the board.
               
             2. Make a clean, conflict-free environment
              For your MuJoCo work specifically, you can safely ignore this warning — it's flagging a problem in your ROS packages, not in jupyter or mujoco, and it won't affect your venv's ability to run the tutorial. But if you'd rather have a clean, conflict-free environment for this project:

             '''
                deactivate
                unset PYTHONPATH
                source .venv/bin/activate
                pip install jupyter
             '''
                <unset PYTHONPATH> for this terminal session stops the ROS packages from leaking in, so pip's resolver only sees your venv. You'll need to do this each time you open a new terminal for MuJoCo work (or just don't source your ROS setup script in that session).

    Engineering Task 6:

       ## Viewer under WSL

       Attempted:
       ''' 
           python -m mujoco.viewer --mjcf=/tmp/smoke_scene.xml
       '''

       Result: FAILED (unusable)

       Symptoms:
            - Window opened but was fully unresponsive (taskbar click did nothing)
            - Displayed "Warning: Copy mode" watermark (WSLg fallback display mode)

       Diagnosis:

           - `glxinfo -B` shows Device: llvmpipe, Accelerated: no — no GPU-accelerated
              OpenGL available in this WSL instance; rendering falls back to a CPU
              software rasterizer, too slow for an interactive real-time viewer.
                 
               Original Contents:
                [
                  name of display: :0
                  display: :0  screen: 0
                  direct rendering: Yes
                  Extended renderer info (GLX_MESA_query_renderer):
                      Vendor: Mesa (0xffffffff)
                      Device: llvmpipe (LLVM 20.1.2, 256 bits) (0xffffffff)
                      Version: 25.2.8
                      Accelerated: no
                      Video memory: 15834MB
                      Unified memory: yes
                      Preferred profile: core (0x1)
                      Max core profile version: 4.5
                      Max compat profile version: 4.5
                      Max GLES1 profile version: 1.1
                      Max GLES[23] profile version: 3.2
                  Memory info (GL_ATI_meminfo):
                      VBO free memory - total: 0 MB, largest block: 0 MB
                      VBO free aux. memory - total: 14345 MB, largest block: 14345 MB
                      Texture free memory - total: 0 MB, largest block: 0 MB
                      Texture free aux. memory - total: 14345 MB, largest block: 14345 MB
                ]
           - `echo $MUJOCO_GL` was empty (using GLFW default), consistent with the
              above — not a MuJoCo configuration issue, a WSL/GPU passthrough issue.
                  Original Contents: 
                  [
                      \(.venv) kevin-lianhu@CAGEWANG:~/student-robotics-training-WK3$ echo $MUJOCO_GL
                      
                  ]


       Environment: WSL2 + WSLg, Mesa 25.2.8, no GPU acceleration

       Conclusion: GUI viewer not usable in this environment without further
       GPU-passthrough configuration (out of scope for this milestone). Proceeding
       with headless verification per acceptance criteria — see
       scripts/mujoco_smoke_test.py, which passes independently of the viewer.   

Stretch Goals:
         1. 
          Frame Sequence
           ## Offscreen rendering backend

             Attempted: MUJOCO_GL=osmesa
             Result: FAILED — AttributeError: 'NoneType' object has no attribute 'glGetError'
             Cause: MuJoCo's osmesa backend delegates to PyOpenGL, which needs its own
             PYOPENGL_PLATFORM env var (separate from MUJOCO_GL) — was unset, so it
             defaulted to a non-headless platform and failed to load any GL library.

             Fix: MUJOCO_GL=egl — uses MuJoCo's native EGL bindings (not PyOpenGL),
             reusing the same Mesa/llvmpipe stack already confirmed working for the
             GLFW viewer. No extra packages needed.

           ## Pillow package was not installed
              Error: 
                    Traceback (most recent call last):
                    File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/frame_sequence.py", line 5, in <module>
                        from PIL import Image
                    ModuleNotFoundError: No module named 'PIL'
              
              Fix: 
                 '''
                    source .venv/bin/activate
                    pip install Pillow
                    pip freeze > requirements.txt
                 '''

            ## '/tmp/smoke_scene.xml' is not exist
                Error:
                      Traceback (most recent call last):
                      File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/frame_sequence.py", line 7, in <module>
                      model = mujoco.MjModel.from_xml_path("/tmp/smoke_scene.xml")
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                      ValueError: ParseXML: Error opening file '/tmp/smoke_scene.xml'
                Fix:
                    Qick fix:
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

                    Better fix — stop relying on /tmp at all

                    '''
                        mkdir -p scripts/scenes
                        cat > scripts/scenes/smoke_scene.xml << 'EOF'
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
            A Randered video

Milestone 3.3

    Engineering Tasks:
                     
                #8, #9

            Error #1:
                Traceback (most recent call last):
                  File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/load_simple_arm.py", line 72, in <module>
                    main()
                  File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/load_simple_arm.py", line 50, in main
                    model, data = load_model()
                                  ^^^^^^^^^^^^
                  File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/load_simple_arm.py", line 24, in load_model
                    model = mujoco.MjModel.from_xml_path(path)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                ValueError: XML Error: invalid keyword: 'Local'
                Element 'compiler', line 11

            Fix: Open the /home/kevin-lianhu/student-robotics-training-WK3/models/simple_arm.xml, access to line 11, Element 'compiler', revised 'Local' to 'local'
            
            Error #2:
                Traceback (most recent call last):
                  File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/load_simple_arm.py", line 72, in <module>
                    main()
                  File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/load_simple_arm.py", line 50, in main
                    model, data = load_model()
                                  ^^^^^^^^^^^^
                  File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/load_simple_arm.py", line 24, in load_model
                    model = mujoco.MjModel.from_xml_path(path)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
             
                ValueError: XML Error: invalid keyword: 'True'
                Element 'joint', line 38

            Fix: Open the /home/kevin-lianhu/student-robotics-training-WK3/models/simple_arm.xml, access to line 38, Element 'joint', revised 'True' to 'true'