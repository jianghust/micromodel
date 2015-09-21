import sys
import Image
import numpy as np
import random


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
        iMax = min(sizeX, self.centerX + self.R)
        jMin = max(0, self.centerY - self.R)
        jMax = min(sizeY, self.centerY + self.R)
        kMin = max(0, self.centerZ - self.R)
        kMax = min(sizeZ, self.centerZ + self.R)
        for i in range(iMin, iMax):
            for j in range(jMin, jMax):
                for k in range(kMin, kMax):
                    d2 = (i - self.centerX) ** 2 + (j - self.centerY) ** 2 + (k - self.centerZ) ** 2
                    if d2 <= self.R2:
                        dataSet[k, j, i] = self.value


class Cylinder:
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
        iMax = min(sizeX, self.centerX + self.R)
        jMin = max(0, self.centerY - self.R)
        jMax = min(sizeY, self.centerY + self.R)
        kMin = max(0, self.Z0)
        kMax = min(sizeZ, self.Z1)
        for i in range(iMin, iMax):
            for j in range(jMin, jMax):
                for k in range(kMin, kMax):
                    d2 = (i - self.centerX) ** 2 + (j - self.centerY) ** 2
                    if d2 <= self.R2:
                        dataSet[k, j, i] = self.value


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


def addNoise(data, sizeX, sizeY, sizeZ, noiseLevel):
    for k in xrange(sizeZ):
        for j in xrange(sizeY):
            for i in xrange(sizeX):
                data[k, j, i] += random.randint(-1 * noiseLevel, noiseLevel)


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


size_x = 256
size_y = 256
size_z = 256
data = np.zeros(size_x * size_y * size_z).reshape(size_z, size_y, size_x)
data[:] = 255

nBoxes = int(sys.argv[1]) ** 3

boxes = []

box_width = size_x / 20
box_height = box_width
box_depth = box_width

print

a0 = -box_width / 2
a1 = size_x + box_width / 2
b0 = -box_height / 2
b1 = size_y + box_height / 2
c0 = -box_depth / 2
c1 = size_z + box_depth / 2

for iBox in xrange(nBoxes):
    sys.stdout.write("\r" + str(iBox + 1) + ' / ' + str(nBoxes))
    sys.stdout.flush()
    location_x = random.randint(a0, a1)
    location_y = random.randint(b0, b1)
    location_z = random.randint(c0, c1)
    boxes.append(
        Box(location_x - box_width / 2, location_y - box_height / 2, location_z - box_depth / 2, box_width, box_height,
            box_depth, 0))

for box in boxes:
    box.setPixels(data, size_x, size_y, size_z)

smooth(data, size_x, size_y, size_z)

print '\n\nPorosity =', calc_phi(data, size_x, size_y, size_z, 127)

print data
for k in range(0, size_z):
    img = Image.fromarray(data[k].astype(np.uint8))
    img.save('./microModel_256_100_boxes_/microModel_256_' + str(k).zfill(4) + '.bmp')
