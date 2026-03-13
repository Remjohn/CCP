# CMF Director's Console V2 - Main App
# Streamlit-based director interface for managing CMF production

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from db.connection import init_db, get_session
from db.models import Project, Batch, StageApproval
from config import VIDEO_VALUE, MONTHLY_GOAL, WEEKLY_GOAL, CURRENCY, INPUTS_DIR
from datetime import datetime, timedelta
import calendar

# Page configuration
st.set_page_config(
    page_title="CMF Director's Console",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

# AUTO-SYNC on startup (runs once per session)
if "sync_done" not in st.session_state:
    try:
        from utils.file_sync import full_sync
        with get_session() as session:
            stats = full_sync(session, INPUTS_DIR)
            st.session_state.sync_done = True
            st.session_state.sync_stats = stats
    except Exception as e:
        st.session_state.sync_done = True
        st.session_state.sync_stats = {"error": str(e)}

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF4B4B;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR - PROGRESS TRACKER (Always visible)
# ============================================================
with st.sidebar:
    st.markdown("### 💰 Progress Tracker")
    
    with get_session() as session:
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        week_start = now - timedelta(days=now.weekday())
        
        total_completed = session.query(Project).filter(
            Project.current_stage == "completed"
        ).count()
        
        month_completed = session.query(Project).filter(
            Project.current_stage == "completed",
            Project.month == current_month
        ).count()
        
        week_completed = session.query(Project).filter(
            Project.current_stage == "completed",
            Project.updated_at >= week_start
        ).count()
    
    # Monthly Progress
    month_progress = month_completed / MONTHLY_GOAL
    month_earnings = month_completed * VIDEO_VALUE
    
    st.markdown(f"**📅 {now.strftime('%B')} Goal**")
    st.progress(min(month_progress, 1.0))
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{month_completed}/{MONTHLY_GOAL}**")
    with col2:
        st.markdown(f"💵 **{CURRENCY}{month_earnings:,}**")
    
    # Weekly Progress
    week_progress = week_completed / WEEKLY_GOAL
    week_earnings = week_completed * VIDEO_VALUE
    
    st.markdown(f"**📆 Week Goal**")
    st.progress(min(week_progress, 1.0))
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{week_completed}/{WEEKLY_GOAL}**")
    with col2:
        st.markdown(f"💵 **{CURRENCY}{week_earnings:,}**")
    
    # Total
    total_earnings = total_completed * VIDEO_VALUE
    st.markdown("---")
    st.markdown(f"**🏆 Total:** {total_completed} videos = **{CURRENCY}{total_earnings:,}**")
    
    # SYNC BUTTON
    st.markdown("---")
    st.markdown("### 🔄 File Sync")
    if st.button("🔄 Sync Files → DB", use_container_width=True):
        try:
            from utils.file_sync import full_sync
            with get_session() as session:
                stats = full_sync(session, INPUTS_DIR)
                st.session_state.sync_stats = stats
            st.success(f"✅ {stats.get('imported', 0)} imported, {stats.get('updated', 0)} updated")
            st.rerun()
        except Exception as e:
            st.error(f"Sync error: {e}")
    
    # Show last sync stats if available
    if "sync_stats" in st.session_state:
        stats = st.session_state.sync_stats
        if "error" in stats:
            st.caption(f"⚠️ {stats['error']}")
        else:
            st.caption(f"Last: +{stats.get('imported', 0)} new, ↻{stats.get('updated', 0)} updated")
    
    # Pace indicator
    days_in_month = calendar.monthrange(current_year, current_month)[1]
    days_left = days_in_month - now.day
    videos_needed = MONTHLY_GOAL - month_completed
    
    if videos_needed > 0 and days_left > 0:
        daily_rate = videos_needed / days_left
        if daily_rate <= 7:
            st.success(f"✅ On track ({daily_rate:.1f}/day needed)")
        elif daily_rate <= 10:
            st.warning(f"⚠️ Need {daily_rate:.1f}/day")
        else:
            st.error(f"🔥 Need {daily_rate:.1f}/day!")
    elif videos_needed <= 0:
        st.success("🎉 Goal achieved!")

st.markdown("---")

# ============================================================
# MAIN DASHBOARD
# ============================================================
st.title("🎬 CMF Director's Console")
st.markdown("**Welcome to the Conscious Movie Factory Production Hub**")

st.divider()

# Quick Stats
col1, col2, col3, col4 = st.columns(4)

with get_session() as session:
    total_projects = session.query(Project).count()
    
    pending_approvals = session.query(StageApproval).filter(
        StageApproval.status == "pending"
    ).count()
    
    active_batches = session.query(Batch).filter(
        Batch.status.in_(["pending", "running"])
    ).count()
    
    completed_projects = session.query(Project).filter(
        Project.current_stage == "completed"
    ).count()

with col1:
    st.metric("📁 Total Projects", total_projects)
with col2:
    st.metric("⏳ Pending Approvals", pending_approvals)
with col3:
    st.metric("🚀 Active Batches", active_batches)
with col4:
    st.metric("✅ Completed", completed_projects)

st.divider()

# Stage Progress Overview
st.subheader("📊 Pipeline Stage Overview")

with get_session() as session:
    stages = ["pending", "scripts", "assets", "composition", "audio", "completed"]
    stage_counts = {}
    
    for stage in stages:
        count = session.query(Project).filter(Project.current_stage == stage).count()
        stage_counts[stage] = count

# Visual progress
stage_cols = st.columns(len(stages))
stage_icons = ["⏸️", "📝", "🎨", "🎬", "🔊", "✅"]

for i, stage in enumerate(stages):
    with stage_cols[i]:
        st.metric(
            f"{stage_icons[i]} {stage.title()}", 
            stage_counts[stage]
        )

st.divider()

# Quick Actions
st.subheader("⚡ Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("➕ New Project", type="primary", use_container_width=True):
        st.switch_page("pages/6_📦_Batches.py")

with col2:
    if st.button("👤 Add Coach", use_container_width=True):
        st.switch_page("pages/8_👤_Coaches.py")

with col3:
    if st.button("📝 Review Scripts", use_container_width=True):
        st.switch_page("pages/2_📝_Scripts.py")

with col4:
    if st.button("📅 Calendar", use_container_width=True):
        st.switch_page("pages/9_📅_Calendar.py")

st.divider()

# Recent Activity
st.subheader("📜 Recent Activity")

with get_session() as session:
    recent = session.query(Project).order_by(
        Project.updated_at.desc()
    ).limit(5).all()
    
    if recent:
        for proj in recent:
            icon = "✅" if proj.current_stage == "completed" else "⏳"
            st.markdown(f"{icon} **{proj.full_code or proj.project_id}** - {proj.current_stage}")
    else:
        st.info("No projects yet. Create one to get started!")

# Footer
st.divider()
st.caption(f"CMF Director's Console V2 | Video Value: {CURRENCY}{VIDEO_VALUE} | Goal: {MONTHLY_GOAL}/month")
