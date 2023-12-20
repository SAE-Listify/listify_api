from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import declarative_base, Session, relationship
from fastapi import HTTPException


Base = declarative_base()


class Project(Base):
    __tablename__ = 'project'
    project_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    repositories = relationship('Repository', back_populates='project', cascade='all, delete-orphan')


class Repository(Base):
    __tablename__ = 'repository'
    repository_id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('project.project_id'))
    name = Column(String(255))
    tasks = relationship('Task', back_populates='repository', cascade='all, delete-orphan')
    project = relationship('Project', back_populates='repositories')


class Task(Base):
    __tablename__ = 'task'
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    repository_id = Column(Integer, ForeignKey('repository.repository_id'))
    name = Column(String(255))
    completed = Column(Boolean)
    priority = Column(String(255))
    due_date = Column(Date)
    assignee = Column(String(255))
    subtasks = relationship('Subtask', back_populates='task', cascade='all, delete-orphan')
    repository = relationship('Repository', back_populates='tasks')


class Subtask(Base):
    __tablename__ = 'subtask'
    subtask_id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('task.task_id'))
    name = Column(String(255))
    completed = Column(Boolean)
    task = relationship('Task', back_populates='subtasks')


class DBConnection:
    """
    Database connection
    TIL ChatGPT is very good at creating docstrings!
    """
    def __init__(self, conn_string: str = "mysql://root:root@localhost/listify_bdd"):
        """
        Initializes a DBConnection object with a database connection string.

        :param conn_string: The connection string for the database.
        """
        # TODO: this is a test local sql database, to change
        engine = create_engine(conn_string, echo=True)
        Base.metadata.create_all(engine)

        # Create a session
        self.session = Session(engine)

    def get_projects_list(self):
        """
        Retrieves a list of projects with their names and IDs.

        :return: The list of projects in the following format:
        {"project_id": 1, "name": "TheProject"}
        """
        try:
            # Query for the projects
            projects = self.session.query(Project).all()

            # Create a list of dictionaries with project information
            projects_list = [
                {'project_id': project.project_id, 'name': project.name} for project in projects
            ]

            return projects_list
        except Exception as e:
            return HTTPException(status_code=500, detail=f"Error retrieving projects list: {e}")

    def get_project_dict_by_id(self, project_id):
        """
        Retrieves a dict representation of a project by its ID, including its repositories, tasks, and subtasks.

        :param project_id: The ID of the project to retrieve.
        :return: A dict representation of the project or an HTTPException if the project is not found.
        """
        # Query for the project and its related entities
        project_id_to_dict = {}
        projects = self.session.query(Project).all()
        for project in projects:
            project_dict = {'name': project.name, 'repositories': []}
            for repository in project.repositories:
                repository_dict = {'name': repository.name, 'tasks': []}
                for task in repository.tasks:
                    task_dict = {
                        'name': task.name,
                        'completed': task.completed,
                        'priority': task.priority,
                        'assignee': task.assignee,
                        'due_date': task.due_date,
                        'subtasks': []
                    }
                    for subtask in task.subtasks:
                        subtask_dict = {'name': subtask.name, 'completed': subtask.completed}
                        task_dict['subtasks'].append(subtask_dict)
                    repository_dict['tasks'].append(task_dict)
                project_dict['repositories'].append(repository_dict)
            project_id_to_dict[project.project_id] = project_dict
        if not project_id_to_dict[project_id]:
            return HTTPException(status_code=404, detail="Project not found")
        return project_id_to_dict[project_id]

    def delete_element_by_id(self, element_type, element_id):
        """
        Deletes an element of the specified type by its ID.

        :param element_type: The type of the element to delete ('Project', 'Repository', 'Task', 'Subtask').
        :param element_id: The ID of the element to delete.
        :return: A dict indicating success or an HTTPException if the element is not found or an error occurs.
        """
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

    def create_project_children(self, repositories_data, project):
        for repository_data in repositories_data:
            tasks_data = repository_data.pop("tasks", [])

            repository = Repository(**repository_data)
            repository.project = project  # Associate the repository with the project
            self.session.add(repository)

            # Create Task objects and associate them with the repository
            for task_data in tasks_data:
                subtasks_data = task_data.pop("subtasks", [])

                task = Task(**task_data)
                task.repository = repository  # Associate the task with the repository
                self.session.add(task)

                # Create Subtask objects and associate them with the task
                for subtask_data in subtasks_data:
                    subtask = Subtask(**subtask_data)
                    subtask.task = task  # Associate the subtask with the task
                    self.session.add(subtask)

    def add_project(self, project_data):
        """
        Adds a project to the database using the provided project data.

        :param project_data: A dict containing the project, with repositories, tasks, and subtasks.
        :return: A dict indicating success and the ID of the added project or an HTTPException if an error occurs.
        """
        try:
            # Extract project information
            project_info = project_data.copy()
            repositories_data = project_info.pop("repositories", [])

            # Create the Project instance
            project = Project(**project_info)
            self.session.add(project)

            # Create Repository objects and associate them with the project
            self.create_project_children(repositories_data, project)

            # Commit to the database
            self.session.commit()
            return {
                "message": f"Project '{project.name}' added successfully with ID {project.project_id}",
                "project_id": project.project_id
            }
        except Exception as e:
            self.session.rollback()
            return HTTPException(status_code=500, detail=f"Error adding project: {e}")

    def overwrite_project_by_id(self, project_id, new_project_data):
        """
        Overwrites a project with a new project dict by its ID.

        :param project_id: The ID of the project to overwrite.
        :param new_project_data: A dict containing the new project data.
        :return: A dict indicating success and the ID of the overwritten project or an HTTPException if an error occurs.
        """
        try:
            # Query for the existing project
            project = self.session.query(Project).get(project_id)

            if project:
                # Clear existing relationships
                project.repositories = []

                # Extract new project information
                new_project_info = new_project_data.copy()
                new_repositories_data = new_project_info.pop("repositories", [])

                # Update the existing project with new information
                # if the new-project does not have a name, it keeps the old one
                project.name = new_project_info.get("name", project.name)

                # Create new Repository objects and associate them with the project
                self.create_project_children(new_repositories_data, project)

                # Commit to the database
                self.session.commit()
                return {"message": f"Project overwritten successfully", "project_id": project_id}
            else:
                return HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
        except Exception as e:
            self.session.rollback()
            return HTTPException(status_code=500, detail=f"Error overwriting project: {e}")

    def session_close(self):
        """
         Closes the database session.
         """
        self.session.close()

