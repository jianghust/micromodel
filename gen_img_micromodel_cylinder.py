import sys
import Image
import numpy as np
import random


# box 
class Box:
    def __init__(self, x0, y0, z0, w, h, t, value):
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.x1 = self.x0 + w
        self.y1 = self.y0 + h
        self.z1 = self.z0 + t
        self.value = value

    def setPixels(self, dataSet, sizeX, sizeY, sizeZ):
        iMin = max(0, self.x0)
        iMax = min(sizeX, self.x1)
        jMin = max(0, self.y0)
        jMax = min(sizeY, self.y1)
        kMin = max(0, self.z0)
        kMax = min(sizeZ, self.z1)
        for i in range(iMin, iMax):
            for j in range(jMin, jMax):
                for k in range(kMin, kMax):
                    dataSet[k, j, i] = self.value


# sphere
class Sphere:
    def __init__(self, x, y, z, r, val):
        self.centerX = x
        self.centerY = y
        self.centerZ = z
        self.R = r
        self.R2 = r ** 2
        self.value = val

    def setPixels(self, dataSet, sizeX, sizeY, sizeZ):
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
                        dataSet[k, j, i] = self.value


# Verically oriented cylinder
class CylinderV:
    def __init__(self, x, y, z0, z1, r, val):
        self.centerX = x
        self.centerY = y
        self.Z0 = z0
        self.Z1 = z1
        self.R = r
        self.R2 = r ** 2
        self.value = val

    def setPixels(self, dataSet, sizeX, sizeY, sizeZ):
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
                        dataSet[k, j, i] = self.value


# Horizontally oriented cylinder
class CylinderH:
    """Return a new Vehicle object."""

    def __init__(self, x0, x1, y, z, r, val):
        self.centerY = y
        self.centerZ = z
        self.X0 = x0
        self.X1 = x1
        self.R = r
        self.R2 = r ** 2
        self.value = val

    def setPixels(self, dataSet, sizeX, sizeY, sizeZ):
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
                        dataSet[k, j, i] = self.value


# smooth the sharpe corner/edge of the images
def smooth(data, sizeX, sizeY, sizeZ):
    source = np.zeros(sizeX * sizeY * sizeZ).reshape(sizeZ, sizeY, sizeX)

    for k in xrange(sizeZ):
        for j in xrange(sizeY):
            for i in xrange(sizeX):
                source[k, j, i] = data[k, j, i]

    for k in xrange(sizeZ):
        for j in xrange(sizeY):
            for i in xrange(sizeX):
                n = 0
                sum_ = 0
                for kk in range(max(0, k - 1), min(sizeZ, k + 2)):
                    for jj in range(max(0, j - 1), min(sizeY, j + 2)):
                        for ii in range(max(0, i - 1), min(sizeX, i + 2)):
                            n += 1;
                            sum_ += source[kk, jj, ii]
                data[k, j, i] = max(0, min(255, round(sum_ / n)))

    del source


# add noise to the geometry
def addNoise(data, sizeX, sizeY, sizeZ, noiseLevel):
    for k in xrange(sizeZ):
        for j in xrange(sizeY):
            for i in xrange(sizeX):
                data[k, j, i] += random.randint(-1 * noiseLevel, noiseLevel)


# calculate the porosity of designed geometry
def calc_phi(data, sizeX, sizeY, sizeZ, threshold_color):
    sum_white = 0
    sum_black = 0
    for k in xrange(sizeZ):
        for j in xrange(sizeY):
            for i in xrange(sizeX):
                if data[k, j, i] >= threshold_color:
                    sum_white += 1
                else:
                    sum_black += 1
    if sum_white + sum_black != sizeZ * sizeY * sizeZ:
        print '>>>>>  something is wrong.'
    return float(sum_black) / float(sum_white + sum_black)


# user designed geometry

size_x = 256
size_y = 256
size_z = 256
data = np.zeros(size_x * size_y * size_z).reshape(size_z, size_y, size_x)
data[:] = 255

nCylindersV = int(sys.argv[1]) ** 3
nCylindersH = int(sys.argv[2]) ** 3

cylindersV = []
cylindersH = []

print

for iCylinderV in xrange(nCylindersV):
    sys.stdout.write("\r" + str(iCylinderV + 1) + ' / ' + str(nCylindersV))
    sys.stdout.flush()
    cylinder_radius = random.randint(1, 20)
    cylinder_z0 = 0
    cylinder_z1 = size_z
    location_x = random.randint(-cylinder_radius, size_x + cylinder_radius)
    location_y = random.randint(-cylinder_radius, size_y + cylinder_radius)
    cylindersV.append(
        CylinderV(location_x - cylinder_radius, location_y - cylinder_radius, cylinder_z0, cylinder_z1, cylinder_radius,
                  0))

for cylinderV in cylindersV:
    cylinderV.setPixels(data, size_x, size_y, size_z)

for iCylinderH in xrange(nCylindersH):
    sys.stdout.write("\r" + str(iCylinderH + 1) + ' / ' + str(nCylindersH))
    sys.stdout.flush()
    cylinder_radius = random.randint(1, 20)
    cylinder_x0 = 0
    cylinder_x1 = size_x
    location_y = random.randint(-cylinder_radius, size_y + cylinder_radius)
    location_z = random.randint(-cylinder_radius, size_z + cylinder_radius)
    cylindersH.append(
        CylinderH(cylinder_x0, cylinder_x1, location_y - cylinder_radius, location_z - cylinder_radius, cylinder_radius,
                  0))

for cylinderH in cylindersH:
    cylinderH.setPixels(data, size_x, size_y, size_z)



# smooth(data,size_x,size_y,size_z)

print '\n\nPorosity =', calc_phi(data, size_x, size_y, size_z, 127)

for k in range(0, size_z):
    img = Image.fromarray(data[k].astype(np.uint8))
    img.save('./microModel_256_cylinder/cylinder_' + str(k).zfill(4) + '.bmp')
