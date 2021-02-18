# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 18:13:28 2021

@author: plini
"""

    

import shutil

newplace = r'C:\Users\plini\Desktop\new'

count = 0
filenamebuffer = ''
error = []
for aux in dfl.index:
    if filenamebuffer != dfl.at[aux,'dirpath']:
        count = 0
        filenamebuffer = dfl.at[aux,'dirpath']
    count = count + 1
    newname = dfl.at[aux,'dirpath']
    ###
    if len(newname.split('/')) > 1:
        newname = newname.split('/')[0]
    ###
    newname = newname +' '+ ("%d"%count).zfill(4) + '.jpg'
    newname = newname.replace('&','and')

    newfile = os.path.join(newplace,newname)
    oldfile = dfl.at[aux,'fullpath']
    try:
        shutil.copy(oldfile,newfile)
    except Exception as e:
        print(e)
        print(oldfile)
        error.append(oldfile)
        # break


