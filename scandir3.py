# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 01:20:15 2020

@author: plini
"""


from os import scandir
import pandas as pd
from os.path import exists,split,join
from collections import OrderedDict
import os


# Retorna arvore de arquivos no path escolhido (local)
def scantree(path):
    print('scantree(path)')
    """Recursively yield DirEntry objects for given directory."""
    for entry in scandir(path):
        if entry.is_dir(follow_symlinks=False):
            for entry in scantree(entry.path):
                yield entry # see below for Python 2.x
        else:
            yield entry

local_folder = os.path.split(os.getcwd())[0]
#local_folder = r"d:\onedrive"
local_folder = os.getcwd()
localfiles = pd.DataFrame()



#%%

if exists(local_folder): 
    local = []
    for aux in scantree(local_folder):
        local.append(aux) 
        
        
    dic = OrderedDict()
    dic['filename'] = list(map(lambda x: x.name,local))
    
    dic['modificado'] = list(map(lambda x: x.stat().st_mtime,local))
    dic['acessado'] = list(map(lambda x: x.stat().st_atime,local))
    
    dic['modificado'] = pd.to_datetime(list(map(lambda x: x.stat().st_mtime,local)),unit='s')
    dic['modificado'] = list(map(lambda x: x.replace(microsecond = 0),dic['modificado']))
    
    dic['acessado'] = pd.to_datetime(list(map(lambda x: x.stat().st_atime,local)),unit='s')
    dic['acessado'] = list(map(lambda x: x.replace(microsecond = 0),dic['acessado']))
    
    
    dic['tamanho'] = list(map(lambda x: x.stat().st_size,local))
    dic['relpath'] = list(map(lambda x: x.path.replace(local_folder,'').replace('\\','/').lstrip('/'),local))
    dic['dirpath'] = list(map(lambda x: split(x)[0],dic['relpath']))
    
    dic['fullpath'] = list(map(lambda x: join(local_folder,x.path.replace(local_folder,'').replace('\\','/').lstrip('/')),local))
    
    dfl = pd.DataFrame(dic,index= dic['relpath'])                    
    
#%% Renomeando arquivos

