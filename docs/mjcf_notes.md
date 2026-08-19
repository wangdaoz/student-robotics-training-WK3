## models/simple_arm.xml

  -- <compiler angle="radian" coordinate="local"/>
      function: <compiler> doesn't add anything to the physical model — it just tells the MJCF parser how to interpret certain values in the rest of the file before compiling it into the internal mjModel. It has no effect once compilation is done.

        ● angle="radian"
          This says every angle-valued number in the file — joint range, hinge axis angles, euler orientations, etc. — is written in radians, not degrees. MJCF actually defaults to degrees if you don't set this. That's why it matters here: our joint ranges are written as range="-1.5708 1.5708". If the compiler assumed degrees (the default), it would read that as an almost-zero range instead of ±90°, and the shoulder joint would barely move at all. Setting angle="radian" makes sure 1.5708 is read as π/2 radians = 90°, matching what we intended.

        ● coordinate="local"

           This says each body's pos/quat/euler in the file is expressed relative to its parent body's frame, not the world frame — so forearm's pos="0 0 0.3" means "0.3m up the z-axis of upper_arm," not "0.3m up the z-axis of the world." That's what lets the kinematic chain nest cleanly: move upper_arm, and forearm moves with it automatically, since its position is defined relative to it.
  -- <geom rgba="0.7 0.7 0.75 1"/>
      
      ● 'rgba'
         sets the color and transparency of that geom, as four numbers each ranging from 0 to 1:
                    ● r — red channel

                    ● g — green channel

                    ● b — blue channel

                    ● a — alpha (opacity): 1 (fully opaque; 0 would be fully transparent)

                    So 0.7 0.7 0.75 1 is a light, slightly cool-toned gray — the r, g, and b values are all close together (grayscale) with just a touch more blue, giving it a faint steel/silver tint. That value's sitting inside the <default> block, so it's not attached to one specific geom — it's the fallback color any <geom> in the file gets unless it sets its own rgba (which is why floor and base_geom in the model override it with their own values, while upper_arm_geom and forearm_geom just inherit this default gray).

                    If you want to change the arm's color, you can either edit that default line, or add an rgba="r g b a" attribute directly to an individual geom to override it just for that one.

  -- <light name="key_light" diffuse="0.8 0.8 0.8" pos="0 0 3" dir="0 0 -1"/>

       <light> adds a light source to the scene so you can actually see the model when it renders — it has zero effect on the physics, purely visual.

          ● name="key_light"
              identifies this light, same idea as naming a body or joint. Not strictly required for a light (nothing else in the file needs to reference it), but naming it keeps the "everything named" convention from the ticket consistent throughout the file.

          ● diffuse="0.8 0.8 0.8"
               the color of light this source casts, as RGB values from 0 to 1. 0.8 0.8 0.8 is a neutral, slightly-dimmed white (not 1 1 1, which would be pure white at full brightness). This is the light equivalent of a geom's rgba, minus the alpha channel — light doesn't have transparency.

          ● pos="0 0 3"
               the light's location in 3D space: x=0, y=0, z=3, so it sits 3 meters straight up from the origin, above the whole arm.

          ● dir="0 0 -1"

               the direction the light points: straight down the z-axis. Combined with pos, this places a light 3m overhead pointing straight down at the scene, like an overhead studio light.

          Note:
              this light doesn't set the directional attribute, and directional is one of the light element's available attributes alongside pos and dir. Left unset, it defaults to a point light — it radiates outward from that pos location in all directions the dir cone allows, so distance from the light affects brightness, similar to a lamp. Setting directional="true" would instead treat it like sunlight — parallel rays with no falloff by distance, coming from the direction dir points regardless of pos. For a small arm model like this, the difference is barely visible, but it becomes important once you're rendering something larger like the full Berkeley Humanoid model in Milestone 3.5.

## scripts/load_simple_arm.py
  
        -- <MODEL_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "models", "simple_arm.xml"))>

              ● '__file__'
                 
                 '__file__' is a special Python variable containing the path of the current Python script.

              ● <os.path.dirname(__file__)>
                dirname() extracts the directory containing the Python file.

              ● ".."
                 go up one directory

                e.g.
                  start from: /home/user/student-robotics-training-WK3/scripts
                  
                  go up one level:
                  /home/user/student-robotics-training-WK3

              ● "models", "simple_arm.xml"
                 Enter the models directory

                 Now we have: /home/user/student-robotics-training-WK3/models

                 finally, specifies the actual MuJoCo XML model file:
                  /home/user/student-robotics-training-WK3/models/simple_arm.xml

              ● os.path.join(...)
                construct a path from given pieces:
                
                e.g. /home/user/student-robotics-training-WK3/scripts/../models/simple_arm.xml

                    Notice that this path contains: scripts/../
                which means "go into scripts, then immediately go back out."

              ● os.path.normpath(...)
                
                normpath(...) cleans up a given path

                It removes unnecessary things.
                In this example, it removes scripts/../

                So the final result is: /home/user/student-robotics-training-WK3/models/simple_arm.xml

## scripts/control_simple_arm.py
   
       -- line 57, line 73

           '''
              qpos_addr = model.jnt_qposadr[model.joint(joint_name).id]
              isolation_qpos_addr = model.jnt_qposadr[model.joint(ISOLATION_JOINT).id]
           '''
              ● model.joint(...)
                
                 looks joint up by name in the model; Returning a small "view" object with info about it.
                 This is the name-based lookup habit from before, applied to joints instead of actuators.

              ● model.jnt_qposadr(...)
                
                 Each joint corresponds an entry, so for each MjModel object, there exists an table: data.pos array.
                 This method looks up the table and search where the target joint's position value(index) actually lives.

         Note:
              If you want to drive the elbow instead, or both joints together, the only lines that need to change are TARGET_JOINT/TARGET_ACTUATOR at the top — everything else looks itself up by name.


      # Summary of the Motion
          
             The shoulder joint is controled by shoulder actuator. We set a series of safe targets within the safe range of the shoulder joint; The shoulder joint will sweep these targets in a sequence: low -> high -> low with no repeated endpoints. 

             Thus, the shoulder joint will rotate from original position and back to the original position.

             The elbow joint is not drived here. The control method is same as shoulder joint's control.

## tests/verify_simple_model.py
            
            '''
                def test_model_steps_without_exploding():
                    """Sanity check: the model is numerically stable, not just well-named."""
                    model = load_model()
                    data = mujoco.MjData(model)
                    for _ in range(50):
                        mujoco.mj_step(model, data)
                    assert all(abs(v) < 1e6 for v in data.qvel), (
                        "simulation velocities exploded -- check damping and gains"
                     )
            '''

            First: what data.qvel actually is. It's the velocity of every joint in the model — for simple_arm.xml, a 2-element array: [shoulder angular velocity, elbow angular velocity], in rad/s. A healthy simulation of a small arm swinging under gravity and mild actuator forces should have velocities somewhere in the single or low double digits — nothing close to a million.

            Now, breaking it on purpose — stripping the joint damping and blowing the timestep out to 250x what's in the XML (a classic way to induce genuine numerical instability):

            2159 rad/s is already absurd — this is a tiny arm with 0.3–0.55m links, there's no physical scenario where it should spin that fast. A real numerical blow-up (the kind caused by an actual bug — e.g. someone deleting the damping from your XML, or a bad integration step) typically doesn't stop at hundreds; it compounds exponentially step over step into the millions, or overflows into inf/nan outright. 1e6 sits comfortably above anything a healthy version of this model would ever produce, but well below where a genuine explosion lands — so it has essentially zero false-positive risk while still catching real instability.

            the comparison also catches NaN and inf for free, without any extra code. In Python (and NumPy), any comparison involving NaN returns False — including abs(nan) < 1e6. So if a joint velocity ever actually becomes NaN (which is what a truly catastrophic blow-up looks like), that element makes all(...) immediately False, and the test fails — even though the check never explicitly asks "is this NaN?"

            One honest caveat I found while testing this — worth knowing, not necessarily worth fixing right now: MuJoCo has its own internal instability watchdog. When I pushed the timestep hard enough to actually produce NaN/Inf internally, MuJoCo printed a warning ("WARNING: Nan, Inf or huge value in QACC...") to stderr and reset the state on its own, rather than letting the corrupted values sit in data.qvel for you to inspect. That means a transient explosion in the middle of a run could self-correct by the time your test checks data.qvel at the very end (our test only checks after all 50 steps finish, once). For this milestone's purposes that's fine — the test is a smoke check, not a rigorous stability proof — but if you ever wanted a stricter version, you'd check qvel (or watch for that stderr warning) after every step inside the loop, not just once at the end.

## Concepts to Explore
     
        •	MJCF kinematic tree
            
              MJCF organizes every body as a tree rooted at <worldbody>.

              In my model: models/simple_arm.xml, the MJCF kinematic tree is a simple chain:
              world → base → upper_arm → forearm

              each body is a child of the one before it.
              MCJF computes everything that actually sits in the world(<worldbody>) by traversing this tree from the top(root) to the bottoms(leaf nodes), composing each body's local transform onto its parent's. This is why test_worldbody_and_nested_bodies checks body_parentid — it's directly verifying the tree structure, not just that three bodies exist.

        •	Local coordinate frames
           
            Each body's pos/quat in the XML is written relative to its parent, not the world -- this is what "coordinate = local" in <compiler> declares.
            Concretely: forearm's pos = "0 0 0.3" means "0.3 m along upper_arm's own z-axis", not the world's z-axis. 
            Furthermore, that is what makes the chain move together -- rotate upper_arm, forearm's frame rotates with it automatically, since its position is defined in terms of the parent, not fixed in the workspace.

        •	Hinge axis and range 

           -- Hinge axis
              
              Hinge axis defines the 3D direction the hinge rotates around, expressed in joint's local frame here.

              E.g.
                   axis = "0 1 0" for both my joints

                   here the 3D direction is the local Y-axis, so both joints swing the arm in the same plane (an XZ-plane bend, like a real elbow).

           -- range

               'range' sets how far it is allowed to rotate. 'range' alone does nothing, unless limited = "true" is also set; without it, MuJoCo ignores the range entirely.

        •	Actuator control range

            Actuator control range bounds what rotate range is allowed for that actuator.
            It bounds what the data.ctrl[i] is allowed to mean for that actuator under the condition: actuator_ctrllimited = "true" 

        •	Position, velocity, and motor actuators

            Position: is the target position of the control unit. For my model, it is target angle;
                      the actuator generates force proportional to the error(kp gain), like a spring pulling toward the target; This is the cause of what produced the overshoot-then-settle behavior you saw in Task 11.

            Velocity: is a target angular velocity instead; the actuator corrects toward matching that speed, not a specific angle.


            Motor: control is applied directly as torque, with zero built-in correction. No spring pulling it back toward anything — if you get the number wrong, nothing self-corrects. This is why position actuators are the friendlier starting point: they're forgiving of an imprecise ctrl value in a way motors aren't.

        •	Gravity, damping, and numerical stability

            Gravity:
                  A physical concept: a force from the Earth that pulls every unit of mass downward.

                  E.g. <option gravity="0 0 -9.81"/>

            Damping: 
                    each damping is produced by a control unit and functions on corresponding controled object. Damping resists  velocity, dissipating energy so the system settles instead of oscillating forever.

            Numerical Stability:
                         
                         Real physics is continuous — position and velocity change smoothly, described by differential equations. A computer can't simulate "continuous"; it can only take discrete steps: compute forces, update velocity, update position, repeat — each step advancing time by dt (your timestep). This is called numerical integration, and it's always an approximation of the true continuous motion.

                         Numerical stability is the property that these small, repeated approximation errors stay small — instead of compounding step after step until they explode. A stable simulation tracks the true physics closely. An unstable one starts drifting from reality and, past a certain point, the errors feed on themselves and grow exponentially.

        •	Element names versus numeric indices

            Indices shift silently if the XML gets reordered; a wrong index still runs — it just quietly controls or inspects the wrong thing. A wrong name fails loudly with a KeyError telling you exactly what's missing, which is why verify_simple_model.py catches a typo'd joint name instantly instead of producing a confusing wrong result three scripts downstream.

            E.g.
               '''
                  model.joint("shoulder_joint")
               '''

               not

               '''
                  data.ctrl[0]
               '''

## Suggested AI Exploration
      
      •	Why should I use element names instead of assuming fixed joint indices?

        1. Fixed indices are under an assumption: you never write down anywhere.
              E.g. 
                  data.ctrl[0] silently means "shoulder_actuator" only for as long as nobody touches the XML's element order. Nothing in the code says that assumption exists — you'd only discover it broke by noticing the arm moving wrong, possibly much later, possibly after logging a bunch of bad data.

        2. It fails the worst possible way: silently

           A crash is annoying but honest — it tells you immediately something's wrong. An index pointing at the wrong element just runs and produces a plausible number

           E.g. 
               the elbow_joint moved to: 1.4e-05 above — nothing about that output screams "this is broken."

        3. Names fail loudly instead

           E.g. 
              when I typo'd shoulder_joint — a clear KeyError naming exactly what was expected and what's actually available. That's a bug you catch in the first test run, not three weeks later.

        Note: any time you write data.ctrl[0] or data.qpos[2] in a script that isn't immediately, locally derived from a model.actuator("name")/model.joint("name") lookup, treat it as a bug waiting for someone to reorder your XML.

      • Compare MuJoCo motor and position actuators for a beginner joint-control demo.

                            Motor (<motor>)                         Position (<position>)
        ______________________________________________________________________________________________
        What Ctrl            Raw torque                                  Target Angle
        means
        ______________________________________________________________________________________________

        Feedback loop        None -- you write it               Built-in (spring toward target via kp)
        ______________________________________________________________________________________________
        Coded needed to       Compute error each step,             data.ctrl[i] = target, done
        reach a target         in Python forever
        ______________________________________________________________________________________________
        Gain tuning              choose <kp> from scratch                 	One kp in the XML,
                                 no default                                 set once
        ______________________________________________________________________________________________
        "Set once, step in       Silently broken — constant torque,       Works exactly as expected
        a loop" pattern           no target reached
        ______________________________________________________________________________________________
        Failure mode             Wrong number that looks plausible             Overshoot/oscillation  
        for beginner             (settles somewhere, just not where you meant)  if kp is badly tuned, but at
                                                                                least converges toward the right place
        ______________________________________________________________________________________________
        What it's                 Direct force/torque control — RL action speces  A quick, forgiving way to say "go 
                                                                                  here" without writing a controler               
        actually good for         simulating a real motor's torque limits, 
                                  custom controllers

        _______________________________________________________________________________________


      • Why might a simulated joint oscillate or become unstable?
        
         Oscillation: bounded, not settle

         Unstable: unbounded, not settle

         • Not enough dampling → oscillation that never settles

           Damping is what removes energy from the system each step; without it, a spring-like actuator (or gravity) just keeps trading energy back and forth forever.

        • Gain too high relative to damping
          
           A gain that's fine at one timestep becomes unstable at the same timestep if pushed too high, and the same gain that's unstable now would be fine again at a smaller timestep — gain, damping, and timestep aren't three independent knobs, they're one tightly coupled system.

           E.g.
              "why does dt matter" cliff we found earlier: a stiffer spring (higher kp) needs proportionally smaller dt

        • A sign error in your own feedback code — a bug, not a physics problem

           E.g.
              Genuinely unbounded — qpos sails straight through where the joint limit would have stopped it (I removed the limit specifically to show this), never turning back. This is one line reversed — data.qpos[0] - target instead of target - data.qpos[0] — and it silently converts a stabilizing correction into a destabilizing one: the "correction" now always pushes further from the target, so every step's error is worse than the last. That's positive feedback, the same runaway mechanism as the timestep/gain cases, just caused by a logic bug instead of a numerical one.

## Stretch Goals

     •	Compare open-loop control with a basic proportional controller
        
        - Open-loop Control
                             An open-loop system applies a predetermined control input $u(t)$ based solely on the desired reference (setpoint) $r(t)$ and an assumed model of the plant. It has no sensor feedback to verify the output $y(t)$.
                                 
                                 $$u(t) = f(r(t))$$
         E.g. 
               Setting a microwave timer for 2 minutes. The oven runs regardless of whether the food is frozen, lukewarm, or burning.

        - Proportional Controller

           A proportional controller is the simplest form of closed-loop feedback control. It computes an error signal $e(t)$ between the reference setpoint $r(t)$ and the measured system output $y(t)$, scaling the control action by a constant proportional gain $K_p$:
                                              $$e(t) = r(t) - y(t)$$
                                              $$u(t) = K_p * e(t)$$

           E.g.
                    Driving a car and steering to stay centered in a lane. If you drift slightly to the right, you apply a gentle left correction; if you drift far to the right, you steer harder.

      Key differences:
         Dimension                     Open-Loop Control                            Proportional (P) 
        ControlFeedback               LoopNone (acts blind)                   Continuous negative feedback

      Disturbance Handling   Cannot detect or compensate for external    [Automatically counteracts disturbances once they affect $y(t)$]

      Model Sensitivity      Extremely sensitive to parameter drift,      Robust against moderate plant parameter uncertainties
                              aging, or calibration errors 

      Steady-State Error(Ess)     Zero only under perfect                 Inherently exhibits a non-zero steady-state offset for   
                               calibration and zero disturbance           standard type-0 systems without an integral (I) term

      Stability Risk           Inherently stable if the open-loop plant   High $K_p$ values can cause oscillations, overshoot, or 
                                itself is stable                           instability in higher-order systems

      Complexity & Cost       Low (no sensors or feedback circuitry required)         Requires sensors, signal conditioning, and 
                                                                                        feedback computation