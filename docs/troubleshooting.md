### Milestone 3.2 
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

### Milestone 3.3

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

        #10
            Error 1
            '''
               Loaded '/home/kevin-lianhu/student-robotics-training-WK3/models/simple_arm.xml' successfully.
               bodies(nbody): 4
               joints(njnt): 2
               Traceback (most recent call last):
                 File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/inspect_model.py", line 54, in <module>
                   main()
                 File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/inspect_model.py", line 51, in main
                   model_inspection(model)
                 File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/inspect_model.py", line 20, in model_inspection
                   print(f"actuators(nact): {model.nact}")
                              ^^^^^^^^^^
               AttributeError: 'mujoco._structs.MjModel' object has no attribute 'nact'. Did you mean: 'noct'?
            '''

            Fix: Open the File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/inspect_model.py", access to the line 20,
            actiators are belong to Control Input, the correspondding MjModel object attrbute is 'nu'; MjModel attribute has no attribute 'nact'.

            Error 2
            '''
               Traceback (most recent call last):
                 File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/inspect_model.py", line 50, in <module>
                   main()
                 File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/inspect_model.py", line 47, in main
                   model_inspection(model)
                 File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/inspect_model.py", line 26, in model_inspection
                   print(f"body {i}: {model.body[i].name}")
                                      ~~~~~~~~~~^^^
               TypeError: 'method' object is not subscriptable
            '''
            Fix:
                 change 'model.body[i]' to 'model.body(i)' because 'body()' is a method for model object.

            Error 3
            '''
                Traceback (most recent call last):
                  File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/inspect_model.py", line 50, in <module>
                    main()
                  File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/inspect_model.py", line 47, in main
                    model_inspection(model)
                  File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/inspect_model.py", line 38, in model_inspection
                    print(f"qpos {i}: {model.name_qpos[i]}")
                                       ^^^^^^^^^^^^^^^
                AttributeError: 'mujoco._structs.MjModel' object has no attribute 'name_qpos'. Did you mean: 'cam_pos'?
            '''
            Fix:
                in function 'model_inspection(model)', create a MjData object for the MjModel; Then, access MjData's 'qpos' array 
                '''
                  data = mujoco.MjData(model)
                  ...
                  print("\nqpos:")
                  for i in range(model.nq):
                      print(f"qpos {i}: {data.qpos[i]}")
                '''

### Milestone 3.5
   
   Engineering Tasks
        
           #23 Write scripts/inspect_berkeley_model.py to load the model and list model statistics, named joints, named actuators, and ranges.

               after running the command: ''' python scripts/inspect_berkeley_model.py '''

               the feedback:
                          [
                            Traceback (most recent call last):
                              File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/inspect_berkeley_model.py", line 11, in <module>
                                model = mujoco.MjModel.from_xml_path(MODEL_PATH)
                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                            ValueError: Error: Error opening file '/home/kevin-lianhu/student-robotics-training-WK3/models/berkeley/Berkeley-Humanoid-Lite-Assets/data/robots/berkeley_humanoid/berkeley_humanoid_lite/mjcf/merged/leg_right_ankle_roll_visual.stl'
                          ]
          
              This is a legitimate, anticipated blocker:
                    Further verification:
                      ● config.json has "merge_stls": true — confirms a merge step really does run.

                      ● .gitignore has **/assets/* under a # Onshape-to-robot comment — confirms this output is intentionally excluded from git.

                      ● The export script (export_onshape_to_mjcf.py) actually creates mjcf/assets/merged/, copies meshes there, then runs content.replace("assets/merged/", "../meshes/") to rewrite the XML paths to point at the shared meshes/ folder instead — then deletes the assets folder (shutil.rmtree).

               Thus, it's a deliberately generated-and-discarded intermediate build artifact. And the path-rewrite step has a real bug: it does a literal string search for "assets/merged/", but MJCF splits that into two separate attributes (meshdir="assets" + file="merged/x.stl") that never appear concatenated as one string — so the rewrite silently never fires on this file. That's the actual root cause of the broken path, not just "files went missing."

               It's a genuine, reproducible gap between what the MJCF's meshdir/file attributes expect and what the repo's .gitignore actually ships, and any other engineer doing a clean clone will hit the identical error.

               Fix:
                   '''
                       cd models/berkeley/Berkeley-Humanoid-Lite-Assets/data/robots/berkeley_humanoid/berkeley_humanoid_lite
                       mkdir -p mjcf/assets/merged
                       cp meshes/*.stl mjcf/assets/merged/
                   '''

                   and re-run the script: scripts/inspect_berkeley_model.py

            #24 - #26

               After inputting the command: <python scripts/control_berkeley_joint.py --ctrl 1.5 --duration 3.0>, nothing displays and the target .csv file in the 'evidence/' didn't exist.

               Fix:  <if __name__ == "__main__": main()> is missing at the bottom of the file: scripts/control_berkeley_joint.py.
                    Add this segment of codes at the bottom of the file and re-run the file.

  #28
 Blocker 1:

    After input the commands:
               '''
                  source .venv/bin/activate
                  pytest tests/verify_berkeley_model.py -v
               '''

               The system reported the following error:
=================================================================== test session starts ===================================================================
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.4.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/kevin-lianhu/student-robotics-training-WK3
plugins: colcon-core-0.21.0, cov-4.1.0
collected 0 items / 1 error                                                                                                                               

========================================================================= ERRORS ==========================================================================
_____________________________________________________ ERROR collecting tests/verify_berkeley_model.py _____________________________________________________
ImportError while importing test module '/home/kevin-lianhu/student-robotics-training-WK3/tests/verify_berkeley_model.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/verify_berkeley_model.py:9: in <module>
    import mujoco
E   ModuleNotFoundError: No module named 'mujoco'
================================================================= short test summary info =================================================================
ERROR tests/verify_berkeley_model.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
==================================================================== 1 error in 0.10s ===================================================================== 


Analysis:

     When you ran python scripts/control_berkeley_joint.py, that command found some python on your PATH — very possibly a virtual environment, conda env, or a user-level pip install — and mujoco is installed there. But the pytest command is a separate executable with its own shebang line pointing at whatever Python it was originally installed for — often the system interpreter, /usr/bin/python3, especially if pytest was installed via apt/pip install --user at some point rather than inside the same environment as mujoco. So "the tests run" and "the control script runs" can silently be two completely different Python installations, each with their own separate set of installed packages.

    1., inpute the following commands confirm the analysis
       '''
          which python3
          python3 -c "import sys; print(sys.executable)"
          python3 -c "import mujoco; print(mujoco.__file__)"

          which pytest
          head -1 $(which pytest)
       '''
         Results:
              [
                 /usr/bin/python3
                 Traceback (most recent call last):
                 File "<string>", line 1, in <module>

                 /usr/bin/pytest
                 #!/usr/bin/python3
              ]

      2. directly confirmation, not in virtual environment
         '''
            which python
            python -c "import mujoco; print(mujoco.__file__)"
         '''

         results:
              [
                Command 'python' not found, did you mean:
                command 'python3' from deb python3
                command 'python' from deb python-is-python3
              ]

      3. reactivate the virtual environment and figure out which module not exist
        '''

           source .venv/bin/activate
           python -c "import mujoco; print(mujoco.__file__)"
           python -m pytest --version
        
        '''

        Results:
                '''
                   /home/kevin-lianhu/student-robotics-training-WK3/.venv/lib/python3.12/site-packages/mujoco/__init__.py
                   /home/kevin-lianhu/student-robotics-training-WK3/.venv/bin/python: No module named pytest
                '''

Fix:
     in activated venv, install pytest module
                '''
                   pip install pytest

                '''

                Results:
                         [
                             Collecting pytest
                               Downloading pytest-9.1.1-py3-none-any.whl.metadata (7.6 kB)
                             Collecting iniconfig>=1.0.1 (from pytest)
                               Downloading iniconfig-2.3.0-py3-none-any.whl.metadata (2.5 kB)
                             Requirement already satisfied: packaging>=22 in ./.venv/lib/python3.12/site-packages (from pytest) (26.3)
                             Collecting pluggy<2,>=1.5 (from pytest)
                               Downloading pluggy-1.6.0-py3-none-any.whl.metadata (4.8 kB)
                             Requirement already satisfied: pygments>=2.7.2 in ./.venv/lib/python3.12/site-packages (from pytest) (2.20.0)
                             Downloading pytest-9.1.1-py3-none-any.whl (386 kB)
                             Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)
                             Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)
                             Installing collected packages: pluggy, iniconfig, pytest
                             Successfully installed iniconfig-2.3.0 pluggy-1.6.0 pytest-9.1.1
                         ]

    Then run the command:
                '''
                   python -m pytest tests/verify_berkeley_model.py -v
                '''

Blocker 2:

=================================================================== test session starts ===================================================================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0 -- /home/kevin-lianhu/student-robotics-training-WK3/.venv/bin/python
cachedir: .pytest_cache
rootdir: /home/kevin-lianhu/student-robotics-training-WK3
plugins: anyio-4.14.2
collected 4 items                                                                                                                                         

tests/verify_berkeley_model.py::test_entry_file_loads ERROR                                                                        [ 25%]
tests/verify_berkeley_model.py::test_selected_joint_exists ERROR                                                                       [ 50%]
tests/verify_berkeley_model.py::test_selected_actuator_exists ERROR                                                                       [ 75%]
tests/verify_berkeley_model.py::test_actuator_drives_the_selected_joint ERROR                                                                       [100%]

========================================================================= ERRORS ==========================================================================
_________________________________________________________ ERROR at setup of test_entry_file_loads _________________________________________________________
file /home/kevin-lianhu/student-robotics-training-WK3/tests/verify_berkeley_model.py, line 29
  def test_entry_file_loads(model):
E       fixture 'model' not found
>       available fixtures: anyio_backend, anyio_backend_name, anyio_backend_options, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, capteesys, doctest_namespace, free_tcp_port, free_tcp_port_factory, free_udp_port, free_udp_port_factory, load_model, monkeypatch, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, subtests, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory
>       use 'pytest --fixtures [testpath]' for help on them.

/home/kevin-lianhu/student-robotics-training-WK3/tests/verify_berkeley_model.py:29
______________________________________________________ ERROR at setup of test_selected_joint_exists _______________________________________________________
file /home/kevin-lianhu/student-robotics-training-WK3/tests/verify_berkeley_model.py, line 36
  def test_selected_joint_exists(model):
E       fixture 'model' not found
>       available fixtures: anyio_backend, anyio_backend_name, anyio_backend_options, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, capteesys, doctest_namespace, free_tcp_port, free_tcp_port_factory, free_udp_port, free_udp_port_factory, load_model, monkeypatch, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, subtests, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory
>       use 'pytest --fixtures [testpath]' for help on them.

/home/kevin-lianhu/student-robotics-training-WK3/tests/verify_berkeley_model.py:36
_____________________________________________________ ERROR at setup of test_selected_actuator_exists _____________________________________________________
file /home/kevin-lianhu/student-robotics-training-WK3/tests/verify_berkeley_model.py, line 40
  def test_selected_actuator_exists(model):
E       fixture 'model' not found
>       available fixtures: anyio_backend, anyio_backend_name, anyio_backend_options, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, capteesys, doctest_namespace, free_tcp_port, free_tcp_port_factory, free_udp_port, free_udp_port_factory, load_model, monkeypatch, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, subtests, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory
>       use 'pytest --fixtures [testpath]' for help on them.

/home/kevin-lianhu/student-robotics-training-WK3/tests/verify_berkeley_model.py:40
________________________________________________ ERROR at setup of test_actuator_drives_the_selected_joint ________________________________________________
file /home/kevin-lianhu/student-robotics-training-WK3/tests/verify_berkeley_model.py, line 44
  def test_actuator_drives_the_selected_joint(model):
E       fixture 'model' not found
>       available fixtures: anyio_backend, anyio_backend_name, anyio_backend_options, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, capteesys, doctest_namespace, free_tcp_port, free_tcp_port_factory, free_udp_port, free_udp_port_factory, load_model, monkeypatch, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, subtests, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory
>       use 'pytest --fixtures [testpath]' for help on them.

/home/kevin-lianhu/student-robotics-training-WK3/tests/verify_berkeley_model.py:44
================================================================= short test summary info =================================================================
ERROR tests/verify_berkeley_model.py::test_entry_file_loads
ERROR tests/verify_berkeley_model.py::test_selected_joint_exists
ERROR tests/verify_berkeley_model.py::test_selected_actuator_exists
ERROR tests/verify_berkeley_model.py::test_actuator_drives_the_selected_joint
==================================================================== 4 errors in 0.30s ====================================================================       

Analysis:

          There's no model fixture in that list — but there is one called load_model. That's not a built-in pytest fixture, which means it's coming from your tests/verify_berkeley_model.py file itself. This strongly suggests the fixture function in your file is actually named load_model, not model
          '''
             @pytest.fixture(scope="module")
             def load_model():   # <-- named load_model here
             return mujoco.MjModel.from_xml_path(MODEL_PATH)
          '''
      Confirm:
             '''
                 grep -n "def load_model\|def model\|(model)\|(load_model)" tests/verify_berkeley_model.py
             '''

             Results:
                    [
                      23:def model():
                      28:def test_entry_file_loads(model):
                      35:def test_selected_joint_exists(model):
                      39:def test_selected_actuator_exists(model):
                      43:def test_actuator_drives_the_selected_joint(model):
                      55:    test_entry_file_loads(model)
                      56:    test_selected_joint_exists(model)
                      57:    test_selected_actuator_exists(model)
                      58:    test_actuator_drives_the_selected_joint(model)
                    ]

Fix:
          '''
             @pytest.fixture(scope="module")
             def model():   # renamed to match what the tests expect
             return mujoco.MjModel.from_xml_path(MODEL_PATH)
          '''

          re-run this file:
             '''
                python -m pytest tests/verify_berkeley_model.py -v
             '''
             

            

                