import json
import csv
import pandas as pd
from datetime import date
from datetime import datetime
import time
import pyodbc
import twitterAPI as twa
import getUserfromSQL as getSql
import tweepy  

NumberGraph=2
######################################################################################
apitweepy = twa.getApi()
######################################################################################

rootNodes = getSql.getRootOfGraph(NumberGraph)

print(rootNodes)

#######################################################################################

usuarios=[]
for index, row in rootNodes.iterrows():
    user=apitweepy.get_user(user_id=None, screen_name=row['CodeNode'], include_entities=True, return_json=True,parser=tweepy.parsers.JSONParser())
    rowdata = [user['id'], user['id_str'], user['name'],user['screen_name'],user['location']]
 
    idGraph=row['idGraph']
    idNode=user['id']
    CodeNode=row['CodeNode']
    LevelToExplore=row['LevelToExplore']
    CompleteExploration=row['CompleteExploration']
    Active=row['Active']
    name=user['name']
    screen_name=user['screen_name']
 
    print('idGraph:',idGraph)
    print('idNode:',idNode)
    print('CodeNode:',CodeNode)
    print('LevelToExplore:',LevelToExplore)
    print('CompleteExploration:',CompleteExploration)
    print('Active:',Active)

    getSql.updateRootGraph(idGraph, idNode,CodeNode,LevelToExplore,CompleteExploration,Active) 
    nodoSql=getSql.getNodoFromDB(idNode,idGraph)

    if(len(nodoSql)==0):
        print('no esta registrado el nodo')
        respuesta = getSql.insertNodoFromDB(idGraph,idNode,idNode,LevelToExplore, 0,1,name,screen_name)
    usuarios.append(rowdata)


#######################################################################################




def nodeFun(idGraph):
    seguidos=[]
    nodo=getSql.getNodoNoCompletadoFromDB(idGraph)
    if(nodo==None):
        return 0

    screen_nameUserNode=nodo['screen_nameUserNode']
    nameUserNode=nodo['nameUserNode']
    idUserNode = nodo['idUserNode']
    Degree=nodo['Degree']
    print('idUserNode: ',idUserNode)
    seguidos=twa.get_timeline(idUserNode)

    print('Largo de array de seguidos es:' , len(seguidos))

    for row in seguidos:
        i=row['id']
        screen_nameFriendEdge=row['screen_name']
        nameFriendEdge=row['name']

        relacion=getSql.getRelationshipFromDB(idUserNode,i,idGraph)
        print('relacion: ',relacion)
        if(len(relacion)==0):
            respuesta=getSql.InsertRelationshipFromDB(idGraph,idUserNode,i,Degree, 0,0, screen_nameUserNode,nameUserNode,screen_nameFriendEdge,nameFriendEdge)
        if(Degree>0):
            gradoNodo=Degree-1
            nodoNuevo=getSql.getNodoFromDB(i,idGraph)
            if(len(nodoNuevo)==0):
               respuesta=getSql.insertNodoFromDB(idGraph,i,i,gradoNodo, 0,1,screen_nameFriendEdge,nameFriendEdge)
    
    getSql.UpdateCerrarNodoFromDB(idUserNode,idGraph)
    
    return(1)


#######################################################################################


loopbreak=1

while(loopbreak==1):
    try:
        loopbreak=nodeFun(NumberGraph)
    except:
        print('ocurrio un error')


#######################################################################################

