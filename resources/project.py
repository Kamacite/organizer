import os, sys
from flask import jsonify, request
from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import *
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from models.project_models import Project as mProject, Section as mSection, Task as mTask
from models.project_schemas import project_schema, section_schema, task_schema

class Projects(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        try:
            result_projects = self.db.session.query(mProject.id, mProject.name, mProject.details).filter(mProject.owner_id == user_id).order_by(mProject.name.asc()).all()
        except:
            abort(404, message="No projects found.")
        user_projects = []
        for proj in result_projects:
            user_projects.append({
                'id': proj[0],
                'name': proj[1],
                'details': proj[2]
            })    
        return jsonify(user_projects)

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        error = project_schema.validate(request.json, session=self.db.session)
        if error:
            abort(400, message=str(error))
        new_project = project_schema.load(request.json)
        new_project.owner_id = user_id
        new_project.last_updated = datetime.now().isoformat()
        new_project.active = True
        new_project.updated_by = user_id
        self.db.session.add(new_project)
        self.db.session.commit()
        return jsonify({'id':new_project.id, 'name':new_project.name, 'details':new_project.details})

class Project(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    @jwt_required
    def get(self, project_id):
        user_id = get_jwt_identity()
        try:
            project = self.db.session.query(mProject).filter(mProject.id == project_id, mProject.owner_id == user_id).one()
        except:
            abort(404)
        return project_schema.dump(project)

    # Add new section to project
    @jwt_required
    def post(self, project_id):
        user_id = get_jwt_identity()
        error = section_schema.validate(request.json, session=self.db.session)
        if error:
            abort(400, message=str(error))
        try:
            project = self.db.session.query(mProject).filter(mProject.id == project_id, mProject.owner_id == user_id).one()
        except:
            abort(404) 
        new_section = section_schema.load(request.json)
        new_section.project_id = project_id
        new_section.owner_id = user_id
        new_section.last_updated = datetime.now().isoformat()
        new_section.active = True
        new_section.updated_by = user_id
        self.db.session.add(new_section)
        self.db.session.commit()
        return section_schema.dump(new_section)
        

    @jwt_required
    def patch(self, project_id):
        pass

    @jwt_required
    def delete(self, project_id):
        pass

class Section(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']
 
    # Add new task to section
    @jwt_required
    def post(self, section_id):
        user_id = get_jwt_identity()
        error = task_schema.validate(request.json, session=self.db.session)
        if error:
            abort(400, message=str(error))
        try:
            section = self.db.session.query(mSection).filter(mSection.id == section_id, mSection.owner_id == user_id).one()
        except:
            abort(404)
        new_task = task_schema.load(request.json)
        new_task.section_id = section_id
        new_task.owner_id = user_id
        new_task.last_updated = datetime.now().isoformat()
        new_task.updated_by = user_id
        new_task.active = True
        self.db.session.add(new_task)
        self.db.session.commit()
        return task_schema.dump(new_task)
    
    def _order_sections(self, section, new_position):
        if(section.position > new_position):
            #Moved to left
            update_sections = self.db.session.query(mSection).filter(mSection.position >= new_position, mSection.position < section.position).all()
            for s in update_sections:
                s.position = s.position + 1
            section.position = new_position
        elif(section.position < new_position):
            #Move Right
            update_sections = self.db.session.query(mSection).filter(mSection.position <= new_position, mSection.position > section.position).all()
            for s in update_sections:
                s.position = s.position - 1
            section.position = new_position

    @jwt_required
    def patch(self, section_id):
        user_id = get_jwt_identity()
        error = section_schema.validate(request.json, session=self.db.session)
        if error:
            abort(400, message=str(error))
        try:
            section = self.db.session.query(mSection).filter(mSection.id == section_id, mSection.owner_id == user_id).one()
        except:
            abort(404)
        section_updates = section_schema.load(request.json)
        if(section_updates.position != section.position and section_updates.position != None):
            #reorder sections
            self._order_sections(section, section_updates.position)
        else:
            #Update name
            pass
        section.last_updated = datetime.now().isoformat()
        section.updated_by = user_id
        self.db.session.commit()
        return section_schema.dump(section)
    
    @jwt_required
    def delete(self):
        pass

class Task(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def _order_tasks(self,task,new_section_id,new_position):
        # Moved to new section
        if (task.section_id != new_section_id):
            try:
                old_section_tasks = self.db.session.query(mTask).filter(mTask.section_id == task.section_id, mTask.position > task.position).all()
                for t in old_section_tasks:
                    t.position = t.position - 1
            except:
                pass
            try:
                new_section_tasks = self.db.session.query(mTask).filter(mTask.section_id == new_section_id, mTask.position >= new_position).all()
                for t in new_section_tasks:
                    t.position = t.position + 1
            except:
                pass
            task.position = new_position
            task.section_id = new_section_id
        # Same section
        elif (task.position > new_position):
            #Moved to lower position
            update_tasks = self.db.session.query(mTask).filter(mTask.section_id == task.section_id, mTask.position >= new_position, mTask.position < task.position).all()
            for t in update_tasks:
                t.position = t.position + 1
            task.position = new_position
        elif (task.position < new_position):
            #Moved to higher position
            update_tasks = self.db.session.query(mTask).filter(mTask.section_id == task.section_id, mTask.position <= new_position, mTask.position > task.position).all()
            for t in update_tasks:
                t.position = t.position - 1
            task.position = new_position

    # Update task details
    @jwt_required
    def patch(self, task_id):
        user_id = get_jwt_identity()
        error = task_schema.validate(request.json, session=self.db.session)
        if error:
            abort(400, message=str(error))
        try:
            task = self.db.session.query(mTask).filter(mTask.id == task_id, mTask.owner_id == user_id).one()
        except:
            abort(404)
        task_updates = task_schema.load(request.json)
        if ( (task.position != task_updates.position or task.section_id != task_updates.section_id) and task_updates.position != None and task_updates.section_id != None):
            self._order_tasks(task, task_updates.section_id, task_updates.position)
        else:
            task.details = task_updates.details
            task.active = task_updates.active

        task.last_updated = datetime.now().isoformat()
        task.updated_by = user_id
        self.db.session.commit()
        return task_schema.dump(task)

    @jwt_required
    def delete(self):
        pass
