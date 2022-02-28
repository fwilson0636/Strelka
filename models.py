from sys import argv
from PIL import Image
from PIL.ExifTags import TAGS
from strelka.strelka import Scanner
import json


def parse_jpeg_from_path(path: str) -> dict:
    """
    This function will take the path of a JPEG image file as input and produce a dictionary from the requested list of metadata fields.
    :param path:this is the path to the image file used
    :return: returns a python dictionary that contains metadata
    """
    # Pseudo code procedure
    # 1. Check if path exists
    # 2. If it doesn't exist , add an error to Strelka scanner instance
    # 3. If it does , open the file and extract contents
    # 4. Call `parse_jpeg_from_data` with contents
    # 5. Return results of function call
    jpeg_scanner = Scanner()
    jpeg_data = dict()

    try:
        # begins the process of reading and parsing metadata
        image = Image.open(path)
        exifdata = image._getexif()
        print("I am here")
        jpeg_data = parse_jpeg_from_data(exifdata)
    except OSError as ose:
        print("Found OSError", ose)
        jpeg_scanner.tags.append("File does not exist")
    except Exception as e:
        print("Found exception", e)
        jpeg_scanner.tags.append(e)
    else:
        print("Success")
    finally:
        print("Completed")

    # print("Scanner errors:", jpeg_scanner.tags)
    return jpeg_data


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

    # Pseudo code procedure
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
        

    # print(f"searching for fields {desired_fields}")
    # print(f"existing fields {list(temp.keys())}")
     

   
    
    # convert all keys (exifdata fields) to lowercase
    temp = {k.lower(): v for k, v in temp.items()}
    
    field_count = 0
    
    # insert conditional to print only fields in file from list to dictionary
    # reversed logic
    for tag in desired_fields:
        # convert desired fields to lowercase
        tag = tag.lower()
        if tag in temp.keys():
            jpeg_parsed[tag] = temp[tag]
            field_count = field_count + 1
        else:
            print("The field (", tag, ") is not available for this jpeg.")
            
    # calculate the percentage of desired fields found in the jpeg    
    field_percentage = round(field_count/19 * 100)        
    print("Jpeg contains", field_percentage, "% of desired fields.")
    
    # print("dictionary:", jpeg_parsed)
    # del jpeg_parsed["gpsinfo"]
    # del jpeg_parsed["usercomment"]
    # del jpeg_parsed["exifversion"]
    # for k,v in jpeg_parsed.items():
    #     if k == "gpsinfo":
    #         for i,j in v.items():
    #             print(type(i), type(j), i, j)
    #     else:
    #         print(type(k),type(v),k,v)
    # print(f"found {len(jpeg_parsed)} fields out of {len(desired_fields)}")
    jpeg_parsed = serialize_jpeg_data(jpeg_parsed)
    
    json_object = json.dumps(jpeg_parsed, indent=4)
    # print(json_object)

    return json_object

def serialize_jpeg_data(unserialized_data: dict) -> dict:
    """
        This function takes in a dictionary of jpeg data and checks if the key and value pairs are 
        an acceptable data types to be converted to json. If they are not, they are serialized(converted to strings).
        The serialized dictionary is returned.

    """
    # TODO : check if correct data type is passed in
    serialized_data = dict()
    valid_key_types = str
    valid_value_types = tuple([str,dict,bool,int,float,list])
    for k,v in unserialized_data.items() :
        new_key = k
        new_value = v
        if not isinstance(k,valid_key_types) :
            new_key = str(k)
        if isinstance(v,bytes) :
            new_value = v.decode("utf-8")
        if not isinstance(v, valid_value_types) or v is None :
            new_value = str(v)
        if isinstance(v,dict) :
            new_value = serialize_jpeg_data(v)
        serialized_data[new_key] = new_value
    return serialized_data
    

if __name__ == "__main__":
    result = parse_jpeg_from_path(argv[1])
    print(result)
