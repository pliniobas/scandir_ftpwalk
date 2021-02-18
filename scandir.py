from scandir import scandir
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

localfiles = pd.DataFrame()
if exists(local_folder): 
    local = []
    for aux in scantree(local_folder):
        local.append(aux) 
        
        
    dic = OrderedDict()
    dic['filename'] = map(lambda x: x.name,local)
    
    dic['modificado'] = map(lambda x: x.stat().st_mtime,local)
    dic['acessado'] = map(lambda x: x.stat().st_atime,local)
    
    dic['modificado'] = pd.to_datetime(map(lambda x: x.stat().st_mtime,local),unit='s')
    dic['modificado'] = map(lambda x: x.replace(microsecond = 0),dic['modificado'])
    
    dic['acessado'] = pd.to_datetime(map(lambda x: x.stat().st_atime,local),unit='s')
    dic['acessado'] = map(lambda x: x.replace(microsecond = 0),dic['acessado'])
    
    
    dic['tamanho'] = map(lambda x: x.stat().st_size,local)
    dic['relpath'] = map(lambda x: x.path.replace(local_folder,'').replace('\\','/').lstrip('/'),local)
    dic['dirpath'] = map(lambda x: split(x)[0],dic['relpath'])
    
    dic['fullpath'] = map(lambda x: join(local_folder,x.path.replace(local_folder,'').replace('\\','/').lstrip('/')),local)
    
    dfl = pd.DataFrame(dic,index= dic['relpath'])                    

