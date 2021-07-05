from odbAccess import *
from abaqus import *
from abaqusConstants import *
from jobMessage import *
import numpy as np
import time
import sys
import shutil,os

import section
import xyPlot

NewModelName='CBT_HU_Test-0'
odb = session.odbs['%s.odb'%NewModelName]
xy1 = xyPlot.XYDataFromHistory(odb=odb, 
        outputVariableName='Reaction force: RF1 PI: rootAssembly Node 3 in NSET RP_CBT_L', 
        steps=('Step-1', ), suppressQuery=True, __linkedVpName__='Viewport: 1')
xy2 = xyPlot.XYDataFromHistory(odb=odb, 
        outputVariableName='Reaction force: RF2 PI: rootAssembly Node 3 in NSET RP_CBT_L', 
        steps=('Step-1', ), suppressQuery=True, __linkedVpName__='Viewport: 1')
xy3 = xyPlot.XYDataFromHistory(odb=odb, 
        outputVariableName='Reaction force: RF3 PI: rootAssembly Node 3 in NSET RP_CBT_L', 
        steps=('Step-1', ), suppressQuery=True, __linkedVpName__='Viewport: 1')
Total_Time = len(xy1)
Time = []
PulloutForce = []
for t in range(Total_Time)[10:]:
    Time.append(xy1[t][0])
    F1 = xy1[t][1]
    F2 = xy2[t][1]
    F3 = xy3[t][1]
    PulloutForce.append(sqrt(F1 * F1 + F2 * F2 + F3 * F3))
MaxForce=max(PulloutForce)
print ('The PulloutForce of %s : %f'%(NewModelName,MaxForce))