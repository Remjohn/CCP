# Page 7: Settings - V2 with Gamification

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import CMF_ROOT, DATABASE_URL, VIDEO_VALUE, MONTHLY_GOAL, WEEKLY_GOAL, CURRENCY
from db.connection import get_session
from db.models import Project

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

# ============================================================
# SIDEBAR - PROGRESS TRACKER
# ============================================================
with st.sidebar:
    st.markdown("### 💰 Progress Tracker")
    
    with get_session() as session:
        now = datetime.now()
        current_month = now.month
        week_start = now - timedelta(days=now.weekday())
        
        total_completed = session.query(Project).filter(Project.current_stage == "completed").count()
        month_completed = session.query(Project).filter(Project.current_stage == "completed", Project.month == current_month).count()
        week_completed = session.query(Project).filter(Project.current_stage == "completed", Project.updated_at >= week_start).count()
    
    st.markdown(f"**📅 {now.strftime('%B')}**")
    st.progress(min(month_completed / MONTHLY_GOAL, 1.0))
    st.markdown(f"**{month_completed}/{MONTHLY_GOAL}** = {CURRENCY}{month_completed * VIDEO_VALUE:,}")
    
    st.markdown(f"**📆 Week**")
    st.progress(min(week_completed / WEEKLY_GOAL, 1.0))
    st.markdown(f"**{week_completed}/{WEEKLY_GOAL}** = {CURRENCY}{week_completed * VIDEO_VALUE:,}")
    
    st.markdown("---")
    st.markdown(f"**🏆 Total:** {total_completed} = {CURRENCY}{total_completed * VIDEO_VALUE:,}")

# ============================================================
# MAIN CONTENT
# ============================================================
st.title("⚙️ Settings")

st.divider()

# Gamification Settings
st.subheader("💰 Gamification Settings")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Video Value", f"{CURRENCY}{VIDEO_VALUE}")
with col2:
    st.metric("Monthly Goal", f"{MONTHLY_GOAL} videos")
with col3:
    st.metric("Weekly Goal", f"{WEEKLY_GOAL} videos")

monthly_potential = MONTHLY_GOAL * VIDEO_VALUE
st.info(f"💡 **Monthly Potential:** {CURRENCY}{monthly_potential:,} | Edit `config.py` to change values.")

st.divider()

# Paths
st.subheader("📂 Paths")

st.markdown(f"**CMF Root:** `{CMF_ROOT}`")
st.markdown(f"**Database:** `{DATABASE_URL}`")

st.divider()

# Database Management
st.subheader("🗄️ Database")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Reset Database", type="secondary"):
        st.warning("This will delete all data!")
        if st.button("⚠️ Confirm Reset"):
            from db.connection import get_engine
            from db.models import Base
            
            Base.metadata.drop_all(bind=get_engine())
            Base.metadata.create_all(bind=get_engine())
            st.success("Database reset!")
            st.rerun()

with col2:
    if st.button("📊 Show Stats"):
        from db.models import Batch, StageApproval, Asset, Coach
        
        with get_session() as session:
            st.markdown(f"- **Projects:** {session.query(Project).count()}")
            st.markdown(f"- **Coaches:** {session.query(Coach).count()}")
            st.markdown(f"- **Batches:** {session.query(Batch).count()}")
            st.markdown(f"- **Approvals:** {session.query(StageApproval).count()}")
            st.markdown(f"- **Assets:** {session.query(Asset).count()}")

st.divider()

# Version Info
st.subheader("ℹ️ About")
st.markdown(f"""
**CMF Director's Console v2.0**

Part of the Conscious Movie Factory production system.
Built for {MONTHLY_GOAL} videos/month scale.

- 4-Stage Approval System
- Gamification ({CURRENCY}{VIDEO_VALUE}/video)
- Coach Management
- Calendar Scheduling
- SQLite Database (PostgreSQL ready)
""")
