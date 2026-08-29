# Berkeley Humanoid Lite — Model Inspection Report

Generated: 2026-08-28T00:04:18
Source model: `/home/kevin-lianhu/student-robotics-training-WK3/models/berkeley/Berkeley-Humanoid-Lite-Assets/data/robots/berkeley_humanoid/berkeley_humanoid_lite/mjcf/bhl_scene.xml`

## Model statistics

| Stat | Value |
|---|---|
| Generalized positions (nq) | 29 |
| Generalized velocities (nv) | 28 |
| Actuators (nu) | 22 |
| Bodies (nbody) | 27 |
| Joints (njnt) | 23 |
| Timestep (s) | 0.002 |

## Joints

| Joint Name | Type | qpos addr | dof addr | Range (rad) | Driven by |
|---|---|---|---|---|---|
| base_freejoint | 0 | 0 (7 slots) | 0 (6 slots) | N/A (free joint) | None |
| arm_left_shoulder_pitch_joint | 3 | 7 (1 slots) | 6 (1 slots) | -1.571,  0.785 | arm_left_shoulder_pitch_joint |
| arm_left_shoulder_roll_joint | 3 | 8 (1 slots) | 7 (1 slots) | -0.262,  1.309 | arm_left_shoulder_roll_joint |
| arm_left_shoulder_yaw_joint | 3 | 9 (1 slots) | 8 (1 slots) | -0.785,  0.785 | arm_left_shoulder_yaw_joint |
| arm_left_elbow_pitch_joint | 3 | 10 (1 slots) | 9 (1 slots) | -0.000,  1.571 | arm_left_elbow_pitch_joint |
| arm_left_elbow_roll_joint | 3 | 11 (1 slots) | 10 (1 slots) | -0.785,  0.785 | arm_left_elbow_roll_joint |
| arm_right_shoulder_pitch_joint | 3 | 12 (1 slots) | 11 (1 slots) | -0.785,  1.571 | arm_right_shoulder_pitch_joint |
| arm_right_shoulder_roll_joint | 3 | 13 (1 slots) | 12 (1 slots) | -1.309,  0.262 | arm_right_shoulder_roll_joint |
| arm_right_shoulder_yaw_joint | 3 | 14 (1 slots) | 13 (1 slots) | -0.785,  0.785 | arm_right_shoulder_yaw_joint |
| arm_right_elbow_pitch_joint | 3 | 15 (1 slots) | 14 (1 slots) | -1.571, -0.000 | arm_right_elbow_pitch_joint |
| arm_right_elbow_roll_joint | 3 | 16 (1 slots) | 15 (1 slots) | -0.785,  0.785 | arm_right_elbow_roll_joint |
| leg_left_hip_roll_joint | 3 | 17 (1 slots) | 16 (1 slots) | -0.175,  1.571 | leg_left_hip_roll_joint |
| leg_left_hip_yaw_joint | 3 | 18 (1 slots) | 17 (1 slots) | -0.982,  0.589 | leg_left_hip_yaw_joint |
| leg_left_hip_pitch_joint | 3 | 19 (1 slots) | 18 (1 slots) | -1.898,  0.982 | leg_left_hip_pitch_joint |
| leg_left_knee_pitch_joint | 3 | 20 (1 slots) | 19 (1 slots) | -0.000,  2.443 | leg_left_knee_pitch_joint |
| leg_left_ankle_pitch_joint | 3 | 21 (1 slots) | 20 (1 slots) | -0.785,  0.785 | leg_left_ankle_pitch_joint |
| leg_left_ankle_roll_joint | 3 | 22 (1 slots) | 21 (1 slots) | -0.262,  0.262 | leg_left_ankle_roll_joint |
| leg_right_hip_roll_joint | 3 | 23 (1 slots) | 22 (1 slots) | -1.571,  0.175 | leg_right_hip_roll_joint |
| leg_right_hip_yaw_joint | 3 | 24 (1 slots) | 23 (1 slots) | -0.589,  0.982 | leg_right_hip_yaw_joint |
| leg_right_hip_pitch_joint | 3 | 25 (1 slots) | 24 (1 slots) | -1.898,  0.982 | leg_right_hip_pitch_joint |
| leg_right_knee_pitch_joint | 3 | 26 (1 slots) | 25 (1 slots) | -0.000,  2.443 | leg_right_knee_pitch_joint |
| leg_right_ankle_pitch_joint | 3 | 27 (1 slots) | 26 (1 slots) | -0.785,  0.785 | leg_right_ankle_pitch_joint |
| leg_right_ankle_roll_joint | 3 | 28 (1 slots) | 27 (1 slots) | -0.262,  0.262 | leg_right_ankle_roll_joint |

## Actuators

| Actuator name | Drives joint | Force range (N*m) | Ctrl range |
|---|---|---|---|
| arm_left_shoulder_pitch_joint | arm_left_shoulder_pitch_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| arm_left_shoulder_roll_joint | arm_left_shoulder_roll_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| arm_left_shoulder_yaw_joint | arm_left_shoulder_yaw_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| arm_left_elbow_pitch_joint | arm_left_elbow_pitch_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| arm_left_elbow_roll_joint | arm_left_elbow_roll_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| arm_right_shoulder_pitch_joint | arm_right_shoulder_pitch_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| arm_right_shoulder_roll_joint | arm_right_shoulder_roll_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| arm_right_shoulder_yaw_joint | arm_right_shoulder_yaw_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| arm_right_elbow_pitch_joint | arm_right_elbow_pitch_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| arm_right_elbow_roll_joint | arm_right_elbow_roll_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| leg_left_hip_roll_joint | leg_left_hip_roll_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| leg_left_hip_yaw_joint | leg_left_hip_yaw_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| leg_left_hip_pitch_joint | leg_left_hip_pitch_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| leg_left_knee_pitch_joint | leg_left_knee_pitch_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| leg_left_ankle_pitch_joint | leg_left_ankle_pitch_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| leg_left_ankle_roll_joint | leg_left_ankle_roll_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| leg_right_hip_roll_joint | leg_right_hip_roll_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| leg_right_hip_yaw_joint | leg_right_hip_yaw_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| leg_right_hip_pitch_joint | leg_right_hip_pitch_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| leg_right_knee_pitch_joint | leg_right_knee_pitch_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| leg_right_ankle_pitch_joint | leg_right_ankle_pitch_joint | -20.0,  20.0 | unbounded (clipped by force range) |
| leg_right_ankle_roll_joint | leg_right_ankle_roll_joint | -20.0,  20.0 | unbounded (clipped by force range) |
