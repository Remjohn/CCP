# Page 8: Coach Management - V3 with Create New Coach

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from db.connection import get_session, init_db
from db.models import Coach, Project
from config import CMF_ROOT, COACH_TEMPLATE_FILES, VIDEO_VALUE, MONTHLY_GOAL, WEEKLY_GOAL, CURRENCY
from datetime import datetime, timedelta
import calendar

st.set_page_config(page_title="Coaches", page_icon="👤", layout="wide")

init_db()

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
    
    # Monthly
    st.markdown(f"**📅 {now.strftime('%B')}**")
    st.progress(min(month_completed / MONTHLY_GOAL, 1.0))
    st.markdown(f"**{month_completed}/{MONTHLY_GOAL}** = {CURRENCY}{month_completed * VIDEO_VALUE:,}")
    
    # Weekly
    st.markdown(f"**📆 Week**")
    st.progress(min(week_completed / WEEKLY_GOAL, 1.0))
    st.markdown(f"**{week_completed}/{WEEKLY_GOAL}** = {CURRENCY}{week_completed * VIDEO_VALUE:,}")
    
    st.markdown("---")
    st.markdown(f"**🏆 Total:** {total_completed} = {CURRENCY}{total_completed * VIDEO_VALUE:,}")

# ============================================================
# MAIN CONTENT
# ============================================================
st.title("👤 Coach Management")
st.markdown("Create new coaches or link existing folders.")

st.divider()

# Default inputs directory
INPUTS_DIR = CMF_ROOT / "🇫🇷 Conscious Movie Factory" / "inputs"

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📋 Registered", "➕ Create New", "🔗 Link Existing", "🔍 Scan"])

with tab1:
    st.subheader("Registered Coaches")
    
    with get_session() as session:
        coaches = session.query(Coach).order_by(Coach.name).all()
        
        if not coaches:
            st.info("No coaches registered. Create one or scan for existing folders.")
        else:
            for coach in coaches:
                project_count = session.query(Project).filter(Project.coach_id == coach.id).count()
                
                with st.expander(f"👤 {coach.name} ({project_count} projects)", expanded=False):
                    st.markdown(f"**Folder:** `{coach.folder_path}`")
                    
                    if coach.folder_path and Path(coach.folder_path).exists():
                        folder = Path(coach.folder_path)
                        
                        st.markdown("**📄 CCF Documentation:**")
                        ccf_patterns = [
                            ("Tribe Soul", "*Tribe Soul*.md"),
                            ("Philosophy", "*Philosophy*.md"),
                            ("Branding", "*branding*.json"),
                        ]
                        
                        for name, pattern in ccf_patterns:
                            matches = list(folder.glob(pattern))
                            icon = "✅" if matches else "❌"
                            st.markdown(f"  {icon} {name}")
                        
                        project_folders = [d for d in folder.iterdir() if d.is_dir()]
                        st.markdown(f"**📁 Projects:** {len(project_folders)}")

with tab2:
    st.subheader("➕ Create New Coach")
    st.markdown("Creates folder with CCF template files.")
    
    with st.form("create_coach_form"):
        coach_name = st.text_input("Coach Name", placeholder="Bruno")
        
        base_dir = st.text_input(
            "Base Directory",
            value=str(INPUTS_DIR),
            help="Where to create the Coach folder"
        )
        
        st.markdown("**Will create:**")
        st.code(f"{base_dir}/Coach {coach_name}/\n├── Tribe Soul Profile.md\n├── Philosophy.md\n├── branding.json\n├── BUSINESS MODEL.md\n├── 7-11-4 SOPHISTICATION.md\n├── PRODUCTION BIBLE.md\n└── Conscious_Soul_Values.md")
        
        submitted = st.form_submit_button("✨ Create Coach", type="primary")
        
        if submitted and coach_name:
            folder_path = Path(base_dir) / f"Coach {coach_name}"
            
            if folder_path.exists():
                st.error(f"Folder already exists: {folder_path}")
            else:
                # Create folder
                folder_path.mkdir(parents=True, exist_ok=True)
                
                # Create template files
                for filename_template, content_template in COACH_TEMPLATE_FILES:
                    filename = filename_template.format(name=coach_name)
                    content = content_template.format(name=coach_name)
                    file_path = folder_path / filename
                    file_path.write_text(content, encoding="utf-8")
                
                # Register in database
                with get_session() as session:
                    coach = Coach(
                        name=coach_name,
                        folder_path=str(folder_path),
                        assets_folder=str(base_dir)
                    )
                    session.add(coach)
                
                st.success(f"✅ Created Coach '{coach_name}'!")
                st.markdown(f"**Folder:** `{folder_path}`")
                st.info("📝 Open the folder and fill in the template files with coach information.")
                st.rerun()

with tab3:
    st.subheader("🔗 Link Existing Coach Folder")
    
    with st.form("link_coach_form"):
        coach_name = st.text_input("Coach Name", placeholder="Adele")
        folder_path = st.text_input(
            "Full Folder Path",
            value=str(INPUTS_DIR / "Coach Adele") if INPUTS_DIR.exists() else "",
        )
        
        submitted = st.form_submit_button("🔗 Link Coach", type="primary")
        
        if submitted and coach_name and folder_path:
            folder = Path(folder_path)
            if not folder.exists():
                st.error(f"Folder does not exist: {folder_path}")
            else:
                with get_session() as session:
                    existing = session.query(Coach).filter(Coach.name == coach_name).first()
                    if existing:
                        st.error(f"Coach '{coach_name}' already registered!")
                    else:
                        coach = Coach(
                            name=coach_name,
                            folder_path=str(folder),
                            assets_folder=str(folder.parent)
                        )
                        session.add(coach)
                        st.success(f"✅ Linked Coach '{coach_name}'")
                        st.rerun()

with tab4:
    st.subheader("🔍 Auto-Scan Inputs Directory")
    st.markdown(f"Scanning: `{INPUTS_DIR}`")
    
    if INPUTS_DIR.exists():
        coach_folders = [d for d in INPUTS_DIR.iterdir() if d.is_dir() and d.name.startswith("Coach")]
        
        if not coach_folders:
            st.info("No 'Coach *' folders found.")
        else:
            st.markdown(f"**Found {len(coach_folders)} coach folder(s):**")
            
            for folder in coach_folders:
                coach_name = folder.name.replace("Coach ", "").strip()
                
                with get_session() as session:
                    existing = session.query(Coach).filter(Coach.name == coach_name).first()
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    status = "✅ Registered" if existing else "⚠️ Not registered"
                    project_count = len([d for d in folder.iterdir() if d.is_dir()])
                    st.markdown(f"**{folder.name}** - {status} ({project_count} projects)")
                
                with col2:
                    if not existing:
                        if st.button("➕ Register", key=f"reg_{coach_name}"):
                            with get_session() as session:
                                coach = Coach(
                                    name=coach_name,
                                    folder_path=str(folder),
                                    assets_folder=str(INPUTS_DIR)
                                )
                                session.add(coach)
                            st.success(f"Registered {coach_name}!")
                            st.rerun()
    else:
        st.error(f"Inputs directory not found: {INPUTS_DIR}")
