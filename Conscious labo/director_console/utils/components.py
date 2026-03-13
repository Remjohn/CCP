# Shared UI components for CMF Director's Console

import streamlit as st
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def show_progress_sidebar():
    """
    Display the progress tracker in the sidebar.
    Should be called by every page.
    """
    from db.connection import get_session
    from db.models import Project
    from config import VIDEO_VALUE, MONTHLY_GOAL, WEEKLY_GOAL, DAILY_GOAL, CURRENCY
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 💰 Progress Tracker")
        
        with get_session() as session:
            # Get current month/week stats
            now = datetime.now()
            current_month = now.month
            current_year = now.year
            
            # Start of current week (Monday)
            week_start = now - timedelta(days=now.weekday())
            
            # Count completed videos
            total_completed = session.query(Project).filter(
                Project.current_stage == "completed"
            ).count()
            
            month_completed = session.query(Project).filter(
                Project.current_stage == "completed",
                Project.month == current_month
            ).count()
            
            # For weekly, check projects completed this week
            week_completed = session.query(Project).filter(
                Project.current_stage == "completed",
                Project.updated_at >= week_start
            ).count()
        
        # === MONTHLY GOAL ===
        month_progress = month_completed / MONTHLY_GOAL
        month_earnings = month_completed * VIDEO_VALUE
        
        st.markdown(f"**📅 {now.strftime('%B')} Goal**")
        st.progress(min(month_progress, 1.0))
        st.markdown(f"**{month_completed}/{MONTHLY_GOAL}** videos")
        st.markdown(f"💵 **{CURRENCY}{month_earnings:,}** earned")
        
        # === WEEKLY GOAL ===
        week_progress = week_completed / WEEKLY_GOAL
        week_earnings = week_completed * VIDEO_VALUE
        
        st.markdown(f"**📆 Week Goal**")
        st.progress(min(week_progress, 1.0))
        st.markdown(f"**{week_completed}/{WEEKLY_GOAL}** videos")
        st.markdown(f"💵 **{CURRENCY}{week_earnings:,}** earned")
        
        # === TOTAL STATS ===
        total_earnings = total_completed * VIDEO_VALUE
        st.markdown("---")
        st.markdown(f"**🏆 All Time**")
        st.markdown(f"📹 **{total_completed}** videos")
        st.markdown(f"💰 **{CURRENCY}{total_earnings:,}** total")
        
        # === MOTIVATIONAL INDICATOR ===
        st.markdown("---")
        
        # Days left in month
        import calendar
        days_in_month = calendar.monthrange(current_year, current_month)[1]
        days_left = days_in_month - now.day
        videos_needed = MONTHLY_GOAL - month_completed
        
        if videos_needed > 0 and days_left > 0:
            daily_rate_needed = videos_needed / days_left
            st.caption(f"📈 Need **{daily_rate_needed:.1f}**/day to hit goal")
            
            if daily_rate_needed <= DAILY_GOAL:
                st.success("✅ On track!")
            elif daily_rate_needed <= DAILY_GOAL * 1.5:
                st.warning("⚠️ Pick up the pace!")
            else:
                st.error("🔥 Time to hustle!")
        elif videos_needed <= 0:
            st.success("🎉 Monthly goal achieved!")
            st.balloons()


def show_video_value_setting():
    """Display and allow editing of video value in settings."""
    from config import VIDEO_VALUE, MONTHLY_GOAL, WEEKLY_GOAL, CURRENCY
    
    st.subheader("💰 Gamification Settings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(f"Video Value", f"{CURRENCY}{VIDEO_VALUE}")
    with col2:
        st.metric("Monthly Goal", f"{MONTHLY_GOAL} videos")
    with col3:
        st.metric("Weekly Goal", f"{WEEKLY_GOAL} videos")
    
    st.info("💡 Edit `config.py` to change these values.")
    
    # Preview of monthly potential
    monthly_potential = MONTHLY_GOAL * VIDEO_VALUE
    st.markdown(f"**Monthly Potential:** {CURRENCY}{monthly_potential:,}")


def page_header(title: str, icon: str = ""):
    """Standard page header with icon."""
    st.title(f"{icon} {title}" if icon else title)
    show_progress_sidebar()
