### Milestone

    Milestone 3.4 Map the Official Berkeley Humanoid Lite Assets

### Current objective
      
    Inspect the official repositories and release assets. Produce a concise asset map that tells another engineer exactly what to download or clone, which version was inspected, where the MJCF entry model is located, and how included meshes or XML files are resolved.

### Work Completed
     
    task #19, task #20

### Commands or tests run

### Blockers

     In task #19, I didn't understand 'included XML files' 'working-directory assumptions'.

     In task #20, I didn't know how to use MuJoCo python API.

### How I investigated

    For task #19, I opened the official assets repository and accessed to relevant subdirectory/subfolder and browsed XML files. Next, I told Claude Code what I didn't know. It helped me to read these XML files and analyze these files.

    After reading its detailed analysis, new confusion existed. So, I continued asking new question. Then, I read its analysis, and check relevant subdirectory and files in repo. Finally, I figured all details in this task.

    For task #20, I asked Claude Code. After reading and understanding its given inspection file and explainations, I knew I cannot run such a executable in my local repo because in subdirectory 'mcjf' of repo, the subdirectory assets/erged/ is missing.

### AI tools used
    
     Claude Code

### What I Learned

    understand the relationships between XML files in same given directory;
    how to get information about the dependencies for any given XML file.

### Next action
   
   task #21 and remind concepts and AI explorations