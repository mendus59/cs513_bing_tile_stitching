import math
import urllib.request
import cv2
import sys
import numpy as np

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

def pixel_coord(lat,lon,level):
    lat_pix=float(lat)
    lon_pix=float(lon)
    matrix_size=2**(8+level)

    pix_x=min(lat_pix,0,matrix_size-1)-0.5
    pix_y=0.5-min(lon_pix,0,matrix_size-1)

    lat_calc=90-360*math.atan(math.exp(-pix_y*2*math.pi))/math.pi
    lon_calc=360*pix_x
    return int(lat_calc),int(lon_calc)

def get_tile_coord(lat, lon, level):
    sinLatitude = math.sin(lat * math.pi/180)
    pixelX = ((lon + 180) / 360) * 256 * math.pow(2, level)
    pixelY = (0.5 - math.log((1 + sinLatitude) / (1 - sinLatitude)) / (4 * math.pi)) * 256 * math.pow(2, level)
    tileX = math.floor(pixelX / 256)
    tileY = math.floor(pixelY / 256)
    tile_coord = calc_quad_key(tileX, tileY, level)
    return tile_coord

def get_tile(lat, lon, level):
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

def get_tile_matrix(minLat, minLon, maxLat, maxLon, level):
    lat_tiles_at_level = 180/math.pow(2, level)
    lon_tiles_at_level = 360/math.pow(2, level)
    lat_diff = abs(maxLat - minLat)
    lon_diff = abs(maxLon - minLon)
    # Create an n x m matrix where n is number of lat tiles and m is number of lon tiles
    n_size = math.ceil(lat_diff / lat_tiles_at_level)
    m_size = math.ceil(lon_diff / lon_tiles_at_level)
    lat_per_tile = lat_diff / n_size
    lon_per_tile = lon_diff / m_size

    print(lat_tiles_at_level, lat_diff, n_size, lat_per_tile)

    tile_matrix = [[0 for m in range(n_size)] for m in range(m_size)]
    currentLon = minLon
    for n in range(0, m_size):
        currentLat = minLat
        for m in range(0, n_size):
            tile_matrix[n][m] = get_tile(currentLat, currentLon, level)
            if minLat - maxLat < 0:
                currentLat += lat_per_tile
            else:
                currentLat -= lat_per_tile
        if minLon - maxLon < 0:
            currentLon += lon_per_tile
        else:
            currentLon -= lon_per_tile
    return tile_matrix

def filter_matrix(matrix):
    matrix_rows = len(matrix)
    for i in range(0, matrix_rows):
        row = set()
        new_matrix_row = []
        for item in matrix[i]:
            if item not in row:
                row.add(item)
                new_matrix_row.append(item)
        matrix[i] = new_matrix_row
    for i in range(0, matrix_rows-1):
        if i < len(matrix)-1:
            if matrix[i][0] == matrix[i+1][0]:
                del matrix[i]
    return(matrix)

# Direction, 0 for vertical, 1 for horizontal
def stitch(img_name1, img_name2, direction):
    img1 = cv2.imread(img_name1)
    img2 = cv2.imread(img_name2)
    concat = np.concatenate((img1, img2), axis=direction)
    return concat

def stitch_image_matrix(matrix):
    matrix_rows = len(matrix)
    image_row = []
    for i in range(0, matrix_rows):
        image_col = []
        for item in matrix[i]:
            image_col.append(cv2.imread(item))
        image_row.append(np.concatenate(image_col, 0))
    final_image = np.concatenate(image_row, 1)
    cv2.imwrite('output.jpeg', final_image)

def main():
    # testminlat = 41.9086744
    # testminlon = -87.6818312
    # testmaxlat = 41.8097234
    # testmaxlon = -87.6023627
    testminlat = 41.863771
    testminlon = -87.618410
    testmaxlat = 41.860802
    testmaxlon = -87.614784

    matrix = get_tile_matrix(testminlat, testminlon, testmaxlat, testmaxlon, 19)
    print(matrix)
    filtered_matrix = filter_matrix(matrix)
    print(filtered_matrix)
    stitch_image_matrix(filtered_matrix)


if __name__ == '__main__':
    main()