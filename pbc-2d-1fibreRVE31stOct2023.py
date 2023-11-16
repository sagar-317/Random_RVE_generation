# Script to apply PBC on comformal 2D mesh
    # Change the model name and part name as per the cae
    # Change the inpur parameter of getByBoundingBox to select the particular edges/nodes/faces
    # Change the coordinates of ReferencePoint
    # Here set 2 is variable, you can fix it by assigning with reference to vertices every time
    # Also, in the reference point based code, create step-1
    
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

import numpy as np

session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)
Model_Name='Model-1'
partname='Part-1'

side = 105.0
lx = side
ly = side
exx = 0.0
exy = 1
eyx = 0.5
eyy = 0.0
d1 = exx*lx
d2 = eyy*ly
d3 = exy*lx
d4 = exy*ly

a = mdb.models['Model-1'].rootAssembly
a.ReferencePoint(point=(side+side/3, side/2, 0))
ref = mdb.models['Model-1'].rootAssembly.features['RP-1']
i=ref.id
a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[i], )
a.Set(referencePoints=refPoints1, name='Set-RP-1')

a = mdb.models['Model-1'].rootAssembly
a.ReferencePoint(point=(side/2, side+side/3, 0))
ref = mdb.models['Model-1'].rootAssembly.features['RP-2']
i=ref.id
a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[i], )
a.Set(referencePoints=refPoints1, name='Set-RP-2')

a = mdb.models['Model-1'].rootAssembly
a.ReferencePoint(point=(side+side/3, side, 0))
ref = mdb.models['Model-1'].rootAssembly.features['RP-3']
i=ref.id
a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[i], )
a.Set(referencePoints=refPoints1, name='Set-RP-3')

a = mdb.models['Model-1'].rootAssembly
a.ReferencePoint(point=(side, side+side/3, 0))
ref = mdb.models['Model-1'].rootAssembly.features['RP-4']
i=ref.id
a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[i], )
a.Set(referencePoints=refPoints1, name='Set-RP-4')

p = mdb.models[Model_Name].parts['Part-1']
n = p.nodes
# define edge sets
NodesEdgeAB = n.getByBoundingBox(-1e-3,1e-3,-1e-3,
                                  1e-3,side-1e-3,1e-3)
p.Set(nodes=NodesEdgeAB, name='SetEgdeAB')

NodesEdgeDC = n.getByBoundingBox(side-1e-3,1e-3,-1e-3,
                                 side+1e-3,side-1e-3,1e-3)
p.Set(nodes=NodesEdgeDC, name='SetEgdeDC')

NodesEdgeAD = n.getByBoundingBox(1e-3,    -1e-3,-1e-3,
                                 side-1e-3,1e-3,1e-3)
p.Set(nodes=NodesEdgeAD, name='SetEgdeAD')

NodesEdgeBC = n.getByBoundingBox(1e-3,     side-1e-3,-1e-3,
                                 side-1e-3,side+1e-3,1e-3)
p.Set(nodes=NodesEdgeBC, name='SetEgdeBC')

NodesVertA = n.getByBoundingBox(-1e-3,-1e-3,-1e-3,
                                 1e-3,1e-3,1e-3)
p.Set(nodes=NodesVertA, name='SetVertA')

NodesVertD = n.getByBoundingBox(side-1e-3,-1e-3,-1e-3,
                                side+1e-3,1e-3,1e-3)
p.Set(nodes=NodesVertD, name='SetVertD')

NodesVertC = n.getByBoundingBox(side-1e-3,side-1e-3,-1e-3,
                                side+1e-3,side+1e-3,1e-3)
p.Set(nodes=NodesVertC, name='SetVertC')

NodesVertB = n.getByBoundingBox(-1e-3,side-1e-3,-1e-3,
                                 1e-3,side+1e-3, 1e-3)
p.Set(nodes=NodesVertB, name='SetVertB')


# a = mdb.models[Model_Name].rootAssembly
# a.ReferencePoint(point=(0,50,0))
# ref = mdb.models[Model_Name].rootAssembly.features['RP-1']
# i=ref.id
# a = mdb.models[Model_Name].rootAssembly
# r1 = a.referencePoints
# refPoints1=(r1[i], )
# a.Set(referencePoints=refPoints1, name='Set-RP-1')

# a = mdb.models[Model_Name].rootAssembly
# a.ReferencePoint(point=(50,0,0))
# ref = mdb.models[Model_Name].rootAssembly.features['RP-2']
# i=ref.id
# a = mdb.models[Model_Name].rootAssembly
# r1 = a.referencePoints
# refPoints1=(r1[i], )
# a.Set(referencePoints=refPoints1, name='Set-RP-2')


def Create_Set_Edges_Y(Model_Name,partname,NodesEdgeName,edgesetname):
    TempCoordinates=[]
    Coordinates=[]
    length1=len(NodesEdgeName)	
    #
        
    for i in range(length1):
        TempCoordinates.append(NodesEdgeName[i].coordinates[1])
        Coordinates.append(NodesEdgeName[i].coordinates[1])	
    #
    
    
    for i in range(0,length1):
        for j in range(length1-1,i,-1):
            if TempCoordinates[j] < TempCoordinates[j-1]:
                temp=TempCoordinates[j-1]
                TempCoordinates[j-1]=TempCoordinates[j]
                TempCoordinates[j]=temp		
    #
    
    
    for i in range(0,length1):
        for j in range(0,length1):
            if abs(TempCoordinates[i] - Coordinates[j])<10e-5:
                k=i+1
                setname= edgesetname+'-'+str(k)
                a=mdb.models[Model_Name]
                Node = a.parts[partname].nodes
                label1=NodesEdgeName[j].label-1
                node=NodesEdgeName[0:0]
                node=(Node[label1:label1+1],)
                a=mdb.models[Model_Name].parts[partname]
                a.Set(nodes=node, name=setname)	
#

def Create_Set_Edges_X(Model_Name,partname,NodesEdgeName,edgesetname):
    TempCoordinates=[]
    Coordinates=[]
    length1=len(NodesEdgeName)	
    #
    
    
    for i in range(length1):
        TempCoordinates.append(NodesEdgeName[i].coordinates[0])
        Coordinates.append(NodesEdgeName[i].coordinates[0])	
    #
    
    
    for i in range(0,length1):
        for j in range(length1-1,i,-1):
            if TempCoordinates[j] < TempCoordinates[j-1]:
                temp=TempCoordinates[j-1]
                TempCoordinates[j-1]=TempCoordinates[j]
                TempCoordinates[j]=temp		
    #
    
    
    for i in range(0,length1):
        for j in range(0,length1):
            if abs(TempCoordinates[i] - Coordinates[j])<10e-5:
                k=i+1
                setname= edgesetname+'-'+str(k)
                a=mdb.models[Model_Name]
                Node = a.parts[partname].nodes
                label1=NodesEdgeName[j].label-1
                node=NodesEdgeName[0:0]
                node=(Node[label1:label1+1],)
                a=mdb.models[Model_Name].parts[partname]
                a.Set(nodes=node, name=setname)	
#

Create_Set_Edges_Y('Model-1','Part-1',NodesEdgeAB,'EdgeAB')
Create_Set_Edges_X('Model-1','Part-1',NodesEdgeBC,'EdgeBC')
Create_Set_Edges_Y('Model-1','Part-1',NodesEdgeDC,'EdgeDC')
Create_Set_Edges_X('Model-1','Part-1',NodesEdgeAD,'EdgeAD')
# RVE STRUCTURE
                    # B-----------------C
                    # |                 |
                    # |                 |
                    # |                 |
                    # |                 |
                    # |                 |
                    # A-----------------D


length1=len(NodesEdgeAB)
for i in range(length1):
	k=i+1
        pfconstraintname='Constraint-Edge-AB-PF-'+str(k)
        yconstraintname='Constraint-Edge-AB-Y-'  +str(k)
    	xconstraintname='Constraint-Edge-AB-X-'  +str(k)
	Set1='Part-1-1.EdgeAB-'+str(k)
	Set2='Part-1-1.EdgeDC-'+str(k)
	mdb.models[Model_Name].Equation(name=xconstraintname, 
        terms=((1.0, Set1, 1), (-1.0, Set2, 1), (1.0, 'Set-RP-1', 1)))
	mdb.models[Model_Name].Equation(name=yconstraintname, 
        terms=((1.0, Set1, 2), (-1.0, Set2, 2), (1.0, 'Set-RP-3', 2)))
	mdb.models[Model_Name].Equation(name=pfconstraintname, 
        terms=((1.0, Set1, 11), (-1.0, Set2, 11), (-1.0, 'Part-1-1.SetVertA', 11), (1.0, 'Part-1-1.SetVertD', 11)))	

length1=len(NodesEdgeAD)
for i in range(length1):
	k=i+1
        pfconstraintname='Constraint-Edge-AD-PF-'+str(k)
    	yconstraintname='Constraint-Edge-AD-Y-'+str(k)
    	xconstraintname='Constraint-Edge-AD-X-'+str(k)
	Set1='Part-1-1.EdgeAD-'+str(k)
	Set2='Part-1-1.EdgeBC-'+str(k)
	mdb.models[Model_Name].Equation(name=xconstraintname, 
        terms=((1.0, Set1, 1), (-1.0, Set2, 1), (1.0, 'Set-RP-4', 1)))
	mdb.models[Model_Name].Equation(name=yconstraintname, 
        terms=((1.0, Set1, 2), (-1.0, Set2, 2), (1.0, 'Set-RP-2', 2)))
	mdb.models[Model_Name].Equation(name=pfconstraintname, 
        terms=((1.0, Set1, 11), (-1.0, Set2, 11), (-1.0, 'Part-1-1.SetVertA', 11), (1.0, 'Part-1-1.SetVertB', 11)))

# pbs applied on the corner nodes
# this is in accordance with gAROZ, GILABERT PAPER
# Consistent application of pbc implicit and explicit
# using relative formulations
# labelling in paper is different, we have ABCD, they have ADCB
# ud_j - ua_j = ex_j*lx, where j = x,y
mdb.models[Model_Name].Equation(name='Constraint-Corners-D-A-X', 
        terms=((1.0, 'Part-1-1.SetVertD', 1), (-1.0, 'Part-1-1.SetVertA', 1), (-1.0, 'Set-RP-1', 1)))
mdb.models[Model_Name].Equation(name='Constraint-Corners-D-A-Y', 
        terms=((1.0, 'Part-1-1.SetVertD', 2), (-1.0, 'Part-1-1.SetVertA', 2), (-1.0, 'Set-RP-3', 2)))
# ub_j - ua_j = ey_j*ly, where j = x,y
mdb.models[Model_Name].Equation(name='Constraint-Corners-B-A-X', 
        terms=((1.0, 'Part-1-1.SetVertB', 1), (-1.0, 'Part-1-1.SetVertA', 1), (-1.0, 'Set-RP-4', 1)))
mdb.models[Model_Name].Equation(name='Constraint-Corners-B-A-Y', 
        terms=((1.0, 'Part-1-1.SetVertB', 2), (-1.0, 'Part-1-1.SetVertA', 2), (-1.0, 'Set-RP-2', 2)))
# uc_j - ud_j = ey_j*ly, where j = x,y
mdb.models[Model_Name].Equation(name='Constraint-Corners-C-D-X', 
        terms=((1.0, 'Part-1-1.SetVertC', 1), (-1.0, 'Part-1-1.SetVertD', 1), (-1.0, 'Set-RP-4', 1)))
mdb.models[Model_Name].Equation(name='Constraint-Corners-C-D-Y', 
        terms=((1.0, 'Part-1-1.SetVertC', 2), (-1.0, 'Part-1-1.SetVertD', 2), (-1.0, 'Set-RP-2', 2)))


# IMPLEMENTATION FROM FAN-YE PAPER - HAD SOME PROBLEMS
# mdb.models[Model_Name].Equation(name='Constraint-Corners-A-C-X', 
#         terms=((1.0, 'Part-1-1.SetVertC', 1), (-1.0, 'Part-1-1.SetVertA', 1), 
#             (-1.0, 'Set-RP-1', 1), (-1.0, 'Set-RP-4', 1)))
# mdb.models[Model_Name].Equation(name='Constraint-Corners-A-C-Y', 
#         terms=((1.0, 'Part-1-1.SetVertC', 2), (-1.0, 'Part-1-1.SetVertA', 2), 
#             (-1.0, 'Set-RP-2', 2), (-1.0, 'Set-RP-3', 2)))
# mdb.models[Model_Name].Equation(name='Constraint-Corners-B-D-X', 
#         terms=((1.0, 'Part-1-1.SetVertD', 1), (-1.0, 'Part-1-1.SetVertB', 1), 
#             (-1.0, 'Set-RP-1', 1), (1.0, 'Set-RP-4', 1)))
# mdb.models[Model_Name].Equation(name='Constraint-Corners-B-D-Y', 
#         terms=((1.0, 'Part-1-1.SetVertD', 2), (-1.0, 'Part-1-1.SetVertB', 2), 
#             (-1.0, 'Set-RP-2', 2), (-1.0, 'Set-RP-3', 2)))
# CORNER PHASE-FIELD CONSTRAINT -----------------------------------------------
# mdb.models[Model_Name].Equation(name='Constraint-Corners-C-B-D-A-PF', 
#         terms=((1.0, 'Part-1-1.SetVertC', 3), (-1.0, 'Part-1-1.SetVertD', 3), 
#             (-1.0, 'Part-1-1.SetVertB', 3), (1.0, 'Part-1-1.SetVertA', 3) ) )

a = mdb.models['Model-1'].rootAssembly
region = a.sets['Set-RP-1']
mdb.models['Model-1'].DisplacementBC(name='BC-1', createStepName='Step-1', 
    region=region, u1=d1, u2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF, 
    distributionType=UNIFORM, fieldName='', localCsys=None)

a = mdb.models['Model-1'].rootAssembly
region = a.sets['Set-RP-2']
mdb.models['Model-1'].DisplacementBC(name='BC-2', createStepName='Step-1', 
    region=region, u1=UNSET, u2=d2, ur3=UNSET, amplitude=UNSET, fixed=OFF, 
    distributionType=UNIFORM, fieldName='', localCsys=None)

a = mdb.models['Model-1'].rootAssembly
region = a.sets['Set-RP-3']
mdb.models['Model-1'].DisplacementBC(name='BC-3', createStepName='Step-1', 
    region=region, u1=UNSET, u2=d3, ur3=UNSET, amplitude=UNSET, fixed=OFF, 
    distributionType=UNIFORM, fieldName='', localCsys=None)

a = mdb.models['Model-1'].rootAssembly
region = a.sets['Set-RP-4']
mdb.models['Model-1'].DisplacementBC(name='BC-4', createStepName='Step-1', 
    region=region, u1=d4, u2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF, 
    distributionType=UNIFORM, fieldName='', localCsys=None)

# mdb.models[Model_Name].Equation(name='Vertice_3_Constraint', terms=((1.0, 'Part-1-1.SetVertB', 
		# 1), (1.0, 'Part-1-1.SetVertD', 1), (-1.0, 'Part-1-1.SetVertC', 1)))
# mdb.models[Model_Name].Equation(name='Vertice_3_Constraint', terms=((1.0, 'Part-1-1.SetVertB', 
		# 2), (1.0, 'Part-1-1.SetVertD', 2), (-1.0, 'Part-1-1.SetVertC', 2)))
#

# Ems = np.array([[0.0, 0.0],[0.0, 1/50]])


# a=mdb.models[Model_Name].rootAssembly
# region = a.sets['Set-RP-1']
# mdb.models[Model_Name].DisplacementBC(name='BC-2', createStepName='Step-1', 
    # region=region, u1=float(Ems[0,0]), u2=float(Ems[1,0]), ur1=UNSET, 
    # amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    # localCsys=None)