from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
import nltk
import playsound
from py2neo import Graph
from py2neo import Database, NodeMatch
from py2neo import cypher
import py2neo
import neo4j
import time
db = Database("http://localhost:7474/")
graph = Graph("http://localhost:7474/")
graph.begin()
graph.database=db
def gen_res(number):
    li = []
    li1=[]
    li2=[]
    for rel in graph.match((), r_type="indicates"):
        s = rel.start_node["sid"]
        if int(s) == number:
            li1.append(rel.end_node)
            li2.append(rel.end_node['label'])
    print(number)
    for i in li1:
        a=[]
        a.append(i['symptom1'])
        a.append(i['symptom2'])
        a.append(i['symptom3'])
        a.append(i['symptom4'])
        a.append(i['symptom5'])
        a.append(i['symptom6'])
        a.append(i['symptom7'])
        a.append(i['symptom8'])
        a.append(i['symptom9'])
        li.append(a)
    print (li)
    return li,li2
