import sys
import math
import itertools
import random
from PIL import Image
    
def shuffle_order(cover_image, key):
    order = []
    for i in range (cover_image.width * cover_image.height):
        order.append(i)
    random.seed(ord(key[len(key)-1]) % len(order))
    shuffled = random.shuffle(order)
    return order
    
def encrypt(plain, key):
    cipher = []
    k = 0
    for i in range(0, len(plain), 8):
    	c = plain[i:i+8]
    	binary = ''.join(c)
    	cipher.append(chr((int(binary, 2)+ord(key[k%len(key)])) % 256))
    	k += 1
    	# c = ord(plain[i])+ord(key[i%len(key)])
    	# cipher.append(chr(c%256))

    return "".join(cipher)

def readBitImage(image):
    bit = []
    px = image.load()
    for i in range(image.width):
        for j in range(image.height):
            if (px[i, j] == 0):
                bit.append('0')
            else:
            	bit.append('1')

    return "".join(bit)

def psnr(watermarkedcover, plaincover):
    return 20 * math.log10(255/rms(watermarkedcover, plaincover))

def rms(image_a,image_b):
    px_a = image_a.load()
    px_b = image_b.load()
    sum=0;
    for i in range(image_a.width):
        for j in range(image_a.height):
            p_a = px_a[i,j]
            p_b = px_b[i,j]
            sum += math.pow((p_a[0] - p_b[0]), 2) + math.pow((p_a[1] - p_b[1]), 2) + math.pow((p_a[2] - p_b[2]), 2)

    return math.sqrt(sum / (image_a.width * image_a.height) / 3)
    

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
    #lsb.show();

def insert_lsb(inputpath, watermarkpath, outputpath):
    cover = Image.open(inputpath)
    watermark = Image.open(watermarkpath).convert("1")
    output = Image.new(cover.mode, cover.size)

    px_cover = cover.load()
    # px_watermark = watermark.load()
    px_output = output.load()


    key = input("Masukkan kunci: ")
    # order = shuffle_order(cover, key)
    bitImage = readBitImage(watermark)
    cipher = encrypt(bitImage, key)
    k = 0
    l = 0
    px_watermark = '{0:08b}'.format(ord(cipher[k]))
    for i in range(cover.width):
        for j in range(cover.height):
            p = list(px_cover[i, j])
            if l > 7:
            	k += 1
            	px_watermark = '{0:08b}'.format(ord(cipher[k%len(cipher)]))
            	l = 0
            p[0] = (p[0] & 0b11111110) | int(px_watermark[l])
            l += 1
            px_output[i, j] = tuple(p)
    output.save(outputpath)
    #output.show()

            # p[0] = (p[0] & 0b11111110) | (px_watermark[i % watermark.width, j % watermark.height] & 1)

def print_psnr(watermarkedpath, plainpath):
    watermarked = Image.open(watermarkedpath)
    plain = Image.open(plainpath)

    print("PSNR: " + str(psnr(watermarked, plain))) 

def main():
    cmd = input("masukkan pilihan (i)nsert / (e)xtract: ")
    if cmd == 'i':
        insert_lsb(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
        print ("Analyzing...")
        print_psnr(str(sys.argv[1]), str(sys.argv[3]))
    else:
        extract_lsb(str(sys.argv[1]), "extracted_lsb_"+str(sys.argv[3]))

if __name__ == '__main__':
    main()
