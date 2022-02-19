from sys import argv
from PIL import Image
from PIL.ExifTags import TAGS
import os.path


def parse_jpeg_from_path(path: str) -> dict:
    """
    This function will take the path of a JPEG image file as input and produce a dictionary from the requested list of metadata fields.
    :param path:this is the path to the image file used
    :return: returns a python dictionary that contains metadata
    """
    # Psuedo code procedure
    # 1. Check if path exists
    # 2. If it doesn't exist , add an error to Strelka scanner instance
    # 3. If it does , open the file and extract contents
    # 4. Call `parse_jpeg_from_data` with contents
    # 5. Return results of function call

    file_exists = os.path.exists(path)

    if file_exists:
        # print(file_exists)
        # begins the process of reading and parsing metadata
        image = Image.open(path)

        exifdata = image._getexif()

        parse_jpeg_from_data(exifdata)
    else:
        raise Exception("Invalid path")

    # try:
    #     if file_exists:
    #         print(file_exists)
    # except:
    #     ErrorHandling.PathError

    # return dict()

def parse_jpeg_from_data(data: bytes) -> dict:
    """
    This function will take the data of a JPEG image file as input and produce a dictionary from the requested list of metadata fields.
    :param data:this is the data to the image file used
    :return: returns a python dictionary that contains metadata
    """
    # fields are currently case sensitive
    desired_fields = [
        "GPSInfo",
        "ExifImageHeight",
        "ExifImageWidth",
        "ExifVersion",
        "Make",
        "Model",
        "Software",
        "UserComment",
        "DateTime",
        "SecurityClassification",
        "ExpandSoftware",
        "Saturation",
        "ImageHistory",
        "ImageNumber",
        "Pressure",
        "FlashEnergy",
        "Noise",
        "ImageNumber",
        "LensMake"
    ]

    # Psuedo code procedure
    # 1. Validate data is JPEG data
    # 2. .....
    # return dict()
    jpeg_parsed = dict()
    exif_table = dict()

    for tag, value in data.items():
        decoded = TAGS.get(tag, tag)
        exif_table[decoded] = value

        temp = dict()
    # iterating over all EXIF data fields
    for tag_id in data:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        readable_data = data.get(tag_id)
        temp[tag] = readable_data
        # decode bytes

    #print(f"searching for fields {desired_fields}")
    #print(f"existing fields {list(temp.keys())}")
    # insert conditional to print only fields in file from list to dictionary
    # reversed logic
    for tag in desired_fields:
        if tag in temp.keys():
            jpeg_parsed[tag] = temp[tag]

    #print("dictionary:", jpeg_parsed)
    #print(f"found {len(jpeg_parsed)} fields out of {len(desired_fields)}")

    return print(jpeg_parsed)

# if __name__ == "__main__":
#     print(argv)
#     result = parse_jpeg_from_path(argv[1])
#     print(result)

parse_jpeg_from_path(argv[1])
