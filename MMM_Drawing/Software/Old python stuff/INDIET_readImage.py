from PIL import Image

def readImage(path):
    img = Image.open(path)
    cols, rows = img.size
    imgList = [[0]*cols for x in range(rows)]
    pixels = img.load()
    for row in range(rows):
        for col in range(cols):
            if (pixels[row,col] == (255,255,255)):
                imgList[row][col] = 0
            else:
                imgList[row][col] = 1
    return imgList

