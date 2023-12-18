import requests
import sqlite3
import json
import os.path
import pickle
import time
from requests.structures import CaseInsensitiveDict
from fcts import *
#tests debug
a=get_v('1','1','1','1','29','1','1')
b=get_r('#####', '1')
c=get_RS('1')
#######################################
#create table for Mou
if not os.path.isfile('./db.sqlite'):
    created=0;
    tuples_Mou=[];
    for Mou in get_Mou():
        tuples_Mou.append((Mou['Value'],Mou['Text']));

    if not os.path.isfile('./db.sqlite'):
     connection = sqlite3.connect('db.sqlite');created=1;#flag
     cursor = connection.cursor();
     cursor.execute("CREATE TABLE Mou (Mou_id integer primary key, Mou_name text)");
     cursor.executemany("INSERT INTO Mou   VALUES (?,?)",tuples_Mou);
     connection.commit();
    ###############################################################
    #create table for Qa
    if created==1:
     cursor.execute('CREATE TABLE Qa (Qa_id int primary key ,Qa_name text,parent_id integer, FOREIGN KEY (parent_id) REFERENCES Mou(Mou_id))');
    tuples_Qa=[];
    for Mou in tuples_Mou:
        tmp=get_r('Qa', Mou[0])
        for tmpp in tmp:
         tuples_Qa.append((tmpp['Value'],tmpp['Text'],Mou[0]));
    if created==1:
     cursor.executemany("INSERT INTO Qa   VALUES (?,?,?)",tuples_Qa);
     connection.commit();
    ###############################################################
    #create table for Qar
    if created==1:
     cursor.execute('CREATE TABLE Qar (Qar_id int primary key ,Qar_name text,parent_id integer, FOREIGN KEY (parent_id) REFERENCES Qa(Qa_id))');
    tuples_Qar=[];
    for val in tuples_Qa:
        tmp=get_r('Qar', val[0])
        for tmpp in tmp:
         tuples_Qar.append((tmpp['Value'],tmpp['Text'],val[0]));
    if created==1:
     cursor.executemany("INSERT INTO Qar   VALUES (?,?,?)",tuples_Qar);
     connection.commit();

    #############################################################################
    #create table for Qar_RS
    forbidden=[];
    if created==1:
     cursor.execute('CREATE TABLE RS (RS_id int primary key,RS_name text)');
     cursor.execute('CREATE TABLE Qar_RS (Qar_id int,RS_id int,Qa_id int, CONSTRAINT Qar_RS_pk PRIMARY KEY (Qar_id, RS_id),CONSTRAINT FK_Qar FOREIGN KEY (Qar_id) REFERENCES Qar(Qar_id),CONSTRAINT FK_RS FOREIGN KEY (RS_id) REFERENCES RS(RS_id),FOREIGN KEY (Qa_id) REFERENCES Qa(Qa_id))');
    tuples_Qar_RS=[];
    for Qar in tuples_Qar[:]:
        tmp=get_RS(Qar[0])
        tmppp=();
        for tmpp in tmp:
            if created==1:
             if tmpp['Value'] not in forbidden:
              cursor.execute("INSERT INTO RS VALUES (?,?)", (tmpp['Value'],tmpp['Text']));
             connection.commit();
             forbidden.append(tmpp['Value']);
            tuples_Qar_RS.append((Qar[0],tmpp['Value'],Qar[2]))
    if created==1:
     cursor.executemany("INSERT INTO Qar_RS VALUES (?,?,?)", tuples_Qar_RS);
     connection.commit();
     with open('objs.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
         pickle.dump([tuples_Mou, tuples_Qa,tuples_Qar,tuples_Qar_RS], f)
#############################################################################
connection = sqlite3.connect('db.sqlite');created=1;
cursor = connection.cursor();
with open('objs.pkl','rb') as f:  # Python 3: open(..., 'rb')
    [tuples_Mou, tuples_Qa,tuples_Qar,tuples_Qar_RS] = pickle.load(f)
#create table for VL
tuples_VL=[];
Ge=['1','2'];
for Mou in tuples_Mou[3:]:
   for Qa in tuples_Qa[:]:
       if Qa[0]=='19': #Qa[2]==Mou[0]:
         #cursor.execute(
               #'CREATE TABLE VL_'+str(Qa[0])+' (FN text,LN text,FN text,MN text,DOBDay int, DOBMonth int, DOBYear int,RN1 int,SPN text, Notes text,Qar_id int, RS_id int,Gender int, FOREIGN KEY (Qar_id) REFERENCES Qar(Qar_id),FOREIGN KEY (RS_id) REFERENCES RS(RS_id) )');
         for Qar_RS in tuples_Qar_RS[:]: #1667
             if Qar_RS[2] == Qa[0]:
                 for Gender in Ge[:]:
                    i=1;j=1;
                    #print((Mou[0],Qa[0],Qar_RS[0],Gender,Qar_RS[1],'1',str(i)))
                    aa=get_v(Mou[0],Qa[0],Qar_RS[0],Gender,Qar_RS[1],'1',str(i))
                    while aa['error'] =='1': # or aa['success']==False
                     i+=1;
                     aa = get_v(Mou[0],Qa[0],Qar_RS[0],Gender,Qar_RS[1],'1', str(i))
                     if i==100:
                         print("error1-nodata"+str(Qar_RS)+str(Gender)); break
                    if i != 100:
                        curr=1;
                        while curr <=aa['data']['TotalPages']:
                         print('?')
                         a = get_v(Mou[0],Qa[0],Qar_RS[0],Gender,Qar_RS[1],str(j), str(i))
                         if a['error'] != '1':
                             print(str(len(a['data']['VL'])) + "loaded")
                             for l in a['data']['VL']:

                                 tuples_VL.append([l['FN'],l['LN'],l['FN'],l['MN'],l['DOBDay'],l['DOBMonth'],l['DOBYear'],l['RN1'],l['SPN'],l['Notes'],Qar_RS[0],Qar_RS[1],Gender])
                                 cursor.execute("INSERT INTO  VL_"+str(Qa[0])+" VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                                    [l['FN'],l['LN'],l['FN'],l['MN'],l['DOBDay'],l['DOBMonth'],l['DOBYear'],l['RN1'],l['SPN'],l['Notes'],Qar_RS[0],Qar_RS[1],Gender]);
                                 connection.commit();
                                 curr=a['data']['CurrentPage'];
                         else: print("error2"+str(Qar_RS)+str(Gender))
                         j+=1;
                         if curr==aa['data']['TotalPages']:
                             print("full"+str(Qar_RS)+str(Gender)); break
                         if j >= curr + 100:
                             print(str(j) + "error3" + str(Qar_RS) + str(Gender));
                             break

# cursor.executemany("INSERT INTO VL VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", tuples_VL);
# connection.commit();
connection.close()
print("end");#debug

# b=[];
# for l in aa['data']['VL']:
#     b.append([l['FN'],l['LN']])


# for Mou in tuples_Mou[:1]:
#     for Qa in tuples_Qa[:1]:
#         for Qar_RS in tuples_Qar_RS[:1]:
#             for Gender in Ge:
#                 RN = 1;
#                 while 1:
#                  tmp=get_v(Mou[0], Qa[0], Qar_RS[0], Gender, Qar_RS[1], RN)
#                  RN+=1;
#                  if tmp['success']==1 and tmp['error']=='':
#                     c=1;
#                     tuples_VL.extend((tmp['data']['VL']))
#                     if tmp['data']['CurrentPage']==tmp['data']['TotalPages']:
#                         break;
#                     elif tmp['data']['VL'][-1]['RN1']+100<RN:
#                         break
#                  else: c+=1;
#                  if c==100:
#                      break
