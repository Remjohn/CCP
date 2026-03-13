# Page 9: Calendar View

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, date, timedelta
import calendar

sys.path.insert(0, str(Path(__file__).parent.parent))
from db.connection import get_session
from db.models import Project, Coach

st.set_page_config(page_title="Calendar", page_icon="📅", layout="wide")

st.title("📅 Production Calendar")
st.markdown("View and schedule projects by day.")

st.divider()

# Month selector
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    selected_month = st.selectbox(
        "Month",
        range(1, 13),
        index=datetime.now().month - 1,
        format_func=lambda x: calendar.month_name[x]
    )

with col2:
    selected_year = st.number_input(
        "Year",
        min_value=2024,
        max_value=2030,
        value=datetime.now().year
    )

st.divider()

# Get projects for selected month
with get_session() as session:
    # Get all projects scheduled for this month
    projects = session.query(Project).filter(
        Project.month == selected_month
    ).order_by(Project.scheduled_day, Project.video_number).all()
    
    # Group by day
    projects_by_day = {}
    unscheduled = []
    
    for proj in projects:
        if proj.scheduled_day:
            day = proj.scheduled_day.day
            if day not in projects_by_day:
                projects_by_day[day] = []
            projects_by_day[day].append(proj)
        else:
            unscheduled.append(proj)
    
    # Calendar view
    st.subheader(f"📅 {calendar.month_name[selected_month]} {selected_year}")
    
    # Get calendar for month
    cal = calendar.Calendar(firstweekday=0)  # Monday start
    weeks = cal.monthdayscalendar(selected_year, selected_month)
    
    # Header row
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    header_cols = st.columns(7)
    for i, day in enumerate(days):
        with header_cols[i]:
            st.markdown(f"**{day}**")
    
    # Calendar weeks
    for week in weeks:
        week_cols = st.columns(7)
        for i, day in enumerate(week):
            with week_cols[i]:
                if day == 0:
                    st.markdown("")  # Empty cell
                else:
                    # Day number
                    day_projects = projects_by_day.get(day, [])
                    
                    if day_projects:
                        # Has projects
                        st.markdown(f"**{day}** ({len(day_projects)})")
                        for proj in day_projects[:3]:  # Show max 3
                            status_icon = "✅" if proj.current_stage == "completed" else "⏳"
                            coach = session.query(Coach).filter(Coach.id == proj.coach_id).first()
                            coach_name = coach.name if coach else "?"
                            st.caption(f"{status_icon} {coach_name}")
                        if len(day_projects) > 3:
                            st.caption(f"+{len(day_projects) - 3} more")
                    else:
                        st.markdown(f"{day}")

st.divider()

# Unscheduled projects
if unscheduled:
    st.subheader(f"⏳ Unscheduled Projects ({len(unscheduled)})")
    
    for proj in unscheduled:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**{proj.full_code or proj.project_id}**")
        
        with col2:
            st.markdown(f"`{proj.current_stage}`")
        
        with col3:
            # Quick schedule
            new_day = st.number_input(
                "Day",
                min_value=1,
                max_value=31,
                value=1,
                key=f"day_{proj.id}"
            )
            if st.button("📅", key=f"schedule_{proj.id}"):
                with get_session() as s:
                    p = s.query(Project).filter(Project.id == proj.id).first()
                    if p:
                        p.scheduled_day = date(selected_year, selected_month, new_day)
                st.rerun()

st.divider()

# Summary stats
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Scheduled", len(projects) - len(unscheduled))
with col2:
    st.metric("Unscheduled", len(unscheduled))
with col3:
    completed = sum(1 for p in projects if p.current_stage == "completed")
    st.metric("Completed", f"{completed}/{len(projects)}")
