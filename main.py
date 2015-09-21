import sys
import pprint
import micromodel

domain_size = [300, 300, 400]
# test = Test()
# Sphere = micromodel.CylinderV(x0=100,y0=100,z0=100,x1=200,y1=200,z1=200,r=40)
sphere = micromodel.Sphere(10, 100, 10, 20, 0)
# sphere.setPixels(256,256,256)
# sphere.saveImages('./imgtemp/','wow')

sphere2 = micromodel.Sphere(100, 50, 10, 20, 0)
sphere3 = micromodel.Sphere(1, 30, 10, 20, 0)

domain = micromodel.Domain(256, 256, 256);
domain.addShape(sphere2, sphere3)
domain.saveImages('./image/', 'img')
#print "the Porosity = " + str(domain.calcPhi(127))
