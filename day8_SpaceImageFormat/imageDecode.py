from pprint import pprint
from typing import Optional,List

def part2(filename: str, pixelWidth: int = 25, pixelHeight: int = 6)->Optional[str]:
    imageLength = pixelWidth * pixelHeight
    layers = parseImage(filename,imageLength)
    if not layers:
        return None
    finalImage = [0]*imageLength
    for pixel in range(imageLength):
        for layer in layers:
            if layer[pixel] != '2':
                # This is the pixel value at this location
                finalImage[pixel] = layer[pixel]
                break
    for i in range(pixelHeight):
        for j in range(pixelWidth):
            if finalImage[(i*pixelWidth)+j] == '1':
                print('X',end='')
            else: 
                print(' ',end='')
        print()
    print()
    return ''.join(finalImage)

def part1(filename: str, pixelWidth: int = 25, pixelHeight: int = 6)->Optional[int]:
    layers = parseImage(filename,pixelWidth * pixelHeight)
    minZeros = None
    onesTimesTwos = None
    layerNum = None
    for i,layer in enumerate(layers):
        zeros,ones,twos = countNums(layer)
        if minZeros is None or zeros < minZeros:
            minZeros = zeros
            layerNum = i
            onesTimesTwos = ones*twos
    zeros,ones,twos = countNums(layers[layerNum])
    return onesTimesTwos

def parseImage(filename: str,layerLength:int)->Optional[List[str]]:
    with open(filename,'r') as f:
        image = f.readline().strip()
        numberLayers = len(image) / layerLength
        layers = [image[i*layerLength:(i+1)*layerLength] for i in range(int(len(image)/layerLength))]
        return layers
    return None

def countNums(layer: str,a: str = '0',b: str = '1',c: str = '2')->(int,int,int):
    countA = 0
    countB = 0
    countC = 0
    for i in layer:
        if i == a:
            countA += 1
        if i == b:
            countB += 1
        if i == c:
            countC += 1
    return countA,countB,countC

