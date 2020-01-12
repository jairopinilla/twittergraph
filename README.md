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
first account to analyse, for example: if you want to start the graph with the Donald Trump twitter and level 2 of depth, you should insert his account in the table GraphRoot.

```sql
insert into Graph(idGraph,Graph) 
values (1, 'Twitter friend')
go
insert into GraphRoot(idGraph,CodeNode,LevelToExplore)
values (1,'realDonaldTrump',2)
```
The graph is built as follows:

![alt text](https://github.com/jairopinilla/twittergraph/blob/master/graph%20twitter.jpeg?raw=true)

The data is saved in SQL Server in this example, the most important table is GraphNodeEdge that saves the information about the edges and nodes.

The process will stop when the degree reaches the 0 value, in other words as higher you define in the GraphRoot table the LevelToExplore, more time the process will take.

The last part is to define the id of the graph to construct in the "main.py" file. 

```python
NumberGraph=2
```
