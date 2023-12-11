
create table project
(
    project_id int          not null
        primary key,
    name       varchar(255) null
)
    engine = InnoDB;

create table repository
(
    repository_id int          not null
        primary key,
    project_id    int          null,
    name          varchar(255) null,
    constraint repository_ibfk_1
        foreign key (project_id) references project (project_id)
)
    engine = InnoDB;

create table task
(
    task_id       int          not null
        primary key,
    repository_id int          null,
    name          varchar(255) null,
    completed     tinyint(1)   null,
    constraint task_ibfk_1
        foreign key (repository_id) references repository (repository_id)
)
    engine = InnoDB;

create table subtask
(
    subtask_id int          not null
        primary key,
    task_id    int          null,
    name       varchar(255) null,
    completed  tinyint(1)   null,
    constraint subtask_ibfk_1
        foreign key (task_id) references task (task_id)
)
    engine = InnoDB;
    
create index project_id
    on repository (project_id);
    
create index repository_id
    on task (repository_id);

create index task_id
    on subtask (task_id);

INSERT INTO listify_bdd.project (project_id, name) VALUES (1, 'Projet 1');
INSERT INTO listify_bdd.project (project_id, name) VALUES (2, 'Projet 2');
INSERT INTO listify_bdd.project (project_id, name) VALUES (3, 'Projet 3');
INSERT INTO listify_bdd.project (project_id, name) VALUES (4, 'Projet 4');

INSERT INTO listify_bdd.repository (repository_id, project_id, name) VALUES (1, 1, 'A faire');
INSERT INTO listify_bdd.repository (repository_id, project_id, name) VALUES (2, 1, 'En cours');
INSERT INTO listify_bdd.repository (repository_id, project_id, name) VALUES (3, 1, 'Terminé');
INSERT INTO listify_bdd.repository (repository_id, project_id, name) VALUES (4, 2, 'Repo 1 2');
INSERT INTO listify_bdd.repository (repository_id, project_id, name) VALUES (5, 3, 'Ménage');
INSERT INTO listify_bdd.repository (repository_id, project_id, name) VALUES (6, 3, 'Cuisine');
INSERT INTO listify_bdd.repository (repository_id, project_id, name) VALUES (7, 4, 'Test');
INSERT INTO listify_bdd.repository (repository_id, project_id, name) VALUES (8, 4, 'Test 2');

INSERT INTO listify_bdd.task (task_id, repository_id, name, completed) VALUES (1, 1, 'Tache 1', 0);
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed) VALUES (2, 1, 'Tache 2 ', 0);
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed) VALUES (3, 1, 'Tache 3', 0);
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed) VALUES (4, 2, 'Tache 1 2', 0);
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed) VALUES (5, 2, 'Tache 2 2', 0);
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed) VALUES (6, 2, 'Tache 3 2', 0);
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed) VALUES (7, 3, 'Tache 1 3', 1);
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed) VALUES (8, 3, 'Tache 2 3', 1);
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed) VALUES (9, 5, 'Aspirateur', 0);
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed) VALUES (10, 6, 'Gateau', 0);
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed) VALUES (11, 5, 'Serpillère', 1);
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed) VALUES (12, 6, 'Repas', 1);

INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (1, 10, 'Farine', 0);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (2, 10, 'Sucre', 0);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (3, 10, 'Beure', 1);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (4, 12, 'vaisselle', 1);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (5, 12, 'table', 0);