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

#Button(root, text="Quit", command=root.destroy).pack()
#root.mainloop()

root.withdraw()
file_path=filedialog.askopenfilename()
root.destroy()

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
        print(llm)
        word=worksheet.cell(29, 4).value
        if word not in Strain:
            Strain.append(word)
#    import pdb; pdb.set_trace()
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
    print(Means)
    print(error)
x_pos = np.arange(Leng)

# Build the plot
fig, ax = plt.subplots()
ax.bar(x_pos, Means,
       yerr=error,
       align='center',
       alpha=0.5,
       ecolor='black',
       capsize=10)
ax.set_ylabel('Touch Response')
ax.set_xticks(x_pos)
ax.set_xticklabels(Strain)
ax.set_title('Touch Assay')
ax.yaxis.grid(True)

#Save the figure and show
plt.tight_layout()
plt.savefig(str(fileName) +'.tiff', dpi=600)
plt.show()