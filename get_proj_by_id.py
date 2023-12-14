from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, Session, relationship

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


# TODO: this is a test local sql database, to change
engine = create_engine('mysql://root:vm@vm.lan/listify_bdd', echo=True)
Base.metadata.create_all(engine)

# Create a session
session = Session(engine)

# Query for the project and its related entities
project_id_to_dict = {}
projects = session.query(Project).all()
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

# Close the session
session.close()


# Access the dictionary for a specific project_id
def get_project_dict_by_id(project_id):
    return project_id_to_dict.get(project_id)

