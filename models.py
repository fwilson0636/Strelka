import logging
from sys import argv
#from PIL import Image
from exif import Image
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
        with open(path, 'rb') as image_file:
            image = Image(image_file)
        #exifdata = image._getexif()
        print("I am here")
        jpeg_data = parse_jpeg_from_data_using_exif(image)
        coords = image_coordinates(image)
        if coords:
            jpeg_data["gps_coords"] = coords
        image = Image.open(path)
        exifdata = image._getexif()
        jpeg_data = parse_jpeg_from_data(exifdata)

    except OSError as ose:
        print("Found OSError", ose)
        jpeg_scanner.tags.append("File does not exist")
    except Exception as e:
        logging.exception("Found exception")
        jpeg_scanner.tags.append(e)
    else:
        print("Success")
    finally:
        print("Completed")

    # print("Scanner errors:", jpeg_scanner.tags)
    return jpeg_data

def decimal_coords(coords, ref):
 decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
 if ref == "S" or ref == "W":
     decimal_degrees = -decimal_degrees
 return decimal_degrees

def image_coordinates(img):

    if img.has_exif:
        try:
            coords = (decimal_coords(img.gps_latitude,
                      img.gps_latitude_ref),
                      decimal_coords(img.gps_longitude,
                      img.gps_longitude_ref))
            return coords
        except AttributeError:
            print('No Coordinates')
    else:
        print ('The Image has no EXIF information')

def parse_jpeg_from_data_using_exif(image:bytes) -> dict:
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
    image_data = dict()
    jpeg_parsed = dict()
    if image.has_exif:
        for field in image.list_all():
            try:
                image_data[field] = str(image.__getattr__(field))
            except Exception as e:
                image_data[field] = str(e)

            # insert conditional to print only fields in file from list to dictionary
            # reversed logic
        field_count = 0
        for tag in desired_fields:
            # convert desired fields to lowercase
            tag = tag.lower()
            if tag in image_data.keys():
                jpeg_parsed[tag] = image_data[tag]
                field_count = field_count + 1
            if field_count == 0:
                print("This may be a malicious image file")
            else:
                print("The field (", tag, ") is not available for this jpeg.")

    return jpeg_parsed

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
    #temp = {if isinstance(k,str) k.lower() else str(): v for k, v in temp.items() }
    temp_dict = dict()

    for k,v in temp.items():
        if isinstance(k,str):
            k=k.lower()
        temp_dict[k] = v
    temp = temp_dict
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

    return jpeg_parsed

def serialize_jpeg_data(unserialized_data: dict) -> dict:
    """
        This function takes in a dictionary of jpeg data and checks if the key and value pairs are 
        acceptable data types to be converted to json. If they are not, they are serialized(converted to strings).
        The serialized dictionary is returned.

    """
    # TODO : check if each value can be an int or float, if so parse 
    # TODO : check if the field we are looking for is the correct data type
    if isinstance(unserialized_data, dict) :
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
    else :
        print("Expected a dictionary type,", type(unserialized_data), "was received.")
        return dict()
    

if __name__ == "__main__":
    result = parse_jpeg_from_path(argv[1])
    print(result)
