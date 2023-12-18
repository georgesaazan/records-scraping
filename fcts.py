import requests
import sqlite3
import json
from requests.structures import CaseInsensitiveDict
url = "#########################################"
headers = CaseInsensitiveDict()
headers["Host"] = "###############"
headers["User-Agent"] = "Fiddler"
headers["Accept"] = "*/*Accept-Language: en-US,en;q=0.5"
headers["Accept-Encoding"] = "gzip, deflate, br"
headers["Referer"] = "##########################################"
headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["X-Requested-With"] = "XMLHttpRequest"
headers["Content-Length"] = "494"
headers["Origin"] = "#######################"
headers["Connection"] = "keep-alive"
headers["Cookie"] = "###############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################"
headers["Pragma"] = "no-cache"
headers["Cache-Control"] = "no-cache"
def get_region(type,parent_id):
 data = "##################################################################################################################################################################################"+type+"&Parent="+parent_id+""
 resp = requests.post(url, headers=headers, data=data)
 # result=resp.content.decode('unicode-escape').encode('latin1').decode('utf-8');
 return resp.json()


def get_Mou():
 data = "##################################################################################################################################################################################&Type=Mou"
 resp = requests.post(url, headers=headers, data=data)
 return resp.json()

def get_RS(parent_id):
 url = "############################################"
 data = "##################################################################################################################################################################################&Qar="+parent_id+""
 resp = requests.post(url, headers=headers, data=data)
 return resp.json()

def get_v(Mou,Qa,Qar,Ge,RS,CurrentPage,RN):
 url = "###################################"
 data = "##################################################################################################################################################################################&obj={\"PageSize\":##,\"CurrentPage\":"+CurrentPage+",\"SearchMode\":2,\"HtmlTemplate\":\"/templates/vsResultMultiple.html\",\"##########\":\"" + Mou + "\",\"#####\":\"" + Qa + "\",\"#####\":\"" + Qar + "\",\"######\":\"" + Ge + "\",\"############\":\"" + RS + "\",\"##############\":\"" + RN +"\"}&=";
 resp = requests.post(url, headers=headers, data=data)

 return resp.json()
 #return resp.content.decode('unicode-escape').encode('latin1').decode('utf-8');
