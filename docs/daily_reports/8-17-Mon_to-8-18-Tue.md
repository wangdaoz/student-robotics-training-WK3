### Milestone

     3.3 Build and Control a Simple Articulated Model

### Current objective
     
     Understand and explain the concepts in the section "Concepts to Explore"
     Explore questions given by the section "Suggested AI Exploration"

     Finish section: Scretch Goals
     
### Work Completed
     
      "Concepts to Explore"

      "Suggested AI Exploration"

      "Scretch Goals"

### Commands or tests run

      Scratch Goal #3:
                      '''
                          unset PYTHONPATH
                          source .venv/bin/activate
                          python scripts/record_tip_trajectory.py
                          python teste/verify_simple_model_actuator_joint.py
                      '''

### Blockers
     
         When I was doing scretch goal #13, I didn't know what files should be created and how to write programs.

### How I investigated

     I asked Claude Code for help. It told me the total idea with plenty of details. I read codes in files shown to me, modified corresponding file and created and edited necessary new files.

     Then, I read and understood each segment of codes in these files; Finally, I compare the test file with other test files from previous tasks.

### AI tools used

    Claude code, Google Gemini

### What I Learned
    
    the functions and correlations of gain, damping, timestep in the process of running a model.

     How to created, modify a model via MCJF; How to write simulation programs for actions of the model; How to write test files to check different models.

### Next action
    Milestone 3.4 Map the Official Berkeley Humanoid Lite Assets