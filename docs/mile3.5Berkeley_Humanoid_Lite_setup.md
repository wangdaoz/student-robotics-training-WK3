## Computer
   - Operating system: WSL 
   - Python version: Python 3.12.3
   - Git version: 2.43.0
   - VS Code installed: yes
   - Claude Code installed: yes

## Steps Completed && Commands Used

 Suppose your local repo didn't have the submodule repo: Berkeley Humanoid Lite Assets repo.

Engineering tasks:

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

## Problems encounted

## Notes for Future Students

        1. Task #23:
            in the file: scripts/inspect_berkeley_model.py:

            <name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i)>
            <name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_ACTUATOR, i)> 

          - The core idea: MUJOCO complies your model into flat arrays

           When MuJoCo loads your MJCF, it doesn't keep a tree of named XML elements around at runtime. Instead, it compiles everything into flat, numbered arrays for speed — joint 0, joint 1, joint 2, ... actuator 0, actuator 1, ... and so on. Your <joint name="leg_right_hip_roll_joint" .../> tag becomes, internally, just "joint index 14" (or whatever number it lands on based on where it appears in the body tree).

           The names you wrote in the XML aren't thrown away — they're stored in a separate lookup table so you can still ask "what's the name of joint #14?" or the reverse, "what's the index of the joint named X?" That's what mj_id2name and mj_name2id are for.

           - mujoco.mjtObj.mjOBJ_JOINT

             this tells MuJoCo which category of object you're asking about. MuJoCo has separate numbering for joints, actuators, bodies, geoms, sensors, etc. — joint index 3 and actuator index 3 are completely unrelated objects. mjtObj is an enum listing all these categories (mjOBJ_JOINT, mjOBJ_ACTUATOR, mjOBJ_BODY, mjOBJ_GEOM, ...), so you have to specify which namespace i refers to.

           - mujoco.mjtObj.mjOBJ_ACTUATOR

             same as mentioned above, tell MuJoCo, you ask're asking about autuator category (mjOBJ_ACTUATOR) 

           - Return value of mujoco.mj_id2name(...)
              the string name you gave that that joint/actuator in XML(e.g. "leg_right_hip_roll_joint"), or None if that joint/actuator was never given a "name= " attribute.

           2. <joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, name="leg_right_hip_roll_joint")>

      
        2. Task #27

             ● <Image.fromarray(renderer.render()).save("evidence/screenshots/before.png")>

                -- renderer.render()
                   tell MuJoCo "renderer" to render the current scene;
                   The result is typically an image represented as a NumPy array, containing pixel data.

                -- Image.fromarray(renderer.render())

                   takes the NumPy array produced by (renderer.render()) and converts it into a Pillow image object.

                -- .save("evidence/screenshots/before.png")

                   saves the Pillow image as a file.

             ● <imageio.mimsave("evidence/screenshots/control_sequence.gif", frames, fps=10)>
                """Save multiple images as an animated image/video."""
   
   # Concepts to Explore

       • Model compilation errors

           When you call <mujoco.MjModel.from_xml_path(...)>, MuJoCo doesn't just parse XML; it complies the model in the XML file: resolving includes, loading every referenced mesh file, computing interia properties and building the flat runtime arrays. Any failure in that pipeline raises an error before you get a usable model.

           E.g.
                        { Traceback (most recent call last):
                              File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/inspect_berkeley_model.py", line 11, in <module>
                                model = mujoco.MjModel.from_xml_path(MODEL_PATH)
                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                            ValueError: Error: Error opening file '/home/kevin-lianhu/student-robotics-training-WK3/models/berkeley/Berkeley-Humanoid-Lite-Assets/data/robots/berkeley_humanoid/berkeley_humanoid_lite/mjcf/merged/leg_right_ankle_roll_visual.stl' }

               a missing mesh was a compilation error, not a runtime one. The skill here is reading these errors precisely: they usually name the exact missing file or malformed element, which is far more useful than treating "it didn't load" as one undifferentiated failure.

      • Named lookup with mj_name2id and mj_id2name
         
         the compiled model stores joints/actuators/bodies as flat numbered arrays, and these two functions translate between the human-readable names in your XML and the numeric indices MuJoCo actually uses internally.

         E.g. 
            Inspection script:
                           '''
                               <name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i)>
                           '''

            Control script:
                         '''
                             joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, JOINT_NAME)
                             actuator_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, ACTUATOR_NAME)>
                         '''

      • Actuator-to-joint mapping

          An actuator and a joint are two separate objects that happene to be linked, not the same thing. 
          The joint defines a degree of freedom (e.g. arm_right_shoulder_pitch_joint, a hinge); 
          the actuator is what applies force/torque to that joint (<motor joint="arm_right_shoulder_pitch_joint" .../>).

          This mapping is stored in <model.actuator_trnid[actuator_id, 0]>. This type of mapping matters because names can be mislead: someone can name an actuator something unrelated to the joint it actually drives, so verifying the link, not just that both names exist, is the real safety check.

      • Free joints and floating bases
         
           Free joint: 6 degrees of freedom in the world (3 translation, 3 rotation)
                       e.g.
                            base_freejoint

           Floating base: not bolted to the ground

      • Inital Pose

          The pose your model starts in before you run any simulation steps.
            e.g.
               qpos after lines 102, 103('mj_resetData' + 'mj_forward') in contril script.

         This matters practically: 
                                  recall arm_right_elbow_pitch_joint's range was [-90°, 0°], so at the default initial qpos=0, that joint starts already at its upper limit — a very different starting condition than arm_right_shoulder_pitch_joint, which starts safely mid-range. Knowing your initial pose before you command any control input is what let us catch that difference and choose the safer joint.

      • Joint range and control range

          • Joint Range(model.jnt_range)-- the physical angle limits of the joint itself, in radians.
              
                    E.g. shoulder pitch: roughly −90° to +45°

          • Control/force Range: the limit on how much torque the actuator can apply, independent of where the joint currently is
            (±20 N·m here).

      • Safe control amplitude

         In practical discipline, ensure your command control input small relative to the actuator's actual force capability. because the ticket explicitly rules out large control values, and because a small, well-understood input gives you a clean, reproducible before/after measurement instead of a violent, possibly unstable motion.

         E.g.
             <MAX_SAFE_CTRL = 5.0>

      • Headless state verification

           Proving something happened in simulation without relying on a human looking at a viewer window — which matters because viewers need a display, may not run reliably over SSH/WSL, and (as the ticket stresses) visual evidence alone isn't sufficient proof anyway.

           E.g.
                My CSV log does: initial_qpos/final_qpos/delta_qpos are numeric, exact, and checkable by a script or a reviewer with no GUI at all — the screenshot/GIF from Task 27 is a supplement to this, not a replacement for it.

   # Suggested AI Exploration

        •	Explain this MuJoCo model-loading error and identify the exact missing path or XML element.

              Error:
                     [
                            Traceback (most recent call last):
                              File "/home/kevin-lianhu/student-robotics-training-WK3/scripts/inspect_berkeley_model.py", line 11, in <module>
                                model = mujoco.MjModel.from_xml_path(MODEL_PATH)
                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                            ValueError: Error: Error opening file '/home/kevin-lianhu/student-robotics-training-WK3/models/berkeley/Berkeley-Humanoid-Lite-Assets/data/robots/berkeley_humanoid/berkeley_humanoid_lite/mjcf/merged/leg_right_ankle_roll_visual.stl'
                     ]

         the exact missing path is: berkeley-humanoid-lite-assets/data/robots/berkeley_humanoid/berkeley_humanoid_lite/mjcf/assets/merged/

       •	 How can I map a MuJoCo actuator to the joint it controls?
         
          
          After you get the actuator ID: 
          '''
             actuator_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, ACTUATOR_NAME)
          '''
          Look up the tranmission type of the actuator:
          '''
             JOINT_TRANSMISSION_TYPES = {mujoco.mjtTrn.mjTRN_JOINT, mujoco.mjtTrn.mjTRN_JOINTINPARENT}

             trn_type = model.actuator_trntype[actuator_id]
             if trn_type not in JOINT_TRANSMISSION_TYPES:
                 raise ValueError(f"Actuator '{ACTUATOR_NAME}' is not joint-driven "
                                   f"(transmission type: {trn_type})")

          If the tramission type is qualiied, look up actuator's transmission target via the following codes:
          '''
             driven_joint_id = model.actuator_trnid[actuator_id, 0]
             driven_joint_name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, driven_joint_id)
          '''

        The general procedure is:
                                 Actuator name
                                     │  mj_name2id
                                     ▼
                                 actuator_id
                                     │
                                     ▼
                                 model.actuator_trntype[actuator_id]  ──►  is it mjTRN_JOINT / mjTRN_JOINTINPARENT?
                                     │  (yes)
                                     ▼
                                 model.actuator_trnid[actuator_id, 0]
                                     │
                                     ▼
                                 driven_joint_id
                                     │  mj_id2name
                                     ▼
                                 Joint name
       
         One important detail: actuator_trnid is specifically MuJoCo's actuator transmission-target array. The exact interpretation of its columns depends on the actuator's transmission type, so column 0 is commonly the primary transmission target (such as a joint ID for a joint transmission), rather than universally meaning "joint ID" for every possible actuator.

         There's no joint_actuator_id array — if you instead started with a joint and wanted "which actuator(s) drive this," you'd have to loop over every actuator, check actuator_trntype/actuator_trnid for each, and collect matches (a joint could even have zero or multiple actuators). Naming this asymmetry shows you understand why the direction in the question ("actuator to joint," not the reverse) was the easy direction to ask about.
      
       •	How should I safely move one joint on a floating-base humanoid without attempting balance control?

          A handful pf layer constraints that each rules out a different way balance control could sneak in.

          The core tension
              
              Every joint in this robot is part of one connected kinematic tree rooted at a floating base. Move any joint, and by Newton's third law the actuator's reaction torque acts back on the rest of the body too — including the base. So "isolating one joint" isn't automatic just because you only command one actuator; it has to be engineered in.

          Layer 1 -- Pick a joint where the coupling doesn't matter
              
              Choosing arm_right_shoulder_pitch_joint over a leg/ankle joint isn't just convenience — it removes the contact dimension of balance. Legs touching a floor introduce friction, normal forces, and tipping moments the moment they move; an arm swinging in open air doesn't. This doesn't eliminate reaction dynamics (see Layer 3), but it eliminates the specific failure mode of "the robot falls over or slips."

         Layer 2 -- Keep the amplitude small and the duration finite

               Small --ctrl and a bounded n_steps loop (both already in your script) limit how much momentum the reaction can impart, and guarantee the simulator can't drift into instability indefinitely. This is what "safe control amplitude" from the concepts list is actually protecting against here.

         Layer 3 -- The subtle part: gravity isn't the only source of base motion

               --freeze-base's current implementation (zeroing gravity) stops the base from falling, but it does not stop it from moving in reaction to the arm's own torque — conservation of momentum means an internal torque between two connected bodies still produces equal-and-opposite motion on both sides, gravity or no gravity. Think of an astronaut in zero-g swinging one arm: their torso still counter-rotates slightly, even with nothing pulling them down.

               For a genuinely joint-isolated measurement, you need to actively hold the base still, not just remove gravity. Since MuJoCo won't let you add a new equality constraint to an already-compiled model (that array size is fixed at compile time from the XML), the clean code-only way to do this is to re-clamp the base's qpos/qvel back to their initial values every step:

               '''
                  if args.freeze_base:
                      base_joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, "base_freejoint")
                      base_qpos_adr = model.jnt_qposadr[base_joint_id]   # 7 slots: xyz + quaternion
                      base_qvel_adr = model.jnt_dofadr[base_joint_id]    # 6 slots: linear + angular velocity
                      base_qpos_initial = data.qpos[base_qpos_adr:base_qpos_adr + 7].copy()

                  for step in range(n_steps):
                      mujoco.mj_step(model, data)
                      if args.freeze_base:
                          data.qpos[base_qpos_adr:base_qpos_adr + 7] = base_qpos_initial
                          data.qvel[base_qvel_adr:base_qvel_adr + 6] = 0.0
               '''

               This is a genuine, disclosed, code-only modification (never touching the official XML), and it's a more rigorous version of what --freeze-base was gesturing at.

         Layer 4 — The structural guarantee: open-loop, not closed-loop

             This is arguably the most important layer, and it's a definitional one: balance control is, by definition, a feedback loop — a controller that reads the robot's tilt, center of mass, or contact state and adjusts output in response.

         Note: the control input is open-loop and independent of base state, therefore it is not balance control by construction," rather than just "I didn't try to balance it.

       •	Review my selected joint and control range for risk of unstable simulation

          Risk 1 — Sustained max effort, not a brief pulse

               The key detail: your control loop holds data.ctrl[actuator_id] constant for the entire --duration. Commanding ±20 N·m isn't a quick tap at full strength — it's continuous, full-capacity torque for the whole simulation window. That's a fundamentally different physical scenario than "small nudge," and it's the difference between "exercising the actuator" and "stress-testing it at its rated limit for seconds at a time."

         
          Risk 2 — The joint will reach its hard limit almost immediately, then keep being driven into it

               arm_right_shoulder_pitch_joint's total range is only about 135° (−90° to +45°). At sustained max torque, the arm segment will accelerate toward one end of that range and hit the mechanical limit within a small fraction of a second — long before your duration elapses. After that, the actuator keeps commanding full torque into an already-saturated joint limit for the remainder of the run. This is exactly the regime where MuJoCo's contact/limit solver has to fight a large sustained driving force with its limit-constraint stiffness — a classic trigger for jitter, energy injection, or solver non-convergence, depending on how the model's solref/solimp limit parameters and model.opt.timestep are tuned. (Worth checking model.opt.timestep yourself before drawing a firm conclusion here — I haven't verified its exact value, and a sufficiently fine timestep can absorb a lot of this that a coarse one can't.)

          Risk 3 — Reaction torque on the floating base

               Since the base isn't grounded, Newton's third law means driving the shoulder at max torque also imparts a proportionally large reaction on the torso — and without --freeze-base (or the stronger per-step clamp from the last exploration), that reaction is free to spin or tip the entire robot. At small --ctrl values this effect is negligible; at the rated maximum, it stops being negligible and starts looking like uncommanded whole-body motion — which directly undermines the "not balance control, not full-body motion" framing your demo is supposed to establish.

       • How can I prove a joint moved when the viewer is unavailable?

          write a control script that record the position and velocity for each timestamp.

          E.g.
               '''
                  for step in range(n_steps):
                      mujoco.mj_step(model, data)
                      log.append((float(data.qpos[qpos_adr]), float(data.qvel[qvel_adr])))
               '''
         Then input command to input these records to an log file and open the file to observe whether the records are changed at each timestamp.

         Revision:
         
         Gap 1 — "Observe if it changed" isn't proof; a threshold check is
             Floating-point state can drift by tiny numerical noise even with zero real motion — so "the numbers are different" alone is too weak a claim. What you actually want to prove is that the change exceeds noise by a wide margin and is attributable to your control input specifically. That means a scripted assertion, not a manual read-through:
             '''
                delta_qpos = abs(final_qpos - initial_qpos)
                NOISE_FLOOR = 1e-6  # rad, several orders below any real movement here
                assert delta_qpos > NOISE_FLOOR, (
                    f"qpos changed by only {delta_qpos:.2e} rad -- "
                    f"indistinguishable from numerical noise, not a real movement"
                )
             '''
             this is what makes the proof headless in the fullest sense — the concept isn't just "no GUI required to generate the evidence," it's "no human required to interpret it either." A file a person has to open and squint at is a weaker form of headless than a script that returns pass/fail on its own.

         Gap 2 — One trial isn't a controlled proof; add a negative control

                 Right now, a nonzero delta_qpos could in principle come from something other than your actuator — residual velocity from initialization, or (per the reaction-torque discussion a couple turns back) coupling from the floating base moving on its own. The rigorous way to isolate "this actuator caused this movement" is a classic control-group comparison: run the identical script twice, once with --ctrl 0 and once with your real value, and show the driven joint moves meaningfully in the second case and doesn't in the first (within your noise floor):

                 '''
                    python scripts/control_berkeley_joint.py --ctrl 0.0 --duration 3.0 --log-file evidence/logs/control_zero.csv
                    python scripts/control_berkeley_joint.py --ctrl 1.5 --duration 3.0 --log-file evidence/logs/control_active.csv
                 '''

                 That comparison — not either run alone — is what actually proves causation rather than just correlation-in-time.

         Revised per-step trajectory logging:

                 '''
                    trajectory_log = []
                    for step in range(n_steps):
                        mujoco.mj_step(model, data)
                        trajectory_log.append({
                            "step": step,
                            "sim_time_s": step * model.opt.timestep,
                            "qpos_rad": float(data.qpos[qpos_adr]),
                            "qvel_rad_s": float(data.qvel[qvel_adr]),
                            "ctrl_Nm": float(data.ctrl[actuator_id]),
                        })

                     with open("evidence/logs/control_berkeley_joint_trajectory.csv", "w", newline="") as f:
                         writer = csv.DictWriter(f, fieldnames=trajectory_log[0].keys())
                         writer.writeheader()
                         writer.writerows(trajectory_log)
                  '''

         One more thing this buys you for free
             A full per-step trajectory doubles as an instability detector, which ties directly back to the risk review from the last exploration: a before/after-only log can't distinguish "moved smoothly to a new position" from "spiked wildly mid-simulation and happened to end up somewhere reasonable." Scanning the trajectory for NaN, a sign flip in qvel, or a value oscillating near the joint limit gives you evidence about how it moved, not just that it moved — worth a line in docs/troubleshooting.md even if you don't end up needing it for this particular joint/ctrl choice.

      •	Help me design a model-inspection report using names rather than hard-coded indices.
          see the script in scripts/generate_berkeley_model_report.py

          -- line 73, lin3 100:

            <"\n".join(lines)>

             ● .join(...)
                a string method: takes an iterable of strings (here, lines) and glues them all together into one single string, inserting the string you called .join() on between each pair of elements.(e.g. insert a feedline ("\n") between each pair of elements)

   # Stretch Goals:
      
       •	Generate a joint/actuator CSV inventory

         This part has been finished in the last AI Exploration: Help me design a model-inspection report using names rather than hard-coded indices

         See details: scripts/generate_berkeley_model_report.py

       • Compare an MJCF model property with the corresponding URDF representation

         Same joint, two formats -- direct comparison (joint: arm_right_shoulder_pitch_joint )

         Property          URDF                               MJCF (compiled model)

          Position        <limit lower="-0.785398"            jnt_range = [-0.785, 1.571]
          limits          upper="1.5708"/>
 
          Effort/         <limit effort="20" .../>            forcerange="-20 20" on the
          force limit                                         <motor>

          Velocity        <limit velocity="15"/>              no equivalent field — MuJoCo's <motor> type has no built-in 
          limit                                               velocity cap

          Actuation       none                                <motor> element, separately defined

          Friction        <joint_properties                   frictionloss="0.1" on
                           friction="0.1"/>                    <default class="berkeley-humanoid-lite">
         __________________________________________________________________________________________________________________

      The position and effort limits match exactly, number for number — good confirmation that both formats were exported from the same underlying Onshape source. But three real structural differences fall out of this:
                                                     
          1. URDF has no concept of actuation at all

           '''
              grep -c "<transmission\|<actuator"
           '''
           on the URDF returns 0 — nothing, anywhere in the file. URDF only describes the robot's kinematic and inertial structure: links, joints, masses, and geometry. It has no native way to say "this joint is driven by a motor with this torque limit" — that's precisely why the URDF's effort limit lives inside the generic <limit> tag (a purely descriptive ceiling) rather than as a separate actuator object the way MJCF's <motor forcerange="..."> is. Actuation in a URDF-based pipeline (e.g. ROS) normally gets bolted on separately via <transmission> tags or a ros2_control config — neither of which this file has.

          2. The floating base is represented completely differently
             
             MJCF declares it explicitly: <freejoint name="base_freejoint"/> — an actual joint object with a name, an index, 7 qpos/6 qvel slots, all inspectable the same way as any other joint (this is exactly why your model report showed njnt=23 but nu=22). URDF has no equivalent concept whatsoever — the base link in the URDF simply has no parent joint at all; a URDF root link floating freely in the world is implicit, unnamed, and uninspectable as an object. You can't mj_name2id-style query "the floating joint" in URDF, because URDF doesn't model it as anything.

          3. Both separate visual from collision geometry — but differently

             • URDF: two entirely separate tags per link, <visual> (detailed mesh) and <collision> (here, a simplified <box size="0.15 0.14 0.23"/> for the base rather than the full mesh) — 27 <link> tags, 11 <collision> blocks total.

             • MJCF: a single <geom> tag per shape, distinguished by class="visual" or class="collision" referencing a <default> block (contype="0" conaffinity="0" for visual, meaning visual geoms don't participate in physics collision at all) — 27 visual geoms, 12 collision geoms.

            collision geom coount:

            URDF: 11 (lines: 13, 115, 157, 289, 331, 463, 487, 529, 643, 667, 709)

            MJCF: 12 (lines: 13, 24, 56, 71, 106, 121, 156, 164, 179, 207, 215, 230)

            Thus, a mismatch there could mean one link's collision shape didn't carry over cleanly between the two exports.