"""  
#******************************************************************************************************** 
RVE2DFibre Creation Script: RVE_06CircularInclusions__WindowSize_100Squared_Units_7.py  
Author: Michael Okereke  
Date:  11-May-2021
Purpose: Creates Abaqus model (RVE2DFibre) using inputs generated from MCRVEGen algorithm 
Inclusion: Creates 7 CIRCULAR Inclusions 
#******************************************************************************************************** 
"""  
# rename model as Model-1
# rename assembly instance RVE2DComposite as Part-1-1
# rename part rve2dcoposote as Part-1


#Import Abaqus-related (Python) Object files 
from abaqus import * 
from abaqusConstants import * 
import __main__ 
import section 
import regionToolset 
import displayGroupMdbToolset as dgm 
import part 
import material 
import assembly 
import step 
import interaction 
import load 
import mesh 
import job 
import sketch 
import visualization 
import xyPlot 
import displayGroupOdbToolset as dgo 
import connectorBehavior 
import numpy as np

h = 21.25e-3
w = 21.25e-3
rad = 2.1e-3
#**************************************************** 
# CREATE MATRIX AND FIBRE MATERIALS/SECTIONS HERE 
#**************************************************** 
mdb.models['Model-1'].Material(name='matrix') 
mdb.models['Model-1'].Material(name='fibre') 
mdb.models['Model-1'].HomogeneousSolidSection(name='matrixSection', material='matrix', thickness=None) 
mdb.models['Model-1'].HomogeneousSolidSection(name='fibreSection', material='fibre', thickness=None) 

#Create Viewport 
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=OFF) 
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(meshTechnique=OFF) 

s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=3*h) 
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints 
s.setPrimaryObject(option=STANDALONE) 
session.viewports['Viewport: 1'].view.setValues(width=h, height=w) 

#**************************************************** 
# REINFORCING INCLUSIONS SECTION 
#**************************************************** 

# ------------------------------------------------------------------- 
#Create Fibre circles at specified centre coordinates(XYAll) and defined radius, R 
# reading coordinates from text files-------------------------------------
# read x coordinates generated from other code

with open("RVE_Centre_Coordinate_x.txt", "r") as file:
    lines = file.readlines()
    center_x_coordinates = []
    for line in lines:
        try:
            center_x = float(line.split()[0])
            center_x_coordinates.append(center_x)
        except ValueError:
            print("Error: invalid literal for float()")
# read y coordinates generated from other code

with open("RVE_Centre_Coordinate_y.txt", "r") as file:
    lines = file.readlines()
    center_y_coordinates = []
    for line in lines:
        try:
            center_y = float(line.split()[0])
            center_y_coordinates.append(center_y)
        except ValueError:
            print("Error: invalid literal for float()")
# centers stored in the numpy arrays
# ------------------------------------------------------------------------

for j in range(0,len(center_x_coordinates)):
    s.CircleByCenterPerimeter(center=(center_x_coordinates[j], center_y_coordinates[j]), 
    point1=(center_x_coordinates[j]+rad, center_y_coordinates[j]))  
    # print(center_y_coordinates[j])



# s.CircleByCenterPerimeter(center=(43.8744, 38.1558), point1=(53.8744, 38.1558)) 
# s.CircleByCenterPerimeter(center=(76.5517, 79.52), point1=(86.5517, 79.52)) 
# s.CircleByCenterPerimeter(center=(18.6873, 48.9764), point1=(28.6873, 48.9764)) 
# s.CircleByCenterPerimeter(center=(44.5586, 64.6313), point1=(54.5586, 64.6313)) 
# s.CircleByCenterPerimeter(center=(65.5098, 16.2612), point1=(75.5098, 16.2612)) 
# s.CircleByCenterPerimeter(center=(95.9744, 34.0386), point1=(105.9744, 34.0386)) 
# s.CircleByCenterPerimeter(center=(-4.0256, 34.0386), point1=(5.9744, 34.0386)) 
# ------------------------------------------------------------------- 
 
#Name the part model and associate it 
p = mdb.models['Model-1'].Part(name='RVE2DFibre', dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY) 
p = mdb.models['Model-1'].parts['RVE2DFibre'] 
 
#Fibre Extrusion 
p.BaseShell(sketch=s) 
s.unsetPrimaryObject() 
p = mdb.models['Model-1'].parts['RVE2DFibre'] 
session.viewports['Viewport: 1'].setValues(displayedObject=p) 
del mdb.models['Model-1'].sketches['__profile__'] 
 
#**************************************************** 
# MATRIX SECTION 
#**************************************************** 

#Create Viewport 
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=OFF) 
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(meshTechnique=OFF) 

s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=3*h) 
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints 
s1.setPrimaryObject(option=STANDALONE) 
session.viewports['Viewport: 1'].view.setValues(width=w, height=h) 

#Sketch RVE Rectangle 
s1.rectangle(point1=(0.0,0.0), point2=(h, w)) 
 
#Name the part model and associate it 
p = mdb.models['Model-1'].Part(name='RVE2DMatrix', dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY) 
p = mdb.models['Model-1'].parts['RVE2DMatrix'] 
 
#Matrix Extrusion 
p.BaseShell(sketch=s1)  
s1.unsetPrimaryObject() 
p = mdb.models['Model-1'].parts['RVE2DMatrix'] 
session.viewports['Viewport: 1'].setValues(displayedObject=p) 
del mdb.models['Model-1'].sketches['__profile__'] 
 
#**************************************************** 
#ASSEMBLY INSTANCES AND MERGE THE TWO INSTANCES 
#**************************************************** 
a = mdb.models['Model-1'].rootAssembly 
a.DatumCsysByDefault(CARTESIAN) 
p = mdb.models['Model-1'].parts['RVE2DFibre'] 
a.Instance(name='RVE2DFibre-1', part=p, dependent=ON) 
p = mdb.models['Model-1'].parts['RVE2DMatrix'] 
a.Instance(name='RVE2DMatrix-1', part=p, dependent=ON) 
a = mdb.models['Model-1'].rootAssembly 
a.InstanceFromBooleanMerge(name='Part-1', instances=( 
    a.instances['RVE2DFibre-1'], a.instances['RVE2DMatrix-1'], ), 
    keepIntersections=ON, originalInstances=SUPPRESS, domain=GEOMETRY) 
# mdb.models['Model-1'].rootAssembly.features.changeKey( 
#     fromName='RVE2DComposite-1', toName='Part-1-1') 

#**************************************************** 
# EXTRUDE-CUT SECTION TO TRIM BOUNDARY FIBRES 
#**************************************************** 
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF,engineeringFeatures=OFF) 
p1 = mdb.models['Model-1'].parts['Part-1'] 
session.viewports['Viewport: 1'].setValues(displayedObject=p1) 
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=2*h) 
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints 
s.setPrimaryObject(option=SUPERIMPOSE) 
p = mdb.models['Model-1'].parts['Part-1'] 
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES) 
s.rectangle(point1=(0 ,0), point2=(h , w)) 
s.rectangle(point1=(-4*h ,-4*w), point2=(4*h ,4*w))   # have to keep larger than the whole diagram.
session.viewports['Viewport: 1'].view.fitView() 
p = mdb.models['Model-1'].parts['Part-1'] 
p.Cut(sketch=s) 
s.unsetPrimaryObject() 
# mdb.models.changeKey(fromName='Model-1', toName='model-file' )
session.viewports['Viewport: 1'].setValues(displayedObject=None) 
 
# mdb.Model(name='Model-1') 
#************************************************************************ 
#                               END OF SCRIPT                             
#************************************************************************ 
# ------------------------------------------------------------------- 
