# Page 4: Composition Approval with CLI Trigger

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))
from db.connection import get_session, init_db
from db.models import Project, StageApproval
from config import VIDEO_VALUE, MONTHLY_GOAL, WEEKLY_GOAL, CURRENCY
from utils.cli_executor import trigger_composition_stage, get_queue_status

st.set_page_config(page_title="Composition", page_icon="🎬", layout="wide")
init_db()

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### 💰 Progress Tracker")
    with get_session() as session:
        now = datetime.now()
        total_completed = session.query(Project).filter(Project.current_stage == "completed").count()
        month_completed = session.query(Project).filter(Project.current_stage == "completed", Project.month == now.month).count()
    
    st.progress(min(month_completed / MONTHLY_GOAL, 1.0))
    st.markdown(f"**{month_completed}/{MONTHLY_GOAL}** = {CURRENCY}{month_completed * VIDEO_VALUE:,}")
    
    st.divider()
    st.markdown("### 📋 Queue")
    queue = [q for q in get_queue_status() if q["phase"] == "composition"]
    st.caption(f"{len(queue)} composition commands queued")

# ============================================================
# MAIN
# ============================================================
st.title("🎬 Composition Approval")

# Get projects at composition stage
with get_session() as session:
    projects = session.query(Project).filter(Project.current_stage == "composition").all()
    project_data = [{"id": p.id, "code": p.full_code or p.project_id, "coach": p.coach.name if p.coach else "Unknown"} for p in projects]

if not project_data:
    st.info("No projects pending composition approval.")
else:
    st.subheader(f"Pending: {len(project_data)} projects")
    
    # Batch actions
    col1, col2, col3 = st.columns(3)
    with col1:
        cli_tool = st.selectbox("CLI Tool", ["claude", "gemini"], key="cli")
    with col2:
        if st.button("🚀 Trigger Composition Stage", type="primary"):
            command_id = trigger_composition_stage(project_data, cli_tool)
            st.success(f"Queued: {command_id}")
    with col3:
        if st.button("✅ Approve All"):
            with get_session() as session:
                for proj in project_data:
                    p = session.query(Project).get(proj["id"])
                    if p:
                        p.current_stage = "audio"
            st.success("All approved!")
            st.rerun()
    
    st.divider()
    
    # Individual projects
    for proj in project_data:
        with st.expander(f"🎬 {proj['code']}"):
            st.markdown("**Composed Video:**")
            st.caption("Video preview would appear here")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Approve", key=f"app_{proj['id']}"):
                    with get_session() as session:
                        p = session.query(Project).get(proj["id"])
                        if p:
                            p.current_stage = "audio"
                    st.rerun()
            with col2:
                if st.button("🔄 Re-compose", key=f"recomp_{proj['id']}"):
                    st.warning("Mark for re-composition")

# ============================================================
# SCENE CUTTER SECTION
# ============================================================
st.divider()
st.subheader("✂️ Scene Cutter (A-Roll)")

from utils.scene_cutter import cut_all_scenes, extract_scenes_from_script

col1, col2 = st.columns(2)
with col1:
    source_video = st.file_uploader("Upload Source Video", type=["mp4", "mov", "avi"])
with col2:
    script_file = st.file_uploader("Upload Script JSON (with timecodes)", type=["json"])

if source_video and script_file:
    import tempfile
    import json
    
    # Parse script
    script_data = json.load(script_file)
    scenes = script_data.get("scenes", [])
    
    st.markdown(f"**Found {len(scenes)} scenes in script**")
    
    # Preview scenes
    for scene in scenes[:5]:  # Show first 5
        st.caption(f"• {scene.get('id', 'UNKNOWN')}: {scene.get('start', '?')} → {scene.get('end', '?')}")
    
    if len(scenes) > 5:
        st.caption(f"... and {len(scenes) - 5} more")
    
    project_code = st.text_input("Project Code", value="PROJECT")
    output_dir = st.text_input("Output Directory", value=r"D:\Work\The Conscious Movie Factory December\🇫🇷 Conscious Movie Factory\inputs")
    
    if st.button("✂️ Cut All Scenes", type="primary"):
        # Save uploaded video to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(source_video.read())
            tmp_path = tmp.name
        
        with st.spinner("Cutting scenes with FFmpeg..."):
            results = cut_all_scenes(
                tmp_path,
                [{"scene_id": s.get("id", f"SC_{i+1:02d}"), "start": s.get("start", "0:00"), "end": s.get("end", "0:00")} for i, s in enumerate(scenes)],
                output_dir,
                project_code
            )
        
        st.success(f"✅ Cut {results['success']} scenes, {results['failed']} failed")
        for output in results.get("outputs", []):
            st.caption(f"📁 {output}")

