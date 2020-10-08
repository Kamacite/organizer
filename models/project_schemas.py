import os, sys
from marshmallow import post_load, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from models.project_models import Project, Section, Task

class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True

    details = fields.Str(validate=validate.Length(min=1))
    owner_id = auto_field()
    section_id = auto_field()
    last_updated = auto_field()
    updated_by = auto_field()
    position = auto_field()
    active = auto_field()

    @post_load
    def make_item(self, data, **kwargs):
        return Task(**data)

task_schema = TaskSchema()

class SectionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Section
        include_fk = True

    name = fields.Str(validate=validate.Length(min=1))
    last_updated = auto_field()
    owner_id = auto_field()
    project_id = auto_field()
    active = auto_field()
    tasks = fields.Nested(TaskSchema, many=True)
    position = auto_field()
    updated_by = auto_field()

    @post_load
    def make_item(self, data, **kwargs):
        return Section(**data)

section_schema = SectionSchema()

class ProjectSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        include_fk = True

    name = fields.Str(validate=validate.Length(min=1))
    details = auto_field()
    last_updated = auto_field()
    owner_id = auto_field()
    active = auto_field()
    sections = fields.Nested(SectionSchema, many=True)
    updated_by = auto_field()

    @post_load
    def make_item(self, data, **kwargs):
        return Project(**data)

project_schema = ProjectSchema()