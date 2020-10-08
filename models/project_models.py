import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

ProjectBase = declarative_base()

class Project(ProjectBase):
    __tablename__ = "projects"
    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(length=32))
    details = sql.Column(sql.String)
    owner_id = sql.Column(sql.Integer)
    sections = relationship("Section", back_populates="project")
    last_updated = sql.Column(sql.String)
    updated_by = sql.Column(sql.Integer)
    active = sql.Column(sql.Boolean)

class Section(ProjectBase):
    __tablename__ = 'sections'
    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String)
    project_id = sql.Column(sql.Integer, sql.ForeignKey('projects.id'))
    project = relationship("Project", back_populates="sections")
    tasks = relationship("Task", backref="section")
    owner_id = sql.Column(sql.Integer)
    last_updated = sql.Column(sql.String)
    updated_by = sql.Column(sql.Integer)
    position = sql.Column(sql.Integer)
    active = sql.Column(sql.Boolean)

class Task(ProjectBase):
    __tablename__ = 'tasks'
    id = sql.Column(sql.Integer, primary_key=True)
    details = sql.Column(sql.String)
    owner_id = sql.Column(sql.Integer)
    section_id = sql.Column(sql.Integer, sql.ForeignKey('sections.id'))
    last_updated = sql.Column(sql.String)
    updated_by = sql.Column(sql.Integer)
    position = sql.Column(sql.Integer)
    active = sql.Column(sql.Boolean)
