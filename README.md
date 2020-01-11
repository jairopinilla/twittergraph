# twittergraph
code to create a graph from twitter mentions

## Installation

It is a python app, so just download the repository, then create a virtual environment. To install all dependencies you should use the 
file requirements.txt with the command. 

```bash
pip install -r requirements.txt
```

## Run
The first step is to run the SQL script, in this case, is a SQL Server script. 
scheme.sql

In the last part of the script you should define the name of the graph and the root nodes, in other words, the graph is built with the 
first account to analyse, for example: if you want to start the graph with the Donald Trump twitter, you should insert his account in 
the table GraphRoot.

```sql
insert into Graph(idGraph,Graph) 
values (1, 'Twitter amigos')
go
insert into GraphRoot(idGraph,CodeNode,LevelToExplore)
values (1,'jipinillal',2)
```
