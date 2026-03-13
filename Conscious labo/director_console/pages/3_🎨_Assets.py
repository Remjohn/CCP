# Page 3: Assets Approval with CLI Trigger

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))
from db.connection import get_session, init_db
from db.models import Project, StageApproval
from config import VIDEO_VALUE, MONTHLY_GOAL, WEEKLY_GOAL, CURRENCY
from utils.cli_executor import trigger_assets_stage, get_queue_status

st.set_page_config(page_title="Assets", page_icon="🎨", layout="wide")
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
    queue = [q for q in get_queue_status() if q["phase"] == "assets"]
    st.caption(f"{len(queue)} assets commands queued")

# ============================================================
# MAIN
# ============================================================
st.title("🎨 Assets Approval")

# Get projects at assets stage
with get_session() as session:
    projects = session.query(Project).filter(Project.current_stage == "assets").all()
    project_data = [{"id": p.id, "code": p.full_code or p.project_id, "coach": p.coach.name if p.coach else "Unknown"} for p in projects]

if not project_data:
    st.info("No projects pending assets approval.")
else:
    st.subheader(f"Pending: {len(project_data)} projects")
    
    # Batch actions
    col1, col2, col3 = st.columns(3)
    with col1:
        cli_tool = st.selectbox("CLI Tool", ["claude", "gemini"], key="cli")
    with col2:
        if st.button("🚀 Trigger Assets Stage", type="primary"):
            command_id = trigger_assets_stage(project_data, cli_tool)
            st.success(f"Queued: {command_id}")
    with col3:
        if st.button("✅ Approve All"):
            with get_session() as session:
                for proj in project_data:
                    p = session.query(Project).get(proj["id"])
                    if p:
                        p.current_stage = "composition"
            st.success("All approved!")
            st.rerun()
    
    st.divider()
    
    # Individual projects
    for proj in project_data:
        with st.expander(f"🎨 {proj['code']}"):
            st.markdown("**Generated Assets:**")
            st.caption("Asset previews would appear here")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Approve", key=f"app_{proj['id']}"):
                    with get_session() as session:
                        p = session.query(Project).get(proj["id"])
                        if p:
                            p.current_stage = "composition"
                    st.rerun()
            with col2:
                if st.button("🔄 Regenerate", key=f"regen_{proj['id']}"):
                    st.warning("Mark for regeneration")
