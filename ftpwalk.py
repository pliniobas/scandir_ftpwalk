# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 23:52:46 2019

@author: plinio.silva
"""

from ftplib import FTP
#import sys
import pandas as pd
import re
#import os
#import numpy as np
from os.path import basename,realpath,dirname,split,splitext,join,getctime,getatime,getmtime,getsize,exists
#import time
#from scandir import scandir
#from collections import OrderedDict


username='*******'
password='*******'

def ftpwalk(ftp,folder,df):
    
    ls = []
    print('folder',folder)
    if len(folder):
        ftp.cwd('/')
        ftp.cwd(folder)
    ftp.retrlines('MLSD',ls.append)
    
    
    #ls = ls[-10:]
    for aux in ls:
        name = (folder + '/' + aux.split(';')[-1].strip(" "))
        df.loc[name,'type'] =  re.findall('type=([\w]+)',aux)[0]
        df.loc[name,'modify'] = pd.datetime.strptime((re.findall('modify=([\w]+)',aux)[0]),'%Y%m%d%H%M%S')
        df.loc[name,'folder'] = folder
        df.loc[name,'filename'] = basename(name)
        try:
            df.loc[name,'size'] = np.long(re.findall('size=([\w]+)',aux)[0])
        except:
#            print('Pasta detectada, pulando criacao de size %s'%aux)
            pass
        if df.loc[name,'type'] == 'dir':
            df.append(ftpwalk(ftp,name,df))
            pass
        pass
    
    df.loc[:,'full_path'] = df.index 
    pass


ftp = FTP()
ftp.connect("ftp.metocean.com")
ftp.login(user=username,passwd=password)
folder = ''


folder_list = [] #Regula a quantidade de dias que serao revistos no servidor
for aux in range(0,8,1):
    folder_list.append( (pd.datetime.today() - pd.Timedelta(days = aux)).strftime('/%Y-%m-%d') )
    

df = pd.DataFrame()
for aux in folder_list:
    ftpwalk(ftp,aux,df) 

