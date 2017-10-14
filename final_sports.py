# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 20:38:27 2016

@author: ASUS_PC
"""

#Import Necessary Modules
from bs4 import BeautifulSoup
import urllib
from re import findall

#Open the File which contains the websites
with open('C:/Users\ASUS-PC\Desktop\websites.txt') as w:
    web = w.readlines()
    
#Create a list 'webs' which stores the names of all the websites
webs = [web.rstrip('\n') for web in open('C:/Users\ASUS-PC\Desktop\websites.txt')]
webs=[x for x in webs if x!='']

#Open the File which contains the exceptions of certain websites
with open('C:/Users\ASUS-PC\Desktop\exceptions.txt') as e:
    excp = e.readlines()

#Create a list 'excp' which stores the names of all the exceptional websites
excp = [excp.rstrip('\n') for excp in open('C:/Users\ASUS-PC\Desktop\exceptions.txt')]

#Loops to change invalid websites to valid websites
for i in range(len(webs)):
    if(webs[i][0:3]=="www"):
        webs[i]="http://"+webs[i]

for i in range(len(webs)):
    if(webs[i][0:4]!="http"):
        webs[i]="http://"+webs[i]

#Loops to change exceptional websites to match input websites
for i in range(len(excp)):
    if(excp[i][0:3]=="www"):
        excp[i]="http://"+excp[i]

for i in range(len(excp)):
    if(excp[i][0:4]!="http"):
        excp[i]="http://"+excp[i]

flag=0

#Loop to get source code of every website line by line
for windex in range(len(webs)):
    try:
        r = urllib.request.urlopen(webs[windex]).read()
        soup = BeautifulSoup(r,"lxml")
        text = soup.decode()
        flag1=0
    #exception to get invalid websites or strings
    except(ConnectionResetError,urllib.request.URLError):
        print("Invalid Website")
    
    else:
        #Loop to check whether the given website is exception or not
        for eindex in range(len(excp)):
            if (webs[windex]==excp[eindex]):
                print("NA")
                flag1=1
                break
            
        if(flag1!=1):
            #Open the File sports.txt which contains the names of different sports
            with open('C:/Users\ASUS-PC\Desktop\sports.txt') as f:
                lines = f.readlines()
         
            #lines is a list which stores the names of all the sports
            lines = [line.rstrip('\n') for line in open('C:/Users\ASUS-PC\Desktop\sports.txt')]
            
            #Use regular expressions to predict whether the particular website is sports oriented or not
            for index in range(len(lines)):
               dataCrop = findall(lines[index], text)
               if len(dataCrop) != 0:
                 print(lines[index])
                 flag=1
                 break
                   
            if (flag!=1):
                print("NA")
