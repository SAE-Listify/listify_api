# drop database listify_bdd;
create database if not exists listify_bdd;
use listify_bdd;

create table if not exists project
(
    project_id int auto_increment
        primary key,
    name       varchar(255) not null
);

create table if not exists repository
(
    repository_id int auto_increment
        primary key,
    project_id    int          not null,
    name          varchar(255) not null,
    constraint project_id
        foreign key (project_id) references project (project_id)
            on update cascade on delete cascade
);

create index project_id_idx
    on repository (project_id);

create table if not exists task
(
    task_id       int auto_increment
        primary key,
    repository_id int          not null,
    name          varchar(255) not null,
    completed     tinyint(1)   not null,
    priority      varchar(255) not null,
    due_date      date,
    assignee      varchar(255),
    constraint repository_id
        foreign key (repository_id) references repository (repository_id)
            on update cascade on delete cascade
);

create table if not exists subtask
(
    subtask_id int auto_increment
        primary key,
    task_id    int          not null,
    name       varchar(255) not null,
    completed  tinyint(1)   not null,
    constraint task_id
        foreign key (task_id) references task (task_id)
            on update cascade on delete cascade
);

create index task_id_idx
    on subtask (task_id);

create index repository_id_idx
    on task (repository_id);


INSERT INTO listify_bdd.project (project_id, name) VALUES (1, 'Projet 1');
INSERT INTO listify_bdd.project (project_id, name) VALUES (2, 'Projet 2');


INSERT INTO listify_bdd.repository (repository_id, project_id, name) VALUES (1, 1, 'A faire');
INSERT INTO listify_bdd.repository (repository_id, project_id, name) VALUES (2, 1, 'En cours');
INSERT INTO listify_bdd.repository (repository_id, project_id, name) VALUES (3, 1, 'Termine');
INSERT INTO listify_bdd.repository (repository_id, project_id, name) VALUES (4, 2, 'Repo 1');
INSERT INTO listify_bdd.repository (repository_id, project_id, name) VALUES (5, 2, 'Repo 2');
INSERT INTO listify_bdd.repository (repository_id, project_id, name) VALUES (6, 2, 'Repo 3');


INSERT INTO listify_bdd.task (task_id, repository_id, name, completed, due_date, assignee, priority) VALUES (9, 1, 'Menage', 0, '2023-12-22', 'qqun', 'Aucune');
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed, due_date, assignee, priority) VALUES (10, 1, 'Cuisine', 0, '2023-12-22', 'qqun', 'Aucune');
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed, due_date, assignee, priority) VALUES (11, 2, 'Devoirs', 0, '2023-12-22', 'Thomas', 'Aucune');
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed, due_date, assignee, priority) VALUES (12, 2, 'Reviser', 0, '2023-12-22', 'Thomas', 'Aucune');
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed, due_date, assignee, priority) VALUES (13, 3, 'Ranger', 1, '2023-12-18', 'Jules', 'Aucune');
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed, due_date, assignee, priority) VALUES (14, 3, 'Faire les courses', 1, '2023-12-18', 'Jules', 'Aucune');
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed, due_date, assignee, priority) VALUES (15, 4, 'Tache 1', 0, '2023-12-22', 'Louis', 'Aucune');
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed, due_date, assignee, priority) VALUES (16, 4, 'Tache 2', 0, '2023-12-22', 'Louis', 'Aucune');
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed, due_date, assignee, priority) VALUES (17, 5, 'Tache 3', 0, '2023-12-22', 'Mass', 'Aucune');
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed, due_date, assignee, priority) VALUES (18, 5, 'Tache 4', 1, '2023-12-18', 'Mass', 'Aucune');
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed, due_date, assignee, priority) VALUES (19, 6, 'TAche 5 ', 1, '2023-12-18', 'Rayne', 'Aucune');
INSERT INTO listify_bdd.task (task_id, repository_id, name, completed, due_date, assignee, priority) VALUES (20, 6, 'Tache 6', 1, '2023-12-18', 'Rayane', 'Aucune');


INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (2, 9, 'Aspirateur', 0);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (3, 9, 'Balais', 1);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (4, 10, 'Plat', 0);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (5, 10, 'Dessert', 1);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (6, 11, 'Dm de Maths', 0);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (7, 11, 'Exos de Mura', 1);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (8, 12, 'PDF de Bielmann', 0);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (9, 12, 'Active Directory', 1);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (10, 13, 'Bureau', 1);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (11, 13, 'Chambre', 1);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (12, 14, 'Des fruits', 1);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (13, 14, 'De la viande', 1);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (14, 15, 'Sous-tache 1', 0);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (15, 15, 'Sous-tache 2', 1);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (16, 16, 'Sous-tache 3', 0);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (17, 16, 'Sous-tache 4', 1);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (18, 17, 'Sous-tache 5', 0);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (19, 17, 'Sous-tache 6', 1);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (20, 18, 'Sous-tache 7', 0);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (21, 18, 'Sous-tache 8', 1);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (22, 19, 'Sous-tache 9', 0);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (23, 19, 'Sous-tache 10', 1);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (24, 20, 'Sous-tache 11', 0);
INSERT INTO listify_bdd.subtask (subtask_id, task_id, name, completed) VALUES (25, 20, 'Sous-tache 12', 1);
