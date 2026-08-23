### Concepts to Explore

    ## Git submodules
        
         A submodule is a separate git repository embedded inside another git repository, pinned to one specific commit and tracked via a ".gitmodules" file.

         The parent repo doesn't store the submodule's files directly — it stores a pointer ("use commit X of repo Y"). That's why git clone alone leaves the submodule folder empty; you need '--recurse-submodules' or 'git submodule update --init' to actually pull the content in.

         E.g. 
            Parent repo: the official Berkeley Humanoid Lite repository
            Submodules: Berkeley Humanoid Lite Assets and Berkeley Humanoid Lite lowlevel 
                          they are both embedded inside the parent repo

    ##  Released assets versus repository source

        Released Assets:
               A tagged, packaged snapshot (like the v1.1.0 release we found) that the maintainers explicitly marked as a usable point-in-time.
            
        Repository Source:
               All things sit on a branch/submodule right now

        A release archive is stable and tested but frozen — you'd have to manually re-download to get updates, and it can't be wired into your own repo as a live submodule.
        E.g. the official Berkeley Humanoid Lite repository and the Berkeley Humanoid Lite Assets repository

        A repository source might be released or not be released.

        A unreleased branch/submodule is unstable. It might in the process of change or miss generated files.
        If you clone a submodule, you are given full git history which is useful for tracking future updates or debugging via commit log.

        E.g. the Berkeley Humanoid Lite Lowlevel repository is not released

          

    ## MJCF include files

      <include file="..."> lets one MJCF file pull in another file's contents at load time, so you can split a model into reusable pieces.

      E.g. 
         In assets repo, in subfolder: 'mcjf'
         'bhl_scene.xml' includes 'berkeley_humanoid_lite.xml', keeping ground plane/lighting/skybox separate from the robot's own body definition — so the same robot file can be reused in different scenes without duplicating it.
          
    ##  Mesh paths and relative paths

        <compiler meshdir="..."> sets a base folder that every <mesh file="..."> reference is resolved against.

        The catch (and the whole reason this is called out as its own concept to explore): that base path is relative to something, and it's not always obvious what — often the XML file's own location on disk, not wherever you launched a script from.

        E.g.
            berkeley_humanoid_lite.xml declares meshdir="assets", but no assets/ folder exists alongside it — the README instead describes a sibling meshes/ folder. That's the concept in action: an unresolved relative path is a silent failure until someone actually tries to load the file.

    ##  URDF versus MJCF

       Similarity:
                   Both are XML formats describing a robot's links, joints, and geometry

       Difference: built for different ecosystems:
        
                    ● URDF: originated in ROS and is broadly portable — supported by ROS, Gazebo, PyBullet, and importable into Isaac Sim — but its expressiveness is fairly basic (links, joints, simple collision/visual geometry).

                    ● MJCF: MuJoCo's native format and far more expressive for physics: 
                           contact solver parameters, tendons, equality constraints, actuator gain/dynamics, sensors, keyframes — none of which URDF can represent natively.

                    E.g. 
                         The repo reflects this tradeoff directly: it ships both a urdf/ and an mjcf/ directory for the same robot, plus a convert_urdf_to_usd.py script — suggesting URDF is treated as the portable "source of truth" description, while MJCF is a parallel, hand-maintained export specifically for MuJoCo-based training, and USD is a separate export for Isaac Sim.

    ## Licensing and attribution

                The key idea:
                             code and assets can carry different licenses within the same project, and they do here

                             E.g. MIT for code, CC BY-SA 4.0 for the CAD/asset models

                MIT mainly requires keeping a copyright notice; CC BY-SA's "ShareAlike" clause requires anything derived from those assets to be released under the same license, plus attribution to the original creators.

                If you ever build on top of these assets and redistribute anything, the asset license — not the code license — governs what you owe

    ## Model version and commit pinning
       
         Because everything above (mesh paths, includes, even which files exist) can change between commits, "I used the official repo" isn't a reproducible statement on its own — it's a moving target.

         Pinning: recording the exact tag or commit SHA you inspected (like we set up with ''' git rev-parse HEAD ''' earlier), so someone else — or you, in six months — can retrieve the byte-identical files you were looking at, rather than whatever main happens to contain later.

### Suggested AI Exploration

    •	Explain the tradeoff between cloning a repository with submodules and downloading a released asset archive

       - Cloning with submodules(<git clone --recurse-submodules xxx>):
        pulls the parent repo's full git history and pins the submodule to whichever commit the parent repo's tree records — that pin is a real git object, not a note you have to maintain yourself. You get the ability to run git log on either repo, diff between commits, and move the submodule forward with <git submodule update --remote> when you want newer assets.

       - Downloading a released asset archive
                     grabbing a packaged snapshot from a tagged release — no .git folder, no history, just the files as they existed at that tag. Smaller, faster, and requires zero git knowledge to use.

              
      Tradeoffs
                        Cloning with submodules                                Released asset archive
      Reproducibility    Exact: commit SHA is a                                depends on your own record-keeping
                         verifiable object                                      of which tag you grabbed
      _____________________________________________________________________________________________________________
      Stability          unstable                                                    Stable
      _____________________________________________________________________________________________________________
      Size/speed         Larger — includes                                           Smaller -- files only, no
                         commit history for both repos                                  history
      ______________________________________________________________________________________________________________
      Updating later    <git submodule update --remote>+ diff                   Manually re-download and diff yourself
      ________________________________________________________________________________________________________________
      Tooling needed      Git, and specifically                                      None -- just zip
                           submodule commands 
                           (a common source of confusion — "empty folder" is 
                           the #1 submodule gotcha for newcomers)
      ________________________________________________________________________________________________________________
      CI/pipeline       Can complicate CI auth if submodules are private            Avoid that entirely
       friction                     or use a different URL scheme 
      ________________________________________________________________________________________________________________
      
      The gotcha worth knowing specifically
       
       GitHub's auto-generated release archives — the "Source code (zip)" / "Source code (tar.gz)" links on a Releases page — do not include submodule content. They're literally just git archive of that tag, and git archive doesn't recurse into submodules. So if you download that zip for this repo expecting the assets to be inside it, you'd get an empty placeholder where the submodule should be — same problem as forgetting --recurse-submodules, just less obvious why. The only way an archive would include the assets is if the maintainers manually attached a separately-built asset bundle to the release (a real uploaded file, not the auto source zip) — worth checking for on the Releases page rather than assuming.

    •	How do MJCF include paths and mesh paths resolve?

        MJCF include paths resolve

        For a MuJoCo's own documentation, an <include> path is resolved relative to the directory of the main MJCF file: the top level file you actually load (e.g. MjModel.from_xml_path(xxx)).

        Mesh paths resolve

        the <complier meshdir="..."> is also resolved relative to the main file's directory: the top level file you actually load.

    •	What information should I record so another engineer can reproduce an exact robot model?

         1. Repository identity -- plural, not singular

            Record both repo URLs separately: the main repo and the Assets repo. They're two different git histories with two different commit spaces -- "I used commit X" is ambiguous unless you say which repo X belongs to.

         2. Exact pin(commit SHA), not just label/tag

            For each repo: the tag name and the commit SHA (git rev-parse HEAD). 
            Record both, not just one — a tag is a movable label under the hood (someone could theoretically delete and re-cut it), while a SHA is the actual immutable content pointer. The tag is for a human to recognize; the SHA is the ground truth if anything's ever in doubt.

         3. Exact clone procedure, including the flag that's easy to skip
            '''
               git clone --recurse-submodules https://github.com/HybridRobotics/Berkeley-Humanoid-Lite.git
               cd Berkeley-Humanoid-Lite
            '''
            '''
               git checkout v1.1.0 / git checkout aa93e47
               git submodule update --init --recursive
            '''
            Note: fill in the actual tag/commit SHA from your own git rev-parse HEAD — don't leave a placeholder in the real deliverable.

         4. The working-directory assumption
            
            Where someone needs to cd to before running anything — repo root, per the README. This one isn't inferred from a config file anywhere; it's a convention the maintainers state in prose, so it has to be copied into your own notes explicitly or it's lost.

         5. The exact entry file
            the specific relative path, and which variant (full robot vs. biped)

         6. The include/dependency chain
            
             Which files include which (scene → robot), and — just as important — a note that the robot files themselves have no further includes. Stating "no further dependencies" is itself useful information; someone reproducing this shouldn't have to re-verify that absence themselves.

         7. How relative paths resolve, plus any that don't

            Documenting a known-broken path is arguably more valuable than documenting only the working ones; it saves the next person from independently rediscovering the same dead end.

            E.g. 
                 The meshdir setting, resolved against the main file's directory (per the rule we just confirmed), and — critically — the fact that this particular resolution currently fails, since no assets/ folder exists there.

         8. Tooling version, not just asset version

            record the MuJoCo package version you tested with, check via
            '''
               pip show mujoco
            '''

            '''
               python -c "import mujoco
               print(mujoco.__version__)
            '''

            MJCF's compiler behavior has changed across MuJoCo versions historically — a model that compiles clean on your version isn't guaranteed to on another. "Reproduce the exact model" quietly assumes "with the same compiler," and that assumption is worth making explicit rather than leaving implicit.

         9. License and attribution
            
             Which license governs code vs. assets, since — as covered earlier — they differ here, and that governs what an engineer downstream is legally allowed to do with what they reproduce.

         10. Any workaround you had to apply, labeled as workaround
            
             E.g.
                 If you used the structure-only stripped XML to get the model to load at all, say so explicitly — and label it as producing a kinematics-only variant, not the real model. Otherwise the next person either can't reproduce your exact steps, or mistakes your workaround output for the genuine article.

    •	Compare what URDF can represent with what MJCF can represent

                Similarity:
                   Both are XML formats describing a robot's links, joints, and geometry

                Difference: built for different ecosystems:
        
                    ● URDF: originated in ROS and is broadly portable — supported by ROS, Gazebo, PyBullet, and importable into Isaac Sim — but its expressiveness is fairly basic (links, joints, simple collision/visual geometry).

                    ● MJCF: MuJoCo's native format and far more expressive for physics: 
                           contact solver parameters, tendons, equality constraints, actuator gain/dynamics, sensors, keyframes — none of which URDF can represent natively.

                    E.g. 
                         The repo reflects this tradeoff directly: it ships both a urdf/ and an mjcf/ directory for the same robot, plus a convert_urdf_to_usd.py script — suggesting URDF is treated as the portable "source of truth" description, while MJCF is a parallel, hand-maintained export specifically for MuJoCo-based training, and USD is a separate export for Isaac Sim.