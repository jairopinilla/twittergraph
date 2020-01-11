import tweepy                  
import json
import csv
import pandas as pd
from datetime import date
from datetime import datetime
import time
import pyodbc

######################################################################################

with open('server.json') as server_file:
    data = json.load(server_file)

configserver = {
    "server" : data['server'],
    "user" : data['user'],
    "password": data['password'],
    "database": data['database']
}
    
server = configserver["server"]
database = configserver["database"]
username = configserver['user']
password = configserver['password']
driver= '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
conn.autocommit = True


######################################################################################

def getRootOfGraph(Numbergragh):
    query = "select idGraphRoot,idGraph,idNode,CodeNode, "\
            " CAST(LevelToExplore AS INT) AS LevelToExplore, "\
            " CAST(CompleteExploration AS INT) AS CompleteExploration, "\
            " CAST(Active AS INT) AS Active "\
            " From GraphRoot where active= 1 and CompleteExploration=0 and idgraph="+str(Numbergragh)
    rootNodes = pd.read_sql(query, conn)
    return rootNodes
######################################################################################

def getUserFromDB(iduser,idgraph):
    query = "SELECT * FROM dbo.GraphNodeEdge WHERE idUserNode="+str(iduser)+" and idgraph="+str(idgraph)
    usuario = pd.read_sql(query, conn)
    return usuario
######################################################################################

def getNodoFromDB(idUserNode,idgraph):
    query = "select * from GraphNodeEdge where isNode= 1 and Active=1 and idUserNode="+str(idUserNode)+" and idgraph="+str(idgraph)
    usuario = pd.read_sql(query, conn)
    return usuario
#getCompletedNode
def getNodoNoCompletadoFromDB(idgraph):
    query = "select top 1 idGraphNodeEdge,idGraph, idUserNode, idFriendEdge, "\
        "   Degree, cast(Complete as int) as Complete, cast(isNode as int) as isNode, "\
        " cast(active as int) as Active, screen_nameUserNode,nameUserNode,screen_nameFriendEdge,nameFriendEdge "\
        " from GraphNodeEdge where isNode= 1 and Active=1 and Complete=0 and idgraph="+str(idgraph)

    cursor = conn.cursor()
    cursor.execute(query) 
    usuario = cursor.fetchone()

    if usuario == None:
        return None
    else:
        return {
        "idGraphNodeEdge" : usuario.idGraphNodeEdge,
        "idGraph" : usuario.idGraph,
        "idUserNode": usuario.idUserNode,
        "idFriendEdge": usuario.idFriendEdge,
        "Degree": usuario.Degree,
        "Complete": usuario.Complete,
        "isNode": usuario.isNode,
        "Active": usuario.Active,
        "screen_nameUserNode":usuario.screen_nameUserNode,
        "nameUserNode":usuario.nameUserNode,
        "screen_nameFriendEdge":usuario.screen_nameFriendEdge,
        "nameFriendEdge":usuario.nameFriendEdge
            }

#UpdateCerrarNodoFromDB
def UpdateCerrarNodoFromDB(idUserNode,idgraph):
    query = "update GraphNodeEdge set Complete=1 where isNode=1 and idUserNode="+str(idUserNode)+" and idgraph="+str(idgraph)
    cursor = conn.cursor()
    cursor.execute(query)
    print('se cierra idUserNode:',idUserNode)
    print(query)
    return 1

def insertNodoFromDB(idGraph,idUserNode,idFriendEdge,Degree, Complete,isNode,screen_name,name):
    screen_name=screen_name.replace("'", "")
    screen_name=screen_name.replace('"', '')
    name=name.replace("'", "")
    name=name.replace('"', '')

    query="insert into GraphNodeEdge(idGraph,idUserNode,idFriendEdge,Degree, Complete,isNode,screen_nameUserNode,nameUserNode,screen_nameFriendEdge,nameFriendEdge) "\
        " values ("+str(idGraph)+","+str(idUserNode)+","+str(idFriendEdge)+","+str(Degree)+","+str(Complete)+","+str(isNode)+"," \
        "'"+str(screen_name)+"','"+str(name)+"','"+str(screen_name)+"','"+str(name)+"')"

    cursor = conn.cursor()
    cursor.execute(query)
    return 1
######################################################################################


def getRelationshipFromDB(idUserNode,idFriendEdge,idgraph):
    query = "select * from GraphNodeEdge where Active=1 and idUserNode="+str(idUserNode)+" and idFriendEdge="+str(idFriendEdge)+" and idgraph="+str(idgraph)
    usuario = pd.read_sql(query, conn)
    return usuario

def InsertRelationshipFromDB(idGraph,idUserNode,idFriendEdge,Degree, Complete,isNode, screen_nameUserNode,nameUserNode,screen_nameFriendEdge,nameFriendEdge):
    screen_nameUserNode=screen_nameUserNode.replace("'", "")
    screen_nameUserNode=screen_nameUserNode.replace('"', '')
    nameUserNode=nameUserNode.replace("'", "")
    nameUserNode=nameUserNode.replace('"', '')
    screen_nameFriendEdge=screen_nameFriendEdge.replace("'", "")
    screen_nameFriendEdge=screen_nameFriendEdge.replace('"', '')
    nameFriendEdge=nameFriendEdge.replace("'", "")
    nameFriendEdge=nameFriendEdge.replace('"', '')

    query="insert into GraphNodeEdge(idGraph,idUserNode,idFriendEdge,Degree, Complete,isNode, screen_nameUserNode,nameUserNode,screen_nameFriendEdge,nameFriendEdge) "\
        " values ("+str(idGraph)+","+str(idUserNode)+","+str(idFriendEdge)+","+str(Degree)+",0,0,'"+str(screen_nameUserNode)+"','"+str(nameUserNode)+"','"+str(screen_nameFriendEdge)+"','"+str(nameFriendEdge)+"')"
    
    cursor = conn.cursor()
    cursor.execute(query)
    return 1
######################################################################################

def updateRootGraph(idGraph, idNode,CodeNode,LevelToExplore,CompleteExploration,Active):
    cursor = conn.cursor()
    query="MERGE dbo.GraphRoot t " \
    " USING ( SELECT "+str(idGraph)+" as idGraph,"+str(idNode)+" as idNode,'"+str(CodeNode)+"' as CodeNode, "\
    +str(LevelToExplore)+" as LevelToExplore,"+str(CompleteExploration)+" as CompleteExploration,"+str(Active)+" as Active ) s "\
    " ON (s.CodeNode = t.CodeNode) "\
    " WHEN MATCHED "\
    " THEN UPDATE SET "\
    "  t.idGraph = s.idGraph, "\
    "   t.idNode = s.idNode,"\
	"	t.LevelToExplore = s.LevelToExplore,"\
	"	t.CompleteExploration = s.CompleteExploration"\
    " WHEN NOT MATCHED BY TARGET  "\
    " THEN INSERT (idGraph, idNode,CodeNode,LevelToExplore,CompleteExploration,Active) "\
    "    VALUES (s.idGraph, s.idNode,CodeNode,s.LevelToExplore,s.CompleteExploration,s.Active);"

    print(query)
    cursor.execute(query)

