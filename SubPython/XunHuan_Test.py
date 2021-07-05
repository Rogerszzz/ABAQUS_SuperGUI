from odbAccess import *
from abaqus import *
from abaqusConstants import *
from jobMessage import *
import numpy as np
import time
import sys
import shutil,os
print('**************')
print('The Test Begins')
N = 0
NewjobName='XunHuan-%o'%N
shutil.copy("XunHuan.inp","%s.inp"%NewjobName)
mdb.JobFromInputFile(name=NewjobName, 
    inputFileName='H:\\pan\\Test\\XunHuan_Test\\XunHuan.inp', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, 
    userSubroutine='', scratch='H:\\pan\\Temp', resultsFormat=ODB, 
    multiprocessingMode=DEFAULT, numCpus=12, numDomains=12, numGPUs=0)
while os.path.isfile('%s.lck'%NewjobName) == True:
    os.remove('%s.lck'%NewjobName)
    time.sleep(1)
mdb.jobs[NewjobName].submit(consistencyChecking=OFF)
print('Submitted successfully')
mdb.jobs[NewjobName].waitForCompletion()
time.sleep(1)
print('The cycle-%o calculation is completed'%N)
print('Start the cycle')
while 1:
    stafile=open('%s.log'%NewjobName,'r')
    lastline=stafile.readlines()[-1]
    stafile.close()
    Completed_flag='COMPLETED'in lastline
    Error_flag='errors'in lastline
    print('Running')
    if Error_flag:
        print('Abaqus/Analysis exited with errors')
        break
    if Completed_flag:
        print('Abaqus JOB COMPLETED')
        break
    time.sleep(10)
inpfile=open('%s.inp'%NewjobName)
if(N<10):
    OldjobName='XunHuan-%o'%N
    N=N+1
    NewjobName='XunHuan-%o'%N
    shutil.copy("%s.inp"%OldjobName,"%s.inp"%NewjobName)
    while os.path.isfile('%s.lck'%NewjobName) == True:
        del inpfile
        del mdb.jobs['%s.lck'%NewjobName]
    odb=openOdb(path='%s.odb'%OldjobName)
    Ass=odb.rootAssembly
    Instance=Ass.instances['PART-1-1']
    U_dispFile=open('Data_U.dat','w')
    inpfile=open('%s.inp'%OldjobName)
    lines=inpfile.readlines()
    inpfile.close()
    originstr='*Part, name=PART-1\n'
    strindex=lines.index(originstr)
    step1=odb.steps['Step-2']
    lastframe=step1.frames[-1]
    displaces=lastframe.fieldOutputs["U"]
    u_val=displaces.getSubset(region=Ass.nodeSets[' ALL NODES']).values
    print('Current number of cycles:%o,Obtain u_val'%N)
    odb.close()
    N0 = 0
    for u in u_val:
        u_nodeLabel = u.nodeLabel
        u_coordinates = Instance.getNodeFromLabel(u.nodeLabel).coordinates
        u_data = u.data
        NewU=(u_nodeLabel,u_data[0]+u_coordinates[0],u_data[1]+u_coordinates[1],u_data[2]+u_coordinates[2])
        (nodeLabel,U1,U2,U3)=NewU
        if (N0>3):
            lines[strindex+N0-2]='%d,%10.8E,%10.8E,%10.8E\n'%(nodeLabel,U1,U2,U3)
        N0=N0+1
    newfile=open('%s.inp'%NewjobName,'w')
    for newline in lines:
        newfile.write(newline)
    newfile.close
    mdb.JobFromInputFile(name=NewjobName, 
            inputFileName='H:\\pan\\Test\\XunHuan_Test\\%s.inp'%OldjobName, type=ANALYSIS, 
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, 
            userSubroutine='', scratch='H:\\pan\\Temp', resultsFormat=ODB, 
            multiprocessingMode=DEFAULT, numCpus=12, numDomains=12, numGPUs=0)
    while os.path.isfile('%s.lck'%NewjobName) == True:
        os.remove('%s.lck'%NewjobName)
        time.sleep(1)
    mdb.jobs[NewjobName].submit(consistencyChecking=OFF)
    print('Current number of cycles:%o,Submitted successfully'%N)
    mdb.jobs[NewjobName].waitForCompletion()
    time.sleep(1)
    print('The cycle-%o calculation is completed'%N)
print('Test complete')
print('*********')