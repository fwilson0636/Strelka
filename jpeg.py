from pprint import pprint

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# dictionary that will contain useful information
jpeg_parsed = dict()

jpeg_file = "Wikipedia-Logo-black-and-white.jpeg"
jpeg_file = "DSCN0025.jpeg"

image = Image.open(jpeg_file)

exifdata = image._getexif()

exif_table = dict()

for tag, value in exifdata.items():
    decoded = TAGS.get(tag, tag)
    exif_table[decoded] = value

#gps_info = dict()

if "GPSInfo" in exif_table:
    for key in exif_table['GPSInfo'].keys():
        decode = GPSTAGS.get(key, key)
        #gps_info[decode] = exif_table['GPSInfo'][key]

    # print out GPS information
    # pprint(gps_info)
    # short hand for merging two python dictionaries, may only work on python3.7+?
    #jpeg_parsed = {**gps_info, **jpeg_parsed}

# print out general information
# pprint(exif_table)

# getting height / width
height, width = image.size
jpeg_parsed["image_height"] = height
jpeg_parsed["image_width"] = width

# get colors
color_count = image.getcolors()

if color_count:
    jpeg_parsed["is_grayscale"] = True
    #print("grayscale image found")
else:
    jpeg_parsed["is_grayscale"] = False
    #print("color image found")

print(jpeg_parsed)

temp = dict()
# iterating over all EXIF data fields
for tag_id in exifdata:
    # get the tag name, instead of human unreadable tag id
    tag = TAGS.get(tag_id, tag_id)
    data = exifdata.get(tag_id)
    temp[tag] = data
    # decode bytes

try:
    # Reading from file
    filename = "fields.txt"
    fp = open(filename, 'r')
    print(fp.read())
    fp.close()

    fields: set = set()
    fields_list: list = list()

    with open(filename, 'r') as fp:
        print("using with statement...")

        for field in fp:
            fields.add(field.strip())
            fields_list.append(field.strip())

    #print(list(fields))
    print(f"searching for fields {fields_list}")
    print(f"existing fields {list(temp.keys())}")
    # insert conditional to print only fields in file from list to dictionary
    # reversed logic
    for tag in fields_list:
        if tag in temp.keys():
            jpeg_parsed[tag] = temp[tag]

except:
    pass

print("dictionary:", jpeg_parsed)
print(f"found {len(jpeg_parsed)} fields out of {len(fields_list)}")


"""
Reference: https://exiftool.org/TagNames/EXIF.html
Reference: https://pillow.readthedocs.io/en/latest/reference/ExifTags.html
Map for geo points: https://www.gps-coordinates.net/
If applicable to the image parse out the following:
* GPS information
* Image Height
* Image Width
* Exif Version (https://en.wikipedia.org/wiki/Exif#Version_history)
* Make of Camera 
* Model of Camera 
* Software 
* UserComment 
* DateTime (formatted in iso format or python datetime)
* identify if the image is black and white or color
"""