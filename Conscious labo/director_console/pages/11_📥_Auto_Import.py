# Page: Auto Import - Discover and import existing projects
# Scans input folders and imports projects into database

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from db.connection import get_session, init_db
from db.models import Project, Coach
from config import INPUTS_DIR
from utils.auto_import import scan_coach_folders, import_project_to_db

st.set_page_config(page_title="Auto Import", page_icon="📥", layout="wide")
init_db()

st.title("📥 Auto Import Projects")
st.markdown("Scan existing project folders and import them into the database.")

st.divider()

# Scan button
col1, col2 = st.columns([2, 1])

with col1:
    scan_path = st.text_input(
        "Scan Directory",
        value=str(INPUTS_DIR),
        help="Path to scan for project folders"
    )

with col2:
    st.markdown("&nbsp;")  # Spacer
    scan_clicked = st.button("🔍 Scan for Projects", type="primary", use_container_width=True)

if scan_clicked or "discovered_projects" in st.session_state:
    if scan_clicked:
        # Perform scan
        scan_dir = Path(scan_path)
        if scan_dir.exists():
            discovered = scan_coach_folders(scan_dir)
            st.session_state.discovered_projects = discovered
            st.success(f"✅ Found {len(discovered)} projects!")
        else:
            st.error(f"Path not found: {scan_path}")
            st.session_state.discovered_projects = []
    
    discovered = st.session_state.get("discovered_projects", [])
    
    if discovered:
        st.divider()
        st.subheader("📋 Discovered Projects")
        
        # Group by coach
        by_coach = {}
        for proj in discovered:
            coach = proj["coach_name"]
            if coach not in by_coach:
                by_coach[coach] = []
            by_coach[coach].append(proj)
        
        # Check which are already imported
        with get_session() as session:
            existing_paths = {p.folder_path for p in session.query(Project).all()}
        
        # Display by coach
        selected_for_import = []
        
        for coach_name, projects in by_coach.items():
            with st.expander(f"👤 {coach_name} ({len(projects)} projects)", expanded=True):
                
                # Summary table
                for proj in projects:
                    is_imported = proj["folder_path"] in existing_paths
                    
                    col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 1, 1])
                    
                    with col1:
                        icon = "✅" if is_imported else "⬜"
                        st.markdown(f"{icon} **{proj['folder_name']}**")
                    
                    with col2:
                        stage_icons = {
                            "pending": "⏸️",
                            "scripts": "📝",
                            "assets": "🎨",
                            "composition": "🎬",
                            "audio": "🔊",
                            "completed": "✅"
                        }
                        stage_icon = stage_icons.get(proj["detected_stage"], "❓")
                        st.markdown(f"{stage_icon} {proj['detected_stage']}")
                    
                    with col3:
                        if proj["has_script"]:
                            st.markdown("📜 Script")
                        else:
                            st.markdown("—")
                    
                    with col4:
                        if proj["has_storyboard"]:
                            st.markdown("🎬 SB")
                        else:
                            st.markdown("—")
                    
                    with col5:
                        if not is_imported:
                            if st.checkbox("Import", key=f"sel_{proj['folder_path']}", value=True):
                                selected_for_import.append((coach_name, proj))
                        else:
                            st.markdown("✓ Done")
        
        st.divider()
        
        # Import button
        if selected_for_import:
            st.markdown(f"**Ready to import: {len(selected_for_import)} projects**")
            
            if st.button("📥 Import Selected Projects", type="primary"):
                imported_count = 0
                skipped_count = 0
                
                with get_session() as session:
                    # Get or create coaches
                    coach_map = {}
                    for coach_name in set(c for c, _ in selected_for_import):
                        coach = session.query(Coach).filter(Coach.name == coach_name).first()
                        if not coach:
                            # Create coach
                            coach = Coach(
                                name=coach_name,
                                assets_folder=str(INPUTS_DIR / coach_name)
                            )
                            session.add(coach)
                            session.flush()
                        coach_map[coach_name] = coach.id
                    
                    # Import projects
                    for coach_name, proj in selected_for_import:
                        coach_id = coach_map[coach_name]
                        success = import_project_to_db(session, proj, coach_id)
                        if success:
                            imported_count += 1
                        else:
                            skipped_count += 1
                
                st.success(f"✅ Imported {imported_count} projects!")
                if skipped_count > 0:
                    st.info(f"Skipped {skipped_count} (already exist)")
                
                # Clear cache to refresh
                del st.session_state.discovered_projects
                st.rerun()
        else:
            st.info("All discovered projects are already imported.")

else:
    st.info("Click 'Scan for Projects' to discover existing project folders.")

st.divider()

# Quick stats
st.subheader("📊 Database Status")

with get_session() as session:
    total_projects = session.query(Project).count()
    total_coaches = session.query(Coach).count()
    
    stages = ["pending", "scripts", "assets", "composition", "audio", "completed"]
    stage_counts = {
        stage: session.query(Project).filter(Project.current_stage == stage).count()
        for stage in stages
    }

col1, col2 = st.columns(2)

with col1:
    st.metric("📁 Total Projects", total_projects)
    st.metric("👤 Total Coaches", total_coaches)

with col2:
    st.markdown("**Stage Distribution:**")
    for stage, count in stage_counts.items():
        if count > 0:
            st.markdown(f"- {stage}: **{count}**")
