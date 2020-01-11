create table Graph(
idGraph int primary key,
Graph varchar(50)
)
GO
create table GraphRoot(
    idGraphRoot int IDENTITY(1,1) primary key,
    idGraph int references Graph(idGraph) not null,
    idNode bigint,
    CodeNode varchar(100),
    LevelToExplore int not null,
    CompleteExploration bit default(0) not null,
    Active bit default(1) not null,
    CONSTRAINT check_ids
    CHECK ((idNode is not null) or (CodeNode is not NULL) )
)
go
create table GraphNodeEdge(
    idGraphNodeEdge bigint identity(1,1) primary key,
    idGraph int references Graph(idGraph) not null,
    idUserNode bigint not null ,
    screen_nameUserNode varchar(100),
    nameUserNode varchar(1000),
    idFriendEdge bigint not null, 
    screen_nameFriendEdge varchar(100),
    nameFriendEdge varchar(1000),
    Degree int not null ,
    Complete bit default(0) not null,
    isNode bit default(0) not null,
    Active bit default(1) not null
)
go
ALTER TABLE GraphRoot
ADD CONSTRAINT C_GraphRoot_Unique_CodeNode UNIQUE (idGraph,CodeNode);
GO
ALTER TABLE GraphNodeEdge
ADD CONSTRAINT C_GraphNodeEdge_Unique_idUserNode_idFriendEdge UNIQUE (idGraph,idUserNode,idFriendEdge);
go
CREATE NONCLUSTERED INDEX IX_GraphRoot_idNode
    ON GraphRoot (idNode)
go
CREATE NONCLUSTERED INDEX IX_GraphRoot_CodeNode
    ON GraphRoot (CodeNode)
go
CREATE NONCLUSTERED INDEX IX_GraphNodeEdge_idUserNode
    ON GraphNodeEdge (idUserNode)
go
CREATE NONCLUSTERED INDEX IX_GraphNodeEdge_idFriendEdge
    ON GraphNodeEdge (idFriendEdge)
GO
ALTER TABLE GraphRoot
ADD CONSTRAINT C_GraphRoot UNIQUE (idGraph,CodeNode);
go

insert into Graph(idGraph,Graph) 
values (1, 'Twitter amigos')
go
insert into GraphRoot(idGraph,CodeNode,LevelToExplore)
values (1,'jipinillal',2)
go
insert into GraphRoot(idGraph,CodeNode,LevelToExplore)
values (1,'jota_jocelin',2)
go
insert into GraphRoot(idGraph,CodeNode,LevelToExplore)
values (1,'MaisAngel',2)
go
insert into GraphRoot(idGraph,CodeNode,LevelToExplore)
values (1,'JorgeRizik',2)


