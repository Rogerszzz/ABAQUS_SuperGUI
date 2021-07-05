from odbAccess import *
from abaqus import *
from abaqusConstants import *
from jobMessage import *
import numpy as np
import time
import sys
import shutil,os
import random
import mesh
ModelName='CBT_HU_Test-0'
myModel=mdb.models[ModelName]
myPart=myModel.parts['PART-1']
MatNum = 10
Eleset = {}

SetRegion=["CBT-POST","CBT-CAN","CBT-COR","CBT-END"]
Elastic=[600,20,2000,200]
Possion=[0.3,0.25,0.3,0.4]
Plastic11=[0.05,0.01,2,0.4]
Plastic12=[0.0,0.0,0.0,0.0]
Plastic21=[0.50,0.38,30,1.5]
Plastic22=[0.003,0.0029,0.0003,0.0004]
Density=[2.1e-10,7.2e-11,3.4e-10,2.8e-10]
ShearDamage=[0.012,0.012,0.008,0.015]

for RegNum in range(len(SetRegion)):
    Reg=SetRegion[RegNum]
    mySet=myPart.sets[Reg]
    Reset_element=mySet.elements
    v_Elastic=Elastic[RegNum]
    v_Possion=Possion[RegNum]
    v_Plastic11=Plastic11[RegNum]
    v_Plastic12=Plastic12[RegNum]
    V_Plastic21=Plastic21[RegNum]
    v_Plastic22=Plastic22[RegNum]
    v_Density=Density[RegNum]
    v_SDamage=ShearDamage[RegNum]
    for number in range(1,MatNum+1):
        setName = "%s-{}".format(number)%Reg
        myElement = mySet.elements[number-1:number]
        Eleset[setName]=[]
    for element in Reset_element:
        r_Num = random.randint(1,MatNum)
        r_SetName="%s-{}".format(r_Num)%Reg
        Eleset[r_SetName].append(element)    
    for number in range(1,MatNum+1):
        materialName = "%s-{}".format(number)%Reg
        sectionName = "%s-{}".format(number)%Reg
        setName = "%s-{}".format(number)%Reg
        myModel.Material(name=materialName)
        myMaterial=myModel.materials[materialName]
        myMaterial.Elastic(table=((v_Elastic*number, v_Possion), ))
        myMaterial.Plastic(table=((v_Plastic11*number, v_Plastic12), (V_Plastic21*number, v_Plastic22*number)))
        myMaterial.Density(table=((v_Density*number, ), ))
        myMaterial.ShearDamageInitiation(ks=1.0, table=((v_SDamage, 0.0, 0.0), ))
        myMaterial.shearDamageInitiation.DamageEvolution(type=DISPLACEMENT, table=((0.001, ), ))
        MEle=mesh.MeshElementArray(Eleset[setName])
        myPart.Set(elements=MEle,name=setName)
        myModel.HomogeneousSolidSection(name=sectionName,material=materialName,thickness=None)
        myPart.SectionAssignment(region=myPart.sets[setName],sectionName=sectionName,offset=0.0,offsetType=MIDDLE_SURFACE,offsetField='',thicknessAssignment=FROM_SECTION)