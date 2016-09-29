import sys
from PIL import Image

d = dict()
colorsum = 0

image = Image.open(str(sys.argv[1]))

print("Counting...")

for i in range(image.size[0]):
    for j in range(image.size[1]):
        r, g, b = image.getpixel((i,j))
        key = "R: " + str(r).zfill(3) + " G: " + str(g).zfill(3) + " B: " + str(b).zfill(3) 
        if key in d:
            d[key] += 1
        else:
            d[key] = 1
            colorsum += 1

for key in d:
    print("Color: ", key, " Occurence: ", d[key])

print("Total color: ", colorsum)
