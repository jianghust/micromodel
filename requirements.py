# import the micro library
import micromodel

# define size of the domain
domain_size = [300,300,400]

# create a domain instance
domain = micromodel.Domain(size=domain_size)

# create boxes and cylinders (many more shapes possible)
box1 = micromodel.Box(x0=0,y0=0,z0=0,width=100,height=100,depth=100)
box2 = micromodel.Box(x0=200,y0=0,z0=0,width=100,height=100,depth=100)
cyl1 = micromodel.Cylinder(x0=100,y0=100,z0=100,x1=200,y1=200,z1=200,r=40)
cyl2 = micromodel.Cylinder(startLocation=box1, endLocation=box2,r=40)

# add the shapes to the domain
domain.add([box1,box2,cyl1,cyl2])

# create another domain instance
another_domain = micromodel.Domain(size=domain_size)

# fill this domain with random spheres that are fully contained within the domain
another_domain.fillWithRandomSpheres(minRadius=5,maxRadius=8,consolidation=0.3,contained=True)

# fuse the two domains together along the z axis, returning a new  combined domain
totalDomain = micromodel.fuseDomains(dom1=domain,dom2=another_domain,location=micro.ZMIN)

# save the domain to a stack of images
totalDomain.saveImages('/path/to/images/my_image_name_') # will result in images named my_image_name_0000.bmp to my_image_name_0799.bmp