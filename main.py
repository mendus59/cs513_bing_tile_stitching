import math
import urllib.request
import cv2
import numpy as np
import itertools


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

def pixel_coord(lat,lon,level=14):
    lat_pix=float(lat)
    lon_pix=float(lon)
    matrix_size=2**(8+level)

    pix_x=min(lat_pix,0,matrix_size-1)-0.5
    pix_y=0.5-min(lon_pix,0,matrix_size-1)

    lat_calc=90-360*math.atan(math.exp(-pix_y*2*math.pi))/math.pi
    lon_calc=360*pix_x
    return int(lat_calc),int(lon_calc)

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


def print_image(file_name):
    image=cv2.imread(file_name)
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyWindow('image')


def get_tile_matrix(lat1, lon1, lat2, lon2,size=12):
    lat1, lat2 = min(lat1, lat2), max(lat1, lat2)
    lon1, lon2 = min(lon1, lon2), max(lon1, lon2)
    x1, y1 = pixel_coord(lat1, lon1)
    x2, y2 = pixel_coord(lat2, lon2)
    x_range=lat2-lat1
    y_range=lon2-lon1
    size_x=x_range/size
    print(x_range,size_x)
    size_y=y_range/size
    x_rng = np.linspace(x1, x2 + 1, size)
    y_rng = np.linspace(y1, y2 + 1, size)
    
    
    xy_pairs = itertools.product(x_rng, y_rng) 
    #return(xy_pairs)
    return[get_tile_coord(x, y) for x,y in xy_pairs], (len(x_rng), len(y_rng))



#(xy_sample,(a,b))=get_tile_matrix(49.00000,85.00000,49.00100,85.00100)

#for xy_samples, possible_values in xy_sample.items():
    #print(xy_samples,possible_values)
#print_image(get_tile(41.832482, -87.615588))
