from pprint import pprint

#enabling the use of JPEG image functions
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# dictionary that will contain requested metadata
jpeg_parsed = dict()

#two different images files to compare the varying metadata fields
jpeg_file = "Wikipedia-Logo-black-and-white.jpeg"
#jpeg_file = "DSCN0025.jpeg"

#begins the process of reading and parsing metadata
image = Image.open(jpeg_file)

exifdata = image._getexif()

exif_table = dict()

for tag, value in exifdata.items():
    decoded = TAGS.get(tag, tag)
    exif_table[decoded] = value

    temp = dict()
# iterating over all EXIF data fields
for tag_id in exifdata:
    # get the tag name, instead of human unreadable tag id
    tag = TAGS.get(tag_id, tag_id)
    data = exifdata.get(tag_id)
    temp[tag] = data
    # decode bytes

#
try:
    # Reading from file
    filename = "fields.txt"
    fp = open(filename, 'r')
    print(fp.read())
    fp.close()

    fields: set = set()
    fields_list: list = list()

    with open(filename, 'r') as fp:
        print("the image used resulted in...")

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