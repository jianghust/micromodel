import random
import sys
import Image
import numpy as np
import os

"""A Micromodel library, including the following class

    Shape:
        1) box.
        2) spheres.
        3) cylinders.

    Domain:
        1) specify the size of image domain, 
        2) add different shapes to the domain, with input coordinates,
        3) fuse different domains into one big domain
        4) create and save images from the domain


    There are also other optional properties included in the domain that can be used for all the shapes, 
        addNoise to the created geometry 
        smooth the sharp geometry
        calculate the porousity of constructed geometry

"""


# class Shape,all shape class parent

class Shape():

    class Box(Shape):
        def __init__(self,width,height,thickness,value):
            self.width = width
            self.height = height
            self.thickness = thickness
            self.value = value
        def getwidth (self):
            return self.width
        def getheight (self):
            return self.height
        def getthickness (self):
            return self.thickness
        def value(self):
            return self.value


    class Sphere(Shape):
        def __init__(self,radius,value):
            self.radius = radius
            self.value = value
        def getradius(self):
            return self.radius
        def value(self):
            return self.value

    class Cylinder(Shape):
        def __init__(self,length,radius,value):
            self.length = length
            self.radius = radius
            self.value = value
        def getradius(self):
            return self.radius
        def getlength(self):
            return self.length
        def value(self):
            return self.value  

class Domain:
    def __init__(self, sizeX, sizeY, sizeZ):
        self.shapes = list()
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.sizeZ = sizeZ
        self.data = np.zeros(sizeX * sizeY * sizeZ).reshape(sizeX, sizeY, sizeZ)
        self.data [:] = np.uint8(255)


    def addShape(self, newshape, x0, y0, z0):
            if isinstance(newshape, Shape) == False:
                print 'No such shape!'
            elif newshape == "Box"
                    w = newshape.getwidth()
                    h = newshape.getheight()
                    t = newshape.getthickness()
                    val = newshape.value()
                    iMin = max(0, self.x0)
                    iMax = min(sizeX, self.x0 + w)
                    jMin = max(0, self.y0)
                    jMax = min(sizeY, self.y0 + h)
                    kMin = max(0, self.z0)
                    kMax = min(sizeZ, self.z0 + t)
                    for i in range(iMin, iMax):
                        for j in range(jMin, jMax):
                            for k in range(kMin, kMax):
                                self.data[k, j, i] = val
            elif newshape == "Sphere" 
                    R = newshape.getradius() 
                    R2 = R**2 
                    val = newshape.value()            
                    iMin = max(0,self.x0-R)
                    iMax = min(sizeX,self.x0+R+1)
                    jMin = max(0,self.y0-R)
                    jMax = min(sizeY,self.y0+R+1)
                    kMin = max(0,self.z0-R)
                    kMax = min(sizeZ,self.z0+R+1)
                    for i in range(iMin,iMax):
                            for j in range(jMin,jMax):
                                    for k in range(kMin,kMax):
                                            d2 = (i-self.x0)**2+(j-self.y0)**2+(k-self.z0)**2
                                            if d2 <= R2:
                                                    self.data[k,j,i] = val
            elif newshape == "Cylinder"
                    R = newshape.getradius() 
                    R2 = R**2 
                    L = newshape.getlength()
                    val = newshape.value()
                    iMin = max(0,self.x0-R)
                    iMax = min(sizeX,self.x0+R+1)
                    jMin = max(0,self.y0-R)
                    jMax = min(sizeY,self.y0+R+1)
                    kMin = max(0,self.z0)
                    kMax = min(sizeZ,z0+L+1)
                    for i in range(iMin,iMax):
                            for j in range(jMin,jMax):
                                    for k in range(kMin,kMax):
                                            d2 = (i-self.x0)**2+(j-self.y0)**2
                                            if d2 <= R2:
                                                    self.data[k,j,i] = val


    # if user simplied want to create spheres in the domain with range of radius and random position, can call this function directly
    def fillWithRandomSpheres(self, minRadius, maxRadius, numbers):
        for iSphere in xrange(numbers):
            , = random.randint(minRadius, maxRadius)
            location_x = random.randint(-sphere_radius, self.sizeX + sphere_radius)
            location_y = random.randint(-sphere_radius, self.sizeY + sphere_radius)
            location_z = random.randint(-sphere_radius, self.sizeZ + sphere_radius)
            domain.addShape(Sphere(sphere_radius,0),location_x,location_y,location_z)
    

    def fuseDomain(self, other, location):
        if location == "x":
            newDomain = np.hstack(this.domain.getDomain(), other.domain.getDomain())
        elif location == "y":
            newDomain = np.vstack(this.domain.getDomain(), other.domain.getDomain())
        elif location == "z":
            newDomain = np.dstack(this.domain.getDomain(), other.domain.getDomain())
        else:
            print "Wrong location!"
        return newDomain

    # smooth the shape edges in the domain

    def smooth(data,sizeX,sizeY,sizeZ):

        source = np.zeros(sizeX*sizeY*sizeZ).reshape(sizeZ,sizeY,sizeX)

        for k in xrange(sizeZ):
            for j in xrange(sizeY):
                for i in xrange(sizeX):
                    source[k,j,i] = data[k,j,i]

        for k in xrange(sizeZ):
            for j in xrange(sizeY):
                for i in xrange(sizeX):
                    n = 0
                    sum_ = 0
                    for kk in range(max(0,k-1),min(sizeZ,k+2)):
                        for jj in range(max(0,j-1),min(sizeY,j+2)):
                            for ii in range(max(0,i-1),min(sizeX,i+2)):
                                n += 1;
                                sum_ += source[kk,jj,ii]
                    data[k,j,i] = max(0,min(255,round(sum_/n)))

        del source


#add noise to the geometry
def addNoise(data,sizeX,sizeY,sizeZ,noiseLevel):
    for k in xrange(sizeZ):
        for j in xrange(sizeY):
            for i in xrange(sizeX):
                data[k,j,i] += random.randint(-1*noiseLevel,noiseLevel) 




# calculate the porosity of designed geometry
def calcPhi(self, threshold_color):
    sum_white = 0
    sum_black = 0
        for k in xrange(sizeZ):
                for j in xrange(sizeY):
                        for i in xrange(sizeX):
                if data[k,j,i] >= threshold_color:
                    sum_white += 1
                else:
                    sum_black += 1   
    if sum_white+sum_black != sizeZ*sizeY*sizeZ:
        print '>>>>>  something is wrong.'                             
    return float(sum_black)/float(sum_white+sum_black)



def saveImages(self, path, name=''):
        if not os.path.exists(path):
            os.makedirs(path)
        #for index in range(len(self.shapes)):
        #   self.shapes[index].saveImages(path, name + '_' + str(index) + '_' + self.shapes[
        #       index].__class__.__name__.lower() + '_')
        for k in range (0,sizeZ):
            img = Image.fromarray(data[k].astype(np.uint8))
            img.save('./microModel_256_cylinder/cylinder_'+str(k).zfill(4)+'.bmp')