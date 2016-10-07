import sys
import math
import itertools
import random
from PIL import Image
    
def shuffle_order(size, shuffle_seed):
    order = []
    for i in range (size):
        order.append(i)
    if (shuffle_seed):
        random.seed(shuffle_seed)
        shuffled = random.shuffle(order)
        return order
    else:
        return order
    
def encrypt(plain, key):
    cipher = []
    k = 0
    len_key = len(key)
    len_plain = len(plain)
    for i in range(len_plain):
        cipher.append((plain[i] + ord(key[i % len_key])) % 256)
    return cipher

def decrypt(cipher, key):
    plain = []
    k = 0
    len_key = len(key)
    len_cipher = len(cipher)
    for i in range(len_cipher):
        plain.append((cipher[i] + 256 - ord(key[i % len_key])) % 256)
    return plain


def readLSB(image, width, binary, order):
    bit = []
    px = image.load()
    k = 0
    cur = 0
    for pos in order:
        i = pos / width
        j = pos % width
        if (binary):
            cur |= (px[i % image.width, j % image.height] & 1) << k
        else:
            cur |= (px[i % image.width, j % image.height][0] & 1) << k
        k += 1
        if (k >= 8):
            bit.append(cur)
            k = 0
            cur = 0
    if (k > 0):
        bit.append(cur)
    return bit

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

    key = input("masukkan kunci: ")
    seed = 0
    key_size = len(key)
    for i in range(key_size):
        seed += ord(key[i])
    cipher = readLSB(cover, cover.width, 0, shuffle_order(cover.width * cover.height, seed))
    plain = decrypt(cipher, key)

    k = 0
    cur = 0
    positions = shuffle_order(cover.width * cover.height, 0)
    for pos in positions:
        i = pos / cover.width
        j = pos % cover.width
        px_lsb[i, j] = ((plain[int(k / 8)] >> (k % 8)) & 1)
        k = (k + 1)
    lsb.save(outputpath);
    lsb.show();

def insert_lsb(inputpath, watermarkpath, outputpath):
    cover = Image.open(inputpath)
    watermark = Image.open(watermarkpath).convert("1")
    output = Image.new(cover.mode, cover.size)
    px_cover = cover.load()
    px_watermark = watermark.load()
    px_output = output.load()
    plain = readLSB(watermark, cover.width, 1, shuffle_order(cover.width * cover.height, 0))
    key = input("masukkan kunci: ")
    cipher = encrypt(plain, key)
    
    k = 0
    cur = 0
    mod = watermark.width * watermark.height
    seed = 0
    key_size = len(key)
    for i in range(key_size):
        seed += ord(key[i])
    positions = shuffle_order(cover.width * cover.height, seed)
    for pos in positions:
        i = pos / cover.width
        j = pos % cover.width
        p = list(px_cover[i, j])
        p[0] = (p[0] & 0b11111110) | ((cipher[int(k / 8)]>>(k % 8)) & 1)
        k = (k + 1) % mod
        px_output[i, j] = tuple(p)
    output.save(outputpath)
    output.show()

def print_psnr(watermarkedpath, plainpath):
    watermarked = Image.open(watermarkedpath)
    plain = Image.open(plainpath)

    print("PSNR: " + str(psnr(watermarked, plain))) 

def main():
    cmd = input("masukkan pilihan (i)nsert / (e)xtract: ")
    if cmd == 'i':
        insert_lsb(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
        print("Original image:", sys.argv[1])
        print("Watermark image:", sys.argv[2])
        print("Image with watermark:", sys.argv[3])
        print("Analyzing...")
        print_psnr(str(sys.argv[1]), str(sys.argv[3]))
    else:
        print("Image with watermark:", sys.argv[1])
        print("Extracted watermark:", sys.argv[2])
        extract_lsb(str(sys.argv[1]), "extracted_lsb_"+str(sys.argv[2]))

if __name__ == '__main__':
    main()
