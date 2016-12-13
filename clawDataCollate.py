# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 13:55:07 2016

@author: Caran
"""

import os
import glob
import io 
FGOHeroData = "FGOHeroData.csv"
FGOMaterialData = "FGOMaterial.csv"
files = glob.glob("D:/Caran/Download/python/phantomjs-2.1.1-windows/bin/" + "*.csv")
files.sort()

#1. title
hdFile = io.open(FGOHeroData, 'w', encoding = 'utf-8')
hdFile.write("hero,type,level,material,num\n".decode('utf-8'))
hdFile.flush()
hdFile.close()

#2. combine
for f in files:
    filename = os.path.split(f)
    if filename[1] == "FGOHero.csv":
        continue
    if filename[1] == "FGOHeroData.csv":
        continue
    
    hdFile = io.open(FGOHeroData, 'a', encoding = 'utf-8')
    fFile = io.open(f, 'r', encoding = 'utf-8')
    fdata = fFile.read()
    hdFile.write(fdata)
    hdFile.flush()
    hdFile.close()
    fFile.close()

print 'combine finish'

#3. replace
mdFile = io.open(FGOMaterialData, 'r', encoding = 'utf-8')
md = mdFile.readlines()
mdFile.close()

hdFile = io.open(FGOHeroData, 'r', encoding = 'utf-8')
hdata = hdFile.read()
hdFile.close()

hdFileNew = io.open("FGOHeroDataNew.csv", 'w', encoding = 'utf-8')
for l in md:
    litem = l.split(',')
    hdata = hdata.replace(litem[1], litem[0])

hdFileNew.write(hdata)    
hdFileNew.flush()
hdFileNew.close()
    
print 'replace finish'
