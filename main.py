import math
import urllib.request
import cv2

API_KEY = 'AoUQkcATQUN_lbITFwS4MnNLnxsSdx1gULgee1cIHoqcB8zOp-8se-3fEKzY05po'

def numberToBase(number, base):
    if number == 0:
        return [0]
    digits = []
    while number:
        digits.append(int(number % base))
        number //= base
    return digits[::-1]

def interweave(string1, string2):
    while(len(string1) != len(string2)):
        if len(string1) < len(string2):
            string1.insert(0, 0)
        else:
            string2.insert(0, 0)
    string_length = len(string1)
    new_string = []
    for i in range(0, string_length):
        new_string.append(string2[i])
        new_string.append(string1[i])
    return new_string

def calc_quad_key(tileX, tileY, level):
    bin_tileX = numberToBase(tileX, 2)
    bin_tileY = numberToBase(tileY, 2)
    keyString = interweave(bin_tileX, bin_tileY)
    key = int("".join(map(str, keyString)))
    quadkey = numberToBase(int(str(key), 2), 4)
    quadkey = str("".join(map(str, quadkey)))
    if len(quadkey) != level:
        while len(quadkey) < level:
            quadkey = '0' + quadkey
    return quadkey

'''
Coordinate Calculations from https://msdn.microsoft.com/en-us/library/bb259689.aspx
    sinLatitude = sin(latitude * pi/180)
    pixelX = ((longitude + 180) / 360) * 256 * 2level
    pixelY = (0.5 – log((1 + sinLatitude) / (1 – sinLatitude)) / (4 * pi)) * 256 * 2level
    tileX = floor(pixelX / 256)
    tileY = floor(pixelY / 256)
'''
def get_tile_coord(lat, lon, level=14):
    sinLatitude = math.sin(lat * math.pi/180)
    pixelX = ((lon + 180) / 360) * 256 * math.pow(2, level)
    pixelY = (0.5 - math.log((1 + sinLatitude) / (1 - sinLatitude)) / (4 * math.pi)) * 256 * math.pow(2, level)
    tileX = math.floor(pixelX / 256)
    tileY = math.floor(pixelY / 256)
    tile_coord = calc_quad_key(tileX, tileY, level)
    return tile_coord

def get_tile(lat, lon, level=14):
    base_url = 'http://h0.ortho.tiles.virtualearth.net/tiles/h'
    end_url = '.jpeg?g=131'
    tile_coord = get_tile_coord(lat, lon, level)
    url_string = base_url + tile_coord + end_url
    file_name = tile_coord + '.jpeg'
    image = urllib.request.urlretrieve(url_string, file_name)
    return file_name

def get_tile_matrix(minLat, maxLat, minLon, maxLon):
    return

def print_image(file_name):
    image=cv2.imread(file_name)
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyWindow('image')

print_image(get_tile(41.832482, -87.615588))