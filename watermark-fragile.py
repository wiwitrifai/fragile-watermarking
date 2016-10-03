import sys
from PIL import Image

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


def main():
    insert_lsb(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
    extract_lsb(str(sys.argv[3]), "extracted_lsb_"+str(sys.argv[3]))

if __name__ == '__main__':
  main()