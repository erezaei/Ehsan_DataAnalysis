#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 10:43:42 2019

@author: erezaei
"""
import tkinter as tk
from tkinter import filedialog
#from tkinter import Button
import os
import numpy as np
from numpy import matlib
import matplotlib.pyplot as plt
import xlrd

root=tk.Tk()

filez = filedialog.askopenfilenames(parent=root,title='Choose a file')
root.withdraw()
root.destroy()
lenfilez=len(filez)
for filnum in range(0,lenfilez):
    
    file_path=filez[filnum]
  
    
    filename_w_ext = os.path.basename(file_path)
    fileName, file_extension = os.path.splitext(filename_w_ext)
    workbook = xlrd.open_workbook(file_path)
    Strain=[]
    Means=[]
    error=[]
    labels=[] 

    for llm in range(0,12):
        worksheet = workbook.sheet_by_index(llm)
        Datee=worksheet.cell(29, 0).value
        
        if Datee:
            #print(llm)
            word=worksheet.cell(29, 4).value
            if word not in Strain:
                Strain.append(word)
              #  import pdb; pdb.set_trace()
    SumMat=np.matlib.zeros((75, len(Strain))) 
    
    for jj in range(0,12):
        worksheet = workbook.sheet_by_index(jj)
        Datee=worksheet.cell(29, 0).value
        if Datee:
            Sumi=np.matlib.zeros((25,1)) 
            word=worksheet.cell(29, 4).value
            index = Strain.index(word)    
            for Trail in range(0,25):
                Ssam=np.matlib.zeros((1,10)) 
                for Touch in range(0,10):
                    Touch_Add=worksheet.cell(Trail+1, Touch+1).value
                    if Touch_Add== '':
                        Touch_Add=0
                    Ssam[0,Touch]=Touch_Add
                TrailSum=np.sum(Ssam)    
                Sumi[Trail,0]=TrailSum 
                
           # FirsZer=np.argwhere(SumMat[:,index] == 0)[0,0]
            Varib1=np.sum(SumMat[0:25,index]) 
            Varib2=np.sum(SumMat[25:50,index]) 
            Varib3=np.sum(SumMat[50:75,index])
            
            if Varib1 == 0 :
                SumMat[0:25,index]=Sumi 
        
            elif (Varib2==0 and Varib1 > 0): 
                SumMat[25:50,index]=Sumi
                
            elif (Varib3==0 and Varib1>0 and Varib2>0):  
                SumMat[50:75,index]=Sumi    
            
# Calculate the average and the standard deviation
    Leng=len(np.squeeze(np.asarray(SumMat[1,:])))
    for i in range(0,Leng):
        Means.append(np.mean(SumMat[:,i]))
        error.append(np.std(SumMat[:,i]))   
    
## Build the Group Barchart
    if filnum==0:
        fig, ax = plt.subplots()
    
    ind = np.arange(Leng)    # the x locations for the groups
    width =0.25         # the width of the bars
    Loc=0.75+ind+((lenfilez-1)/2*filnum)*width

    p = ax.bar(Loc, Means, width, bottom=0, yerr=error)
    
ax.set_ylabel('Touch Response')
ax.set_xticks(ind+1 )
ax.set_xticklabels((Strain))
ax.set_title('Touch Assay')
#ax.yaxis.grid(True)
ax.legend(('Day 4', 'Day 8','Day 12'))


#Save the figure and show
plt.tight_layout()
plt.savefig(str(fileName) +'.tiff', dpi=600)
plt.show()