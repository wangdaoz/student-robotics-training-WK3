#!/usr/bin/env bash
# run_all.sh - Week 3 clean-clone verification runner
# Run this from the repo root, right after a fresh git clone.

set -uo pipefail   # NOT -e: one failure shouldn't kill the rest of the run

LOGDIR="evidence/logs"
mkdir -p "$LOGDIR"

PASS=0
FAIL=0
FAILED_ITEMS=()

run_and_log() {
    local name="$1"
    shift
    echo "=== $name ==="
    "$@" > "$LOGDIR/${name}.log" 2>&1
    local status=$?
    if [ $status -eq 0 ]; then
        echo "  PASS (exit $status)"
        PASS=$((PASS + 1))
    else
        echo "  FAIL (exit $status) -- see $LOGDIR/${name}.log"
        FAIL=$((FAIL + 1))
        FAILED_ITEMS+=("$name")
    fi
}

echo "########## 1. Environment setup ##########"
unset PYTHONPATH
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt --quiet
pip install pytest

 
echo ""
echo "########## 2. Tests (tests/) ##########"
run_and_log "test_simple_model"    python tests/verify_simple_model.py
run_and_log "test_berkeley_model"  python -m pytest tests/verify_berkeley_model.py -v
run_and_log "test_simple_model_actuator_joint" python tests/verify_simple_model_actuator_joint.py
run_and_log "test_mujoco_env" python tests/test_mujoco_env.py
run_and_log "test_stretch_Goal3" python tests/Stretch_Goal3_verify_simple_model.py
 
echo ""
echo "########## 3. Scripts (scripts/) ##########"
run_and_log "mujoco_smoke_test"       python scripts/mujoco_smoke_test.py
run_and_log "inspect_model"           python scripts/inspect_model.py
run_and_log "control_simple_arm"      python scripts/control_simple_arm.py 
run_and_log "record_tip_trajectory"   python scripts/record_tip_trajectory.py
run_and_log "mile3.2_stretch_goal1_rand_video" python scripts/rand_video.py
run_and_log "mile3.2_stretch_goal2_model_states" python scripts/stretchgoal2_model_stats.py
run_and_log "inspect_berkeley_model"  python scripts/inspect_berkeley_model.py
run_and_log "control_berkeley_joint"  python scripts/control_berkeley_joint.py --ctrl 0.1 --duration 2.0
run_and_log "control_berkeley_joint_viewer" python scripts/control_berkeley_joint.py --ctrl 1.0 --duration 2.0 --record
run_and_log "load_simple_arm" python scripts/load_simple_arm.py --headless 
run_and_log "generate_berkeley_model_report" python scripts/generate_berkeley_model_report.py
run_and_log "mile3.5stretch_goal1_Control_2_joints" python scripts/mile3.5stretch_goal1_Control_2_joints.py --ctrl 1.0 --duration 2.0
run_and_log "mile3.5_stretch_3_contr_berekeley_joint" python scripts/mile3.5_stretch_3_contr_berekeley_joint.py --target-joint "arm_left_shoulder_pitch_joint" --ctrl 1.0 --duration 2.0
 
echo ""
echo "===== SUMMARY ====="
echo "Passed: $PASS"
echo "Failed: $FAIL"
if [ "$FAIL" -gt 0 ]; then
    echo "Failed items:"
    for item in "${FAILED_ITEMS[@]}"; do
        echo "  - $item"
    done
    exit 1
fi
 
echo "All checks passed."
exit 0