import sys
import pprint
import micromodel

domain_size = [300,300,400]
#test = Test()
#shape = micromodel.CylinderV(x0=100,y0=100,z0=100,x1=200,y1=200,z1=200,r=40)
shape = micromodel.Sphere(10,100,10,20,0)
shape.setPixels(256,256,256)
shape.saveImages('./imgtemp/','wow')
