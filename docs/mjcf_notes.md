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