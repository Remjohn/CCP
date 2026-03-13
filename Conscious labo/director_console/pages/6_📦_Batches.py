# Page 6: Batch Management - V2 with naming convention

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, date

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import CMF_ROOT
from db.connection import get_session, init_db
from db.models import Project, Batch, BatchProject, StageApproval, Coach
from utils.naming import (
    get_current_month,
    get_next_video_number,
    generate_project_code,
    create_project_folder,
)

st.set_page_config(page_title="Batch Management", page_icon="📦", layout="wide")

# Reinitialize DB for new models
init_db()

st.title("📦 Batch Management V2")
st.markdown("Create and manage batch execution runs with standardized naming.")

st.divider()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["➕ New Project", "🚀 Create Batch", "📋 Active", "✅ Completed"])

with tab1:
    st.subheader("➕ Add New Project")
    st.markdown("Create a project with standardized naming: `CVN-TVN-MM-CoachName`")
    
    with get_session() as session:
        coaches = session.query(Coach).order_by(Coach.name).all()
        
        if not coaches:
            st.warning("No coaches found. Add a coach first in the Coaches page.")
            if st.button("👤 Go to Coaches"):
                st.switch_page("pages/8_👤_Coaches.py")
        else:
            with st.form("new_project_form"):
                # Coach selection
                coach_options = {c.name: c.id for c in coaches}
                selected_coach = st.selectbox("Coach", list(coach_options.keys()))
                
                # Auto-calculate naming
                current_month = get_current_month()
                total_videos = 220
                
                # Get next video number
                with get_session() as s:
                    next_num = get_next_video_number(s, current_month, total_videos)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    video_number = st.number_input("Video # (CVN)", value=next_num, min_value=1, max_value=total_videos)
                with col2:
                    st.metric("Total (TVN)", total_videos)
                with col3:
                    month = st.number_input("Month (MM)", value=current_month, min_value=1, max_value=12)
                
                # Preview the code
                preview_code = generate_project_code(video_number, total_videos, month, selected_coach)
                st.info(f"📛 Project Code: **{preview_code}**")
                
                # Scheduling
                st.markdown("**📅 Schedule:**")
                scheduled_day = st.date_input("Production Day", value=date.today())
                
                # Optional name
                project_name = st.text_input("Project Name (optional)", placeholder="e.g., Matthis Interview")
                
                submitted = st.form_submit_button("➕ Create Project", type="primary")
                
                if submitted:
                    coach_id = coach_options[selected_coach]
                    full_code = generate_project_code(video_number, total_videos, month, selected_coach)
                    
                    with get_session() as s:
                        # Get coach details
                        coach = s.query(Coach).filter(Coach.id == coach_id).first()
                        
                        # Create folder
                        inputs_dir = Path(coach.assets_folder) if coach.assets_folder else CMF_ROOT / "inputs"
                        folder = create_project_folder(inputs_dir, selected_coach, full_code)
                        
                        # Create project
                        project = Project(
                            project_id=full_code,
                            name=project_name or full_code,
                            video_number=video_number,
                            month=month,
                            total_videos=total_videos,
                            full_code=full_code,
                            scheduled_day=scheduled_day,
                            coach_id=coach_id,
                            folder_path=str(folder),
                            current_stage="pending"
                        )
                        s.add(project)
                        s.flush()
                        
                        # Create stage approvals
                        for stage in ["scripts", "assets", "composition", "audio"]:
                            approval = StageApproval(
                                project_id=project.id,
                                stage=stage,
                                status="pending"
                            )
                            s.add(approval)
                    
                    st.success(f"✅ Created project: **{full_code}**")
                    st.markdown(f"Folder: `{folder}`")
                    st.info("💡 Add TRANSCRIPT.md to the folder, then create a batch to start processing.")

with tab2:
    st.subheader("🚀 Create Batch from Projects")
    
    with get_session() as session:
        # Get pending projects
        pending_projects = session.query(Project).filter(
            Project.current_stage == "pending"
        ).order_by(Project.scheduled_day, Project.video_number).all()
        
        if not pending_projects:
            st.info("No pending projects. Create projects first.")
        else:
            st.markdown(f"**{len(pending_projects)} projects ready for batch:**")
            
            selected_ids = []
            for proj in pending_projects:
                coach = session.query(Coach).filter(Coach.id == proj.coach_id).first()
                coach_name = coach.name if coach else "Unknown"
                
                if st.checkbox(
                    f"📄 {proj.full_code or proj.project_id} ({coach_name}) - Day: {proj.scheduled_day}",
                    key=f"sel_{proj.id}",
                    value=True
                ):
                    selected_ids.append(proj.id)
            
            if st.button("🚀 Create Batch", type="primary"):
                batch_id = f"BATCH_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}"
                
                with get_session() as s:
                    batch = Batch(
                        batch_id=batch_id,
                        status="pending",
                        total_projects=len(selected_ids)
                    )
                    s.add(batch)
                    s.flush()
                    
                    for i, proj_id in enumerate(selected_ids):
                        bp = BatchProject(
                            batch_id=batch.id,
                            project_id=proj_id,
                            order_index=i
                        )
                        s.add(bp)
                        
                        # Update project stage
                        proj = s.query(Project).filter(Project.id == proj_id).first()
                        if proj:
                            proj.current_stage = "scripts"
                
                st.success(f"✅ Created batch: **{batch_id}** with {len(selected_ids)} projects!")
                st.markdown("Go to **📝 Scripts** to start the approval process.")

with tab3:
    st.subheader("📋 Active Batches")
    
    with get_session() as session:
        active_batches = session.query(Batch).filter(
            Batch.status.in_(["pending", "running", "paused"])
        ).order_by(Batch.created_at.desc()).all()
        
        if not active_batches:
            st.info("No active batches.")
        else:
            for batch in active_batches:
                batch_projects = session.query(BatchProject).filter(
                    BatchProject.batch_id == batch.id
                ).all()
                
                completed = sum(
                    1 for bp in batch_projects
                    if session.query(Project).filter(
                        Project.id == bp.project_id,
                        Project.current_stage == "completed"
                    ).first()
                )
                
                with st.expander(f"📦 {batch.batch_id} ({completed}/{len(batch_projects)})", expanded=True):
                    st.progress(completed / max(len(batch_projects), 1))
                    
                    for bp in batch_projects:
                        proj = session.query(Project).filter(Project.id == bp.project_id).first()
                        if proj:
                            icon = "✅" if proj.current_stage == "completed" else "⏳"
                            st.markdown(f"{icon} {proj.full_code or proj.project_id}: `{proj.current_stage}`")

with tab4:
    st.subheader("✅ Completed Batches")
    
    with get_session() as session:
        completed = session.query(Batch).filter(
            Batch.status == "completed"
        ).order_by(Batch.completed_at.desc()).limit(10).all()
        
        if not completed:
            st.info("No completed batches yet.")
        else:
            for batch in completed:
                st.markdown(f"✅ **{batch.batch_id}** - {batch.total_projects} videos")
