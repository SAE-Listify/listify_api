from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, Session, relationship
from fastapi import HTTPException


Base = declarative_base()


class Project(Base):
    __tablename__ = 'project'
    project_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    repositories = relationship('Repository', back_populates='project')


class Repository(Base):
    __tablename__ = 'repository'
    repository_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.project_id'))
    name = Column(String(255))
    tasks = relationship('Task', back_populates='repository')
    project = relationship('Project', back_populates='repositories')


class Task(Base):
    __tablename__ = 'task'
    task_id = Column(Integer, primary_key=True)
    repository_id = Column(Integer, ForeignKey('repository.repository_id'))
    name = Column(String(255))
    completed = Column(Boolean)
    subtasks = relationship('Subtask', back_populates='task')
    repository = relationship('Repository', back_populates='tasks')


class Subtask(Base):
    __tablename__ = 'subtask'
    subtask_id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('task.task_id'))
    name = Column(String(255))
    completed = Column(Boolean)
    task = relationship('Task', back_populates='subtasks')


class DBConnection:
    def __init__(self, conn_string: str = "mysql://root:root@localhost/listify_bdd"):
        # TODO: this is a test local sql database, to change
        engine = create_engine(conn_string, echo=True)
        Base.metadata.create_all(engine)

        # Create a session
        self.session = Session(engine)

    def get_project_dict_by_id(self, project_id):
        # Query for the project and its related entities
        project_id_to_dict = {}
        projects = self.session.query(Project).all()
        for project in projects:
            project_dict = {'name': project.name, 'repositories': []}
            for repository in project.repositories:
                repository_dict = {'name': repository.name, 'tasks': []}
                for task in repository.tasks:
                    task_dict = {'name': task.name, 'completed': task.completed, 'subtasks': []}
                    for subtask in task.subtasks:
                        subtask_dict = {'name': subtask.name, 'completed': subtask.completed}
                        task_dict['subtasks'].append(subtask_dict)
                    repository_dict['tasks'].append(task_dict)
                project_dict['repositories'].append(repository_dict)
            project_id_to_dict[project.project_id] = project_dict
        if not project_id_to_dict.get(project_id):
            return HTTPException(status_code=404, detail="Project not found")
        return project_id_to_dict.get(project_id)

    def delete_element_by_id(self, element_type, element_id):
        try:
            element_class = globals().get(element_type)
            if element_class:
                element = self.session.query(element_class).get(element_id)
                if element:
                    self.session.delete(element)
                    self.session.commit()
                    return {"message": "Deleted successfully", "element_type": element_type, "element_id": element_id}
                else:
                    return HTTPException(status_code=404, detail=f"{element_type} with id {element_id} not found")
            else:
                print(f"Invalid element type: {element_type}")
        except Exception as e:
            self.session.rollback()
            return HTTPException(status_code=500, detail=f"Error deleting {element_type} with ID {element_id}: {e}")

    def session_close(self):
        self.session.close()

