-- create database pokemon

use pokemon;

create table PokemonType(
    id int AUTO_INCREMENT primary key,
    name varchar(20),
    constraint PokemonType unique (name)
);

create table Pokemon(
    id int not null primary key,
    name varchar(20),
    type int,
    height float,
    weight float,
    foreign key (type) references PokemonType(id)
);

 create table Trainer(
     name varchar(20) primary key,
     town varchar(20)
 );

 create table PokemonTrainer(
     pid int,
     t_name varchar(20),
     foreign key (pid) references Pokemon(id),
     foreign key (t_name) references Trainer(name),
     primary key(pid, t_name)
 );

