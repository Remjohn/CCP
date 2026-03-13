# SQLAlchemy models for CMF Director's Console V2

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Coach(Base):
    """Coach/Brand entity."""
    __tablename__ = "coaches"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    folder_path = Column(String(500))
    avatar_path = Column(String(500))  # V2: Coach avatar image
    assets_folder = Column(String(500))  # V2: Root folder for coach projects
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    projects = relationship("Project", back_populates="coach")
    
    def __repr__(self):
        return f"<Coach {self.name}>"


class Project(Base):
    """Individual video project."""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(String(50), unique=True, nullable=False)  # e.g., "01_50-12"
    name = Column(String(255))  # e.g., "Matthis"
    
    # V2: New naming fields
    video_number = Column(Integer)  # CVN (001-220)
    month = Column(Integer)  # MM (01-12)
    total_videos = Column(Integer, default=220)  # TVN
    full_code = Column(String(50))  # e.g., "009-220-12-Adele"
    scheduled_day = Column(Date)  # Day this video is scheduled for
    
    coach_id = Column(Integer, ForeignKey("coaches.id"))
    folder_path = Column(String(500))
    current_stage = Column(String(50), default="pending")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    coach = relationship("Coach", back_populates="projects")
    stage_approvals = relationship("StageApproval", back_populates="project")
    assets = relationship("Asset", back_populates="project")
    outputs = relationship("Output", back_populates="project")
    batch_projects = relationship("BatchProject", back_populates="project")
    comments = relationship("ProjectComment", back_populates="project")  # V2
    commands = relationship("PendingCommand", back_populates="project")  # V2
    
    def __repr__(self):
        return f"<Project {self.full_code or self.project_id}: {self.name}>"


class Batch(Base):
    """Batch execution run."""
    __tablename__ = "batches"
    
    id = Column(Integer, primary_key=True)
    batch_id = Column(String(100), unique=True, nullable=False)
    current_stage = Column(String(50), default="scripts")
    status = Column(String(50), default="pending")
    total_projects = Column(Integer, default=0)
    completed_projects = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime)
    
    # Relationships
    batch_projects = relationship("BatchProject", back_populates="batch")
    
    def __repr__(self):
        return f"<Batch {self.batch_id}>"


class BatchProject(Base):
    """Many-to-many relationship between batches and projects."""
    __tablename__ = "batch_projects"
    
    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer, ForeignKey("batches.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    order_index = Column(Integer, default=0)
    
    # Relationships
    batch = relationship("Batch", back_populates="batch_projects")
    project = relationship("Project", back_populates="batch_projects")


class StageApproval(Base):
    """Approval status for each stage of a project."""
    __tablename__ = "stage_approvals"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    stage = Column(String(50), nullable=False)
    status = Column(String(50), default="pending")
    approved_at = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="stage_approvals")
    
    def __repr__(self):
        return f"<StageApproval {self.project_id}:{self.stage}={self.status}>"


class Asset(Base):
    """Generated or procured assets."""
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    asset_type = Column(String(50))
    asset_role = Column(String(50))
    file_path = Column(String(500))
    file_name = Column(String(255))
    scene_number = Column(Integer)
    status = Column(String(50), default="generated")
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="assets")
    
    def __repr__(self):
        return f"<Asset {self.file_name}>"


class Output(Base):
    """Final output files."""
    __tablename__ = "outputs"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    output_type = Column(String(50))
    file_path = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="outputs")
    
    def __repr__(self):
        return f"<Output {self.output_type}>"


# V2: New models

class ProjectComment(Base):
    """Comments on projects, including re-run instructions for agent."""
    __tablename__ = "project_comments"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    comment = Column(Text, nullable=False)
    is_rerun_instruction = Column(Boolean, default=False)
    stage = Column(String(50))  # Which stage this comment relates to
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="comments")
    
    def __repr__(self):
        return f"<Comment project={self.project_id} rerun={self.is_rerun_instruction}>"


class PendingCommand(Base):
    """Commands waiting to be executed by the agent."""
    __tablename__ = "pending_commands"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    command_type = Column(String(50), nullable=False)  # run_scripts, run_assets, etc.
    command_args = Column(Text)  # JSON encoded arguments
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    error_message = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    executed_at = Column(DateTime)
    
    # Relationships
    project = relationship("Project", back_populates="commands")
    
    def __repr__(self):
        return f"<PendingCommand {self.command_type} status={self.status}>"
