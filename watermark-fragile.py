import sys
import math
from PIL import Image

def psnr(watermarkedcover, plaincover):
    return 20 * math.log10(256/rms(watermarkedcover, plaincover))

def rms(image_a,image_b):
    px_a = image_a.load()
    px_b = image_b.load()
    for i in range(image_a.width):
        sum = 0
        for j in range(image_a.height):
            p_a = px_a[i,j]
            p_b = px_b[i,j]
            sum +=  math.pow((p_a[0] - p_b[0]), 2)
    return math.sqrt(sum / (image_a.width * image_a.height))
    

def extract_lsb(inputpath, outputpath):
    cover = Image.open(inputpath)
    lsb = Image.new("1", cover.size);
    px_cover = cover.load()
    px_lsb = lsb.load()

    for i in range(cover.width):
        for j in range(cover.height):
            p = px_cover[i, j]
            px_lsb[i, j] = (p[0] & 1)
    lsb.save(outputpath);
    lsb.show();

def insert_lsb(inputpath, watermarkpath, outputpath):
    cover = Image.open(inputpath)
    watermark = Image.open(watermarkpath).convert("1")
    output = Image.new(cover.mode, cover.size)
    px_cover = cover.load()
    px_watermark = watermark.load()
    px_output = output.load()

    for i in range(cover.width):
        for j in range(cover.height):
            p = list(px_cover[i, j])
            p[0] = (p[0] & 0b11111110) | (px_watermark[i % watermark.width, j % watermark.height] & 1)
            px_output[i, j] = tuple(p)
    output.save(outputpath)
    output.show()

def print_psnr(watermarkedpath, plainpath):
    watermarked = Image.open(watermarkedpath)
    plain = Image.open(plainpath)

    print("PSNR: " + str(psnr(watermarked, plain))) 

def main():
    insert_lsb(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
    extract_lsb(str(sys.argv[3]), "extracted_lsb_"+str(sys.argv[3]))
    print ("Analysis")
    print_psnr(str(sys.argv[1]), str(sys.argv[3]))

if __name__ == '__main__':
  main()
