import random
import sys
import Image
import numpy as np
import os

"""A Micromodel library, including the following class

    Shape:
        1) box.
        2) spheres.
        3) cylinders: horizontally oriented (x aligned) or vertially aligned (z oriented) cylinders.

    Domain:
        user can specify the size of image domain, add different shapes to the domain, fuse different domains,
        create and save images from the domain


    There are also other optional properties included in the domain that can be used for all the shapes, 
        addNoise to the created geometry 
        smooth the sharp geometry
        calculate the porousity of constructed geometry

"""


# class Shape,all shapre class parent

class Shape():
    def setDataLimit(self, sizeX, sizeY, sizeZ):
        self.data = np.zeros(sizeX * sizeY * sizeZ).reshape(sizeX, sizeY, sizeZ)
        self.data[:] = np.uint8(255)
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.sizeZ = sizeZ

    def setPixels(self, sizeX, sizeY, sizeZ):
        pass

    def addNoise(self, noiseLevel):
        for k in xrange(self.sizeZ):
            for j in xrange(self.sizeY):
                for i in xrange(self.sizeX):
                    self.data[k, j, i] += random.randint(-1 * noiseLevel, noiseLevel)

    def getData(self):
        return self.data

    def smooth(self):
        source = self.setDataLimit(self.sizeX, self.sizeY, self.sizeZ);

        for k in xrange(self.sizeZ):
            for j in xrange(self.sizeY):
                for i in xrange(self.sizeX):
                    source[k, j, i] = self.data[k, j, i]

        for k in xrange(self.sizeZ):
            for j in xrange(self.sizeY):
                for i in xrange(self.sizeX):
                    n = 0
                    sum_ = 0
                    for kk in range(max(0, k - 1), min(self.sizeZ, k + 2)):
                        for jj in range(max(0, j - 1), min(self.sizeY, j + 2)):
                            for ii in range(max(0, i - 1), min(self.sizeX, i + 2)):
                                n += 1;
                                sum_ += source[kk, jj, ii]
                    self.data[k, j, i] = max(0, min(255, round(sum_ / n)))
        del source

    def saveImages(self, path, name):
        self.data = np.uint8(self.data)
        for index in range(len(self.data)):
            img = Image.fromarray(self.data[index])
            img.save(path + name + str(index).zfill(4) + '.bmp')

            # the size here is the size of shapes, it has nothing to do with the entire domain size
            # value is the pixel value written in the image


# Box
class Box(Shape):
    data = []

    def __init__(self, x0, y0, z0, w, h, t, value):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.x1 = self.x0 + w
        self.y1 = self.y0 + h
        self.z1 = self.z0 + t
        self.value = value

    def setPixels(self, sizeX, sizeY, sizeZ):
        self.setDataLimit(sizeX, sizeY, sizeZ)
        iMin = max(0, self.x0)
        iMax = min(sizeX, self.x1)
        jMin = max(0, self.y0)
        jMax = min(sizeY, self.y1)
        kMin = max(0, self.z0)
        kMax = min(sizeZ, self.z1)
        for i in range(iMin, iMax):
            for j in range(jMin, jMax):
                for k in range(kMin, kMax):
                    self.data[k, j, i] = self.value


# Sphere

class Sphere(Shape):
    def __init__(self, x, y, z, r, value):
        self.centerX = x
        self.centerY = y
        self.centerZ = z
        self.R = r
        self.R2 = r ** 2
        self.value = value

    def setPixels(self, sizeX, sizeY, sizeZ):
        self.setDataLimit(sizeX, sizeY, sizeZ)
        iMin = max(0, self.centerX - self.R)
        iMax = min(sizeX, self.centerX + self.R + 1)
        jMin = max(0, self.centerY - self.R)
        jMax = min(sizeY, self.centerY + self.R + 1)
        kMin = max(0, self.centerZ - self.R)
        kMax = min(sizeZ, self.centerZ + self.R + 1)
        for i in range(iMin, iMax):
            for j in range(jMin, jMax):
                for k in range(kMin, kMax):
                    d2 = (i - self.centerX) ** 2 + (j - self.centerY) ** 2 + (k - self.centerZ) ** 2
                    if d2 <= self.R2:
                        self.data[k, j, i] = self.value


# Vertical oriented cylinder

class CylinderV(Shape):
    def __init__(self, x, y, z0, z1, r, val):
        self.centerX = x
        self.centerY = y
        self.Z0 = z0
        self.Z1 = z1
        self.R = r
        self.R2 = r ** 2
        self.value = val

    def setPixels(self, sizeX, sizeY, sizeZ):
        self.setDataLimit(sizeX, sizeY, sizeZ)
        iMin = max(0, self.centerX - self.R)
        iMax = min(sizeX, self.centerX + self.R + 1)
        jMin = max(0, self.centerY - self.R)
        jMax = min(sizeY, self.centerY + self.R + 1)
        kMin = max(0, self.Z0)
        kMax = min(sizeZ, self.Z1 + 1)
        for i in range(iMin, iMax):
            for j in range(jMin, jMax):
                for k in range(kMin, kMax):
                    d2 = (i - self.centerX) ** 2 + (j - self.centerY) ** 2
                    if d2 <= self.R2:
                        self.data[k, j, i] = self.value


# Horizontally oriented cylinder

class CylinderH(Shape):
    def __init__(self, x0, x1, y, z, r, val):
        self.centerY = y
        self.centerZ = z
        self.X0 = x0
        self.X1 = x1
        self.R = r
        self.R2 = r ** 2
        self.value = val

    def setPixels(self, sizeX, sizeY, sizeZ):
        self.setDataLimit(sizeX, sizeY, sizeZ)
        iMin = max(0, self.X0)
        iMax = min(sizeX, self.X1 + 1)
        jMin = max(0, self.centerY - self.R)
        jMax = min(sizeY, self.centerY + self.R + 1)
        kMin = max(0, self.centerZ - self.R)
        kMax = min(sizeZ, self.centerZ + self.R + 1)
        for i in range(iMin, iMax):
            for j in range(jMin, jMax):
                for k in range(kMin, kMax):
                    d2 = (j - self.centerY) ** 2 + (k - self.centerZ) ** 2
                    if d2 <= self.R2:
                        self.data[k, j, i] = self.value
                        # Class Domain


class Domain:
    def __init__(self, sizeX, sizeY, sizeZ):
        self.shapes = list()
        #        self.domain = domain
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.sizeZ = sizeZ
        # domain = np.array([sizeX,sizeY,sizeZ])

        # domain[] is a list with domain[0] = axis X, domain[1] = axis Y and domain[2] = axis Z
        # initialize a 3D data array to store pixels

    #    def getdomain(self):
    #        data = np.zeros(self.sizeX * self.sizeY * self.sizeZ).reshape(self.sizeX, self.sizeY, self.sizeZ)
    #        data[:] = 255
    #        return data

    # First, identify if we have such shape in the library
    # if does, append the shape to current domain list and construct it
    # iterate the list, add all the shapes to the specified domain

    def addShape(self, *args):
        for value in args:
            if isinstance(value, Shape) == False:
                print 'No such shape!'
            else:
                value.setPixels(self.sizeX, self.sizeY, self.sizeZ)
                self.shapes.append(value)

    # if user simplied want to create spheres in the domain with range of radius and random position, can call this function directly
    def fillWithRandomSpheres(self, minRadius, maxRadius, numbers):
        for iSphere in xrange(numbers):
            sphere_radius = random.randint(minRadius, maxRadius)
            location_x = random.randint(-sphere_radius, self.sizeX + sphere_radius)
            location_y = random.randint(-sphere_radius, self.sizeY + sphere_radius)
            location_z = random.randint(-sphere_radius, self.sizeZ + sphere_radius)
            self.shapes.append(
                Sphere(location_x - sphere_radius, location_y - sphere_radius, location_z - sphere_radius,
                       sphere_radius, 0))
        for sphere in self.shapes:
            sphere.setPixels(self.sizeX, self.sizeY, self.sizeZ)

            # user can build different small domains and fuse them into an bigger domain, but limited to grow in x, y, z directly right now.

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
    def smooth(self, sizeX, sizeY, sizeZ):
        for k in range(len(self.shapes)):
            self.shapes[0].smooth()

    # addNoise to the shapes in the domain
    def addNoise(self, noiseLevel):
        for k in range(len(self.shapes)):
            self.shapes[0].addNoise(noiseLevel)

    # calculate the porosity of designed geometry
    def calcPhi(self, threshold_color):
        sum_white = 0
        sum_black = 0

        for index in xrange(len(self.shapes)):
            data = self.shapes[index].getData()
            for k in xrange(self.sizeZ):
                for j in xrange(self.sizeY):
                    for i in xrange(self.sizeX):
                        if data[k, j, i] >= threshold_color:
                            sum_white += 1
                        else:
                            sum_black += 1
        return float(sum_black) / float(sum_white + sum_black)

    # save images

    def saveImages(self, path, name=''):
        if not os.path.exists(path):
            # 创建目录
            os.makedirs(path)
        for index in range(len(self.shapes)):
            self.shapes[index].saveImages(path, name + '_' + str(index) + '_' + self.shapes[
                index].__class__.__name__.lower() + '_')
