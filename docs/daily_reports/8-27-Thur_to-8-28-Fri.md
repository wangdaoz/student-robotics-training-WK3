### Milestone
    Milestone 3.5 Load and Control Berkeley Humanoid Lite in MuJoCo

### Current objective

    Suggested AI Exploration and Scretch Goals

### Work Completed

      Suggested AI Exploration, Scretch Goals

### Commands or tests run

      AI Exploration:
              '''
                 unset PYTHONPATH
                 source .venv/bin/activate
                 python scripts/generate_berkeley_model_report.py
              '''
       
      
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
### Blockers

     In last AI exploration: Help me design a model-inspection report using names rather than hard-coded indices. I didn't know how to write such a script.


### How I investigated

     I asked Claude Code to help me. Then, I read its codes and thought about it. Finally, I wrote my script.

### AI tools used

      I asked Claude Code to help me finish all tasks in this section.
      I asked ChatGPT to answer codes or commands that I hadn't understood,

### What I Learned

     From stretch goal 3, I learned that args is a plain object, and you access its fields with normal Python attribute syntax: args.something. But - is not a legal character inside a Python identifier — args.target-joint isn't "the attribute named target-joint," it's parsed by Python itself as subtraction: args.target minus a variable called joint. That's precisely bug #2 from before — Python happily accepted it as valid syntax, just not the syntax you intended.

     From stretch goal 4, I learned some main differences by analyzing two different formats for a same model/asset.

### Next action

     Weekend Engineering Wrap-up.