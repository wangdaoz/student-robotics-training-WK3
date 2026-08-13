## Computer
   - Operating system: WSL 
   - Python version: Python 3.12.3
   - Git version: 2.43.0
   - VS Code installed: yes
   - Claude Code installed: yes

## Steps Completed && Commands Used

   Tasks #2, #3
    1. Check the version of your Python, then create the venv
        '''
            cd ~/student-robotics-training-WK3
            python3 --version
            python3 -m venv .venv
        '''
    2. Activate it and confirm the exact version inside
       '''
           source .venv/bin/activate
           python --version
       '''
         Expected Result:
              Python 3.12.3

    3. Install MuJoCo and freeze dependencies
       '''
          pip install --upgrade pip
       '''
          Expected Results:
            
               [
                    Requirement already satisfied: pip in ./.venv/lib/python3.12/site-packages (24.0)
                    Collecting pip
                    Downloading pip-26.2.1-py3-none-any.whl.metadata (4.6 kB)
                    Downloading pip-26.2.1-py3-none-any.whl (1.8 MB)
                    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 3.5 MB/s eta 0:00:00
                    Installing collected packages: pip
                      Attempting uninstall: pip
                        Found existing installation: pip 24.0
                        Uninstalling pip-24.0:
                          Successfully uninstalled pip-24.0
                    Successfully installed pip-26.2.1
               ]
               
        '''
           pip install mujoco
        '''
            Expected Results:
                [
                    Collecting mujoco
                       Downloading mujoco-3.11.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (232 kB)
                    Collecting absl-py (from mujoco)
                      Downloading absl_py-2.5.0-py3-none-any.whl.metadata (3.3 kB)
                    Collecting etils[epath] (from mujoco)
                      Downloading etils-1.14.0-py3-none-any.whl.metadata (6.5 kB)
                    Collecting glfw (from mujoco)
                      Downloading glfw-2.10.2-py2.py3-none-manylinux_2_28_x86_64.whl.metadata (5.5 kB)
                    Collecting numpy (from mujoco)
                      Downloading numpy-2.5.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (6.6 kB)
                    Collecting pyopengl (from mujoco)
                      Downloading pyopengl-3.1.10-py3-none-any.whl.metadata (3.3 kB)
                    Collecting fsspec (from etils[epath]->mujoco)
                      Downloading fsspec-2026.7.0-py3-none-any.whl.metadata (10 kB)
                    Collecting typing_extensions (from etils[epath]->mujoco)
                      Downloading typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
                    Collecting zipp (from etils[epath]->mujoco)
                      Downloading zipp-4.1.0-py3-none-any.whl.metadata (3.6 kB)
                    Downloading mujoco-3.11.0-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (18.9 MB)
                       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 18.9/18.9 MB 4.2 MB/s  0:00:04
                    Downloading absl_py-2.5.0-py3-none-any.whl (137 kB)
                    Downloading etils-1.14.0-py3-none-any.whl (172 kB)
                    Downloading fsspec-2026.7.0-py3-none-any.whl (206 kB)
                    Downloading glfw-2.10.2-py2.py3-none-manylinux_2_28_x86_64.whl (248 kB)
                    Downloading numpy-2.5.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.7 MB)
                       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.7/16.7 MB 4.6 MB/s  0:00:03
                    Downloading pyopengl-3.1.10-py3-none-any.whl (3.2 MB)
                       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.2/3.2 MB 4.9 MB/s  0:00:00
                    Downloading typing_extensions-4.16.0-py3-none-any.whl (45 kB)
                    Downloading zipp-4.1.0-py3-none-any.whl (10 kB)
                    Installing collected packages: pyopengl, glfw, zipp, typing_extensions, numpy, fsspec, etils, absl-py, mujoco
                    Successfully installed absl-py-2.5.0 etils-1.14.0 fsspec-2026.7.0 glfw-2.10.2 mujoco-3.11.0 numpy-2.5.1 pyopengl-3.1.10 typing_extensions-4.16.0 zipp-4.1.0
                ]

        '''
           pip freeze > requirements.txt
           
        '''

        Confirm '.venv/' is ignored
                  -- it should already be covered by the Python template you picked earlier, but verify
        '''
           grep -n "venv" .gitignore
        '''

   Tasks #4
        
         1. Activate the virtual environment
           '''
              source .venv/bin/activate
           '''

         2. Install the "jupyter" package
           '''
              pip install jupyter
           '''

           Expected Results:
                           Requirement already satisfied: jupyter in ./.venv/lib/python3.12/site-packages (1.1.1)
                           Requirement already satisfied: notebook in ./.venv/lib/python3.12/site-packages (from jupyter) (7.6.1)
                                                                 .
                                                                 .
                                                                 .
                           Requirement already satisfied: tzdata in ./.venv/lib/python3.12/site-packages (from arrow>=0.15.0->isoduration->jsonschema[format-nongpl]>=4.18.0->jupyter-events>=0.11.0->jupyter-server<3,>=2.19.0->jupyterlab->jupyter) (2026.3)

         3. Make a tutorial sub directory in home directory and Run tutorial
            '''
                  mkdir -p ~/scratch/mujoco-tutorial
                  cd ~/scratch/mujoco-tutorial
                  unset PYTHONPATH
                  source ~/student-robotics-training-WK3/.venv/bin/activate
                  curl -O https://raw.githubusercontent.com/google-deepmind/mujoco/main/python/tutorial.ipynb
                  jupyter notebook --no-browser --port=8888
            '''
            
            Expected Results:
               1. After inputted:<curl -O https://raw.githubusercontent.com/google-deepmind/mujoco/main/python/tutorial.ipynb>
                                     % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                                                    Dload  Upload   Total   Spent    Left  Speed
                                   100 75221  100 75221    0     0   282k      0 --:--:-- --:--:-- --:--:--  283k

               2. After inputted: <jupyter notebook --no-browser --port=8888>
                             [I 2026-08-08 15:34:55.372 ServerApp] jupyter_lsp | extension was successfully linked.
                             [I 2026-08-08 15:34:55.379 ServerApp] jupyter_server_terminals | extension was successfully linked.
                             [I 2026-08-08 15:34:55.384 ServerApp] jupyterlab | extension was successfully linked.
                             [I 2026-08-08 15:34:55.398 ServerApp] notebook | extension was successfully linked.
                             [I 2026-08-08 15:34:55.404 ServerApp] Writing Jupyter server cookie secret to /home/kevin-lianhu/.local/share/jupyter/runtime/jupyter_cookie_secret
                             [I 2026-08-08 15:34:56.001 ServerApp] notebook_shim | extension was successfully linked.
                             [I 2026-08-08 15:34:56.053 ServerApp] notebook_shim | extension was successfully loaded.
                             [I 2026-08-08 15:34:56.055 ServerApp] jupyter_lsp | extension was successfully loaded.
                             [I 2026-08-08 15:34:56.057 ServerApp] jupyter_server_terminals | extension was successfully loaded.
                             [I 2026-08-08 15:34:56.070 LabApp] JupyterLab extension loaded from /home/kevin-lianhu/student-robotics-training-WK3/.venv/lib/python3.12/site-packages/jupyterlab
                             [I 2026-08-08 15:34:56.071 LabApp] JupyterLab application directory is /home/kevin-lianhu/student-robotics-training-WK3/.venv/share/jupyter/lab
                             [I 2026-08-08 15:34:56.072 LabApp] Extension Manager is 'pypi'.
                             [I 2026-08-08 15:34:56.202 ServerApp] jupyterlab | extension was successfully loaded.
                             [I 2026-08-08 15:34:56.206 ServerApp] notebook | extension was successfully loaded.
                             [I 2026-08-08 15:34:56.206 ServerApp] Serving notebooks from local directory: /home/kevin-lianhu/scratch/mujoco-tutorial
                             [I 2026-08-08 15:34:56.207 ServerApp] Jupyter Server 2.20.0 is running at:
                             [I 2026-08-08 15:34:56.207 ServerApp] http://localhost:8888/tree?token=ae10d22d79e614964b51b5e9284930e15f76d3ccda2c0545
                             [I 2026-08-08 15:34:56.207 ServerApp]     http://127.0.0.1:8888/tree?token=ae10d22d79e614964b51b5e9284930e15f76d3ccda2c0545
                             [I 2026-08-08 15:34:56.207 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
                             [C 2026-08-08 15:34:56.211 ServerApp] 
    
                                 To access the server, open this file in a browser:
                                     file:///home/kevin-lianhu/.local/share/jupyter/runtime/jpserver-28399-open.html
                                 Or copy and paste one of these URLs:
                                     http://localhost:8888/tree?token=ae10d22d79e614964b51b5e9284930e15f76d3ccda2c0545
                                     http://127.0.0.1:8888/tree?token=ae10d22d79e614964b51b5e9284930e15f76d3ccda2c0545
                             [I 2026-08-08 15:35:02.088 ServerApp] Skipped non-installed server(s): basedpyright, bash-language-server, dockerfile-language-server-nodejs, javascript-typescript-langserver, jedi-language-server, julia-language-server, pyrefly, pyright, python-language-server, python-lsp-server, r-languageserver, sql-language-server, texlab, typescript-language-server, unified-language-server, vscode-css-languageserver-bin, vscode-html-languageserver-bin, vscode-json-languageserver-bin, yaml-language-server

   Task #5
            1. Create the file in your repo
                '''
                    cd ~/student-robotics-training-WK3
                    nano scripts/mujoco_smoke_test.py
                '''

            2. Coding in the file: mujoco_smoke_test.py

            3. Running
              '''
                 unset PYTHONPATH
                 source .venv/bin/activate
                 python scripts/mujoco_smoke_test.py
              '''

              Expected Results:
                                [PASS] mujoco smoke test: 100 steps completed
                                       simulation_time=0.0200
                                       mujoco version=3.x.x

            4. Save the results as evidence
               '''
                  mkdir -p evidence/logs
                  python scripts/mujoco_smoke_test.py | tee evidence/logs/smoke_test_output.txt
               ''' 

   Task #6
            1. Attempt the viewer
               '''
                   unset PYTHONPATH
                   source .venv/bin/activate
                   python -m mujoco.viewer 2>&1 | tee evidence/logs/viewer_attempt.txt
               '''

               If that opens a window (even an empty one), try loading a real model into it — press Ctrl+L inside the viewer, or launch it programmatically via the file path: scripts/viewer_attempt.py (scratch/throwaway — doesn't need to be committed)
                 ''' 
                    import mujoco
                    import mujoco.viewer

                    model = mujoco.MjModel.from_xml_string(
                         "<mujoco><worldbody><geom type='plane' size='1 1 0.1'/></worldbody></mujoco>"
                    )
                    data = mujoco.MjData(model)
                    mujoco.viewer.launch(model, data)
                 '''
            
            2. If it fails — capture the exact error, don't paraphrase it
               Whatever you get, keep the full, verbatim traceback — not a summary.

   Stretch Goals
      1. Save a short rendered video or frame sequence
         Frame Sequence:
         '''
            unset PYTHONPATH
            source .venv/bin/activate
            python scripts/save_frame_sequence.py
         '''
         Short Rander Video:
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

           Expected Results:
                          Model Statistics:scripts/scenes/smoke_scene.xml
                           bodies (nbody):   2
                           joints (njnt):    1
                           geoms (ngeom):    2
                           actuators (nu):   0
                           qpos size (nq):   7
                           qvel size (nv):   6
                           joint 0: type=free, name=
      
      3. Add a small automated smoke test
          '''
            nano/touch tests/test_mujoco_env.py
            source .venv/bin/activate
            python tests/test_mujoco_env.py
          '''
          Expected Results:
             [PASS] model loads
             [PASS] simulation steps and sphere falls under gravity
             [PASS] no NaN/Inf in final state
             [PASS] all checks passed

          '''
             echo "exit code: $?"
          '''

          Expected Result:
                          exit code: 0

## Problems encounted
     Engineering Tasks
        
            #2 Create a Python virtual environment and document the exact Python version used.
               
               1. I was not sure whether I should deactivate the virtual environment if I want to commit tracked files. I asked Claude Code, it answered:
                    {
                        No, it's not required — deactivating and running git commit are unrelated. Git works the same whether your venv is active or not, since git is a system-level command, not something tied to your Python environment. 
                    }

                2. I didn't know what command to deactivate the python virtual environment. I asked Claude Code.
                   The command is: <deactivate>

                  Note: No arguments needed. It's a shell function that Python's venv module adds to your session when you activate the environment, and it works from anywhere as long as a venv is currently active. Your prompt will drop the (.venv) prefix once it's done, confirming you're back to the system Python.
            
            #4	Run the official MuJoCo Python tutorial or one official example.
                  Before I started the offical tutorial file, I had been in "student-robotics-training-WK3" repo directory, I was not sure whether I should download the tutorial to my current directory.

                  I asked Claude Code: [
                               Now I currently in the root directory "student-robotics-training-WK3", should I run the commands: <curl -O https://raw.githubusercontent.com/google-deepmind/mujoco/main/python/tutorial.ipynb>and <jupyter notebook --no-browser --port=8888> in the current directory?
                             ]

                   The Claude Code recommended not running these in the repo root — do this exploration outside the repo instead. A few reasons:
                                 ● The tutorial notebook isn't a deliverable — it's not in your recommended repo structure (README.md, .gitignore, requirements.txt, docs/, models/, scripts/, tests/, evidence/). There's no "correct" place for it to live there.

                                 ● Launching Jupyter creates a hidden .ipynb_checkpoints/ folder wherever the notebook sits — one more thing you'd have to remember to .gitignore for no real benefit.

                                 ● Jupyter's file browser will also show your entire repo tree (docs, scripts, evidence, etc.) in the browser tab, which is just noisy and irrelevant to what you're doing right now.

                                 ● Keeping exploration cleanly separate from deliverables matches the philosophy your handbook keeps repeating — don't let throwaway/reference material blur into what needs to be reproducible.

                   Then It told me to run it in another directory with commands:
                                                         '''
                                                            mkdir -p ~/scratch/mujoco-tutorial
                                                            cd ~/scratch/mujoco-tutorial
                                                            unset PYTHONPATH
                                                            source ~/student-robotics-training-WK3/.venv/bin/activate
                                                            curl -O https://raw.githubusercontent.com/google-deepmind/mujoco/main/python/tutorial.ipynb
                                                            jupyter notebook --no-browser --port=8888
                                                         '''
                   Once I'm done exploring, just leave the notes/insights in docs/mujoco_setup.md back in your repo (as we discussed), and the scratch folder can sit untouched or get deleted — it was never meant to be tracked.



## Notes for Future Students
   Tasks #2, #3
     Steps:
            #1 Check the version of your Python, then create the venv

               ● <python3 -m venv .venv>
                
                -- python3
                   tell the Linux/WSL to run Python3

                -- '-m'
                     '-m' means run a Python module as a program; Python3 is being asked to find and execute a module that is installed/available in Python3.

                -- 'venv'
                    'venv' is a Python3's built-in virtual environment module;
                    A virtual environment creates an isolated Python environment for a project.

                -- '.venv'
                      the directory name where the virtual environment will be created

                      The leading '.' in '.venv' is a Linux convention meaning the directory is hidden when using a normal <ls> command. To display the directory, you need to input 
                       <ls -a>

                Note: After inputting this command, if you actually not have Python 3.x, you need to install a specific version:
                  '''
                     sudo apt install python3.12 python3.12-venv
                  '''
                  then run:
                  '''
                     python3.12 -m venv .venv
                  '''

            #3 Install MuJoCo and freeze dependencies
                
                ● <pip install --upgrade pip>
                   -- 1st pip
                        'pip' is a Python's package manager; It downloads and installs Python software packages

                   -- 'install' 
                       
                       download and install a target package

                   -- '--upgrade'
                       
                       this option tells the package manager: 'pip',
                       "If the package is already installed, replace it with a newer version if one is available."

                   -- 2nd 'pip'
                       the name of the target package that you want to install/upgrade

                ● <pip freeze > requirements.txt>

                   -- 'freeze'
                          List all the Python packages currently installed in this environment, including their exact versions.

                   -- '>'
                       A shell output redirection
                          it means: Take the output from the command on the left and write it into the file on the right.
            
            #4 Confirm '.venv/' is ignored
                ● <grep -n "venv" .gitignore>

                  serarch the text: "venv" in the file: ".gitignore"

                  - '-n'
                      Show the line number along with each matching line.

   Task #4
          Step 3: download the tutorial and save it
                ● <curl -O https://raw.githubusercontent.com/google-deepmind/mujoco/main/python/tutorial.ipynb>

                  -- 'curl'
                      'curl' is the program that communicates with the web server.

                       Here, it sends an HTTP/HTTPS request to GitHub and retrieves the requested file.
                  
                  -- '-O'
                      uppercase letter 'O' not the number zero/0
                     
                       It means: "Save the downloaded data to a local file whose name comes from the URL."
                     This name is also called '--remote-name'

                      So this command will first create a file with name "tutorial.ipynb" in current work directory

                ● <jupyter notebook --no-browser --port=8888>
                    
                     jupyter      notebook       --no-browser       --port=8888
                        │             │                │                 │
                        │             │                │                 └─ use port 8888
                        │             │                └────────────────── don't open browser
                        │             └────────────────────────────────── start Notebook server
                        └──────────────────────────────────────────────── Jupyter program

                     -- 'jupyter'
                          
                          This invokes the Jupyter command-line program.
                          Jupyter is an environment for working interactively with things such as Python code, explanations, equations, and output.

                     -- 'notebook'
                         
                          'notebook' starts a notebook server; The server provides a web-based interface through which you can open and run .ipynb files.

                     -- '--no-browser'
                          This option means: Do not automatically open a web browser when Jupyter starts.

                          Normally, Jupyter may try to launch a browser automatically. hat's inconvenient in WSL because Jupyter is running inside Linux/WSL, while your graphical browser is normally running in Windows.

                     -- '--port=8888'
                          This option means: Tell the Jupyter server to listen for connections on network port 8888.
                          Here you're choosing 8888 as Juypter's doorway

                     After running this command: jupyter starts a server in current work directory: /scratch/mujoco-tutorial
                        
                          Conceptually:
                                               WSL
                                                ┌─────────────────────────────────────┐
                                                │                                     │
                                                │  /home/yourname/mujoco/             │
                                                │       │                             │
                                                │       └── tutorial.ipynb            │
                                                │                                     │
                                                │       Jupyter Notebook Server       │
                                                │              │                      │
                                                │          port 8888                  │
                                                │              │                      │
                                                └──────────────┼──────────────────────┘
                                                               │
                                                               │ localhost:8888
                                                               ↓
                                                         Windows Web Browser

   Task #5
         
         ● Python Codes in "mujoco_smoke_test.py"
          
          -- Line 11: <MODEL_XML = "<mujoco><worldbody/></mujoco>">
                   this defines a minimal MJCF(MuJoCo XML) model as a Python string.

                   ● <mujoco> is the root element required by every MuJoCo model file; 
                      XML (and MJCF, which is MuJoCo's XML-based model format) uses paired tags to mark the start and end of an element:
                              ● <mujoco> -- opens the element, marking the beginning of the model definition

                              ● </mujoco> -- closes it, marking the end; the / before the tag name is what signals "this is a closing tag"

                                  Since <mujoco> is the required root element of every MJCF file, </mujoco> simply terminates that root element, making the string a complete, well-formed XML document. If it were missing, the parser (mujoco.MjModel.from_xml_string) would raise an XML parsing error because the <mujoco> element would never be closed
                   
                   ● <worldbody/> is the top-level container for all physical objects(bodies, geoms, lights, etc.) in the scene.
                    
                     Here it's empty — no bodies, geoms, or joints — so this is the simplest possible valid scene, just enough to prove MuJoCo can parse and compile a model.

                     Note that <worldbody/> is written differently — it's a self-closing tag (ends in />), used because it has no content in this minimal example. That's shorthand for <worldbody></worldbody>.

                This segment creates the description of the simulation model that MuJoCo model will later compile
          
         
          -- Line 17: <model = mujoco.MjModel.from_xml_string(MODEL_XML)>
                  ● 'mujoco'
                       This refers to the MuJoCo Python package imported on line 9:
                        '''
                           import mujoco
                        '''

                  ● 'MjModel'
                      This is a MuJoCo class: simulation to complied/static description of the scene

                  ● 'from_xml_string(...)'
                      It is a method/function that:
                                            takes a MJCF model provided as a string arguement as input and complie it into an output: MjModel.

          -- The Overall process for lines 11, 17:
                                                   MODEL_XML
                                                       │
                                                       │ XML string
                                                       ▼
                                                   from_xml_string()
                                                       │
                                                       │ compile
                                                       ▼
                                                   MjModel
                                                       │
                                                       ▼
                                                     model
                   
                 An important distinction is that line 11 describes the model, while line 17 creates the actual MuJoCo model object from that description.

          -- Line 21: <data = mujoco.MjData(model)>     

                       ● MjData(...)
                          take the given parameter and create an MjData object;
                          MjData: the mutable, current state of simulation 
                          
                          mujoco.MjData(model)
                                  creates the MuJoCo data structure using the 'model'(MjModel) created on line 17.
      
          -- Line 25: <mujoco.mj_step(model, data)>
                    advances the MuJoCo simulation by one simulation timestep

                  Arguments: 
                              'model': what the simulation is

                              'data': what the current state

                  Then, function/method mj_step(...) performs the simulation step and updates data.

         ● Relevant Commands

             -- <nano scripts/mujoco_smoke_test.py>

               -- 'nano'
                   'nano' is a simple, terminal-based text editor available in Linux/WSL
                    Unlike graphical editors such as VS Code, Nano runs inside your terminal.

            -- <python scripts/mujoco_smoke_test.py | tee evidence/logs/smoke_test_output.txt>

                -- '|'
                    
                    It is called 'pipe' operator; Connect the output of one command to the input of another command

                -- 'tee'
                      
                        The name comes from the Unix tee command behaving like a T-shaped pipe:
                                                                ┌──► terminal
                                                                │
                                                  input ───────►┼
                                                                │
                                                                └──► file
                        The input is split into two directions, resembling the letter T.

                        'tee' is a command/program:
                                       Takes input and sends a copy into the target file and current terminal

   Task #6
          -- <glxinfo -B 2>&1 | head -20>

                  ● 'glxinfo'

                      glxinfo is a Linux utility that reports information about OpenGL and the GLX graphics system.

                  ● '-B' 
                    '-B' is an option: brief; Instead of displaying the enormous amount of information that glxinfo can provide, -B asks it to display a shorter summary of the important OpenGL information.

                  ● 'head'
                     An Linux utility display the beginning of its input

                  ● '-20'
                      display the first 20 lines 

   Stretch Goals:
          1. Save a short rendered video or frame sequence 

             -- frame_sequence.py
                  - <os.makedirs(OUTPUT_DIR, exist_ok=True)>
                   
                    ● exist_ok=True
                        exist_ok=True tells Python not to raise an error if the directory already exists

                  - <renderer = mujoco.Renderer(model, height=480, width=640)>
                     
                     ● Renderer
                      Renderer is a class in mujoco model

                     ● height=480, width=640
                       
                        the size of rendered image is: 480x640 pixel

                  - <renderer.update_scene(data)>
                    
                     ● update_scene(...)
                        
                        
                        update_scene() is a MuJoCo method that prepares the renderer's internal scene representation based on the current simulation state.
                     
                  - <Image.fromarray(renderer.render()).save(f"{OUTPUT_DIR}/frame_{i:03d}.png")>
                     
                     ● renderer.render()
                      
                       renders that scene into image data: NumPy array containing the image pixels.

                     ● Image.fromarray(...)

                         fromarray() converts the NumPy array produced by MuJoCo into a Pillow Image object.

                     ● {i:03d}
                          Take the integer i and format it as a 3-digit decimal number, adding leading zeros when necessary.                     

                   - <writer = imageio.get_writer(f"{OUTPUT_DIR}/sphere_drop.mp4", fps=30)>

                      ● get_writer(f"{OUTPUT_DIR}/sphere_drop.mp4", fps=30)
                        Asks ImageIO to create a writer for a video file
 
                        'fps': frames per second
                        Play/store the video at 30 frames per second.

          2. Inspect model statistics such as number of bodies, joints, actuators, qpos, and qvel
             In executable: scripts/stretchgoal2_model_stats.py
             -- <jtype = joint_types.get(model.jnt_type[i], "unknown")>
                Get the joint type number from MuJoCo, look up its corresponding name in joint_types, and if that number isn't in my dictionary, use 'unknown' instead.