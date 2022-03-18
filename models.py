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
    
    fields_validated = validate_fields(jpeg_parsed)
    
    json_object = json.dumps(jpeg_parsed, indent=4)
    # print(json_object)

    return json_object

def serialize_jpeg_data(unserialized_data: dict) -> dict:
    """
        This function takes in a dictionary of jpeg data and checks if the key and value pairs are 
        acceptable data types to be converted to json. If they are not, they are serialized(converted to strings).
        The serialized dictionary is returned.

    """
            
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
    

def validate_fields(serialized_data: dict, additional_fields: dict = dict()):
    """
            This function takes in serialized data as a dictionary and validates that each data field (key)
            has a value of the desired data type. If the type is not correct we cast it to the correct type.
            If the value is not parseable to the correct data type then we delete that field from the
            dictionary completely. We return the validated fields.

        """
    dict_desired_fields = {
        "gpsinfo": dict,
        "exifimageheight": int,
        "exifimagewidth": int,
        "exifversion": str,
        "make": str,
        "model": str,
        "software": str,
        "usercomment": str,
        "datetime": str,
        "securityclassification": str,
        "expandsoftware": str,
        "saturation": int,
        "imagehistory": str,
        "imagenumber": int,
        "pressure": str,
        "flashenergy": str,
        "noise": str,
        "imagenumber": int,
        "lensmake": str
    }

    dict_desired_fields.update(additional_fields)

    # TODO : check if each value can be an int or float, if so parse
    # assigning types in dictionary takes care of this
    # TODO : check if the field we are looking for is the correct data type
    # possibly compare the k,v (type of v) in unserialized_data to the k,v in dict_desired_fields
    validated_data = dict()
    
    """ validate based on desired fields """
    # loop through desired fields
    # check to see if the key in serialized data
    # if not, skip field
    # if so, check that the value of desired fields matches the type of the value in serialized data
    # if not, try to cast the value to the correct type
    # else if it is correct, pass
    # if it can't be done, delete field from dictionary
    
    for k,v in dict_desired_fields.items():
        
        if k in serialized_data.keys():
            if not isinstance(serialized_data.get(k),v):
                try:
                    new_value = v(serialized_data.get(k))
                except:
                    del serialized_data[k]
                else:
                    validated_data[k] = new_value
            else:
                validated_data[k] = serialized_data.get(k)
            print("For key ", k, "serialized data type: ", 
                     type(serialized_data.get(k)), " desired type: ", v)
        else:
            # no validation needs to be done because the field doesnt exist
            pass
    
    """ validate based on serialized data """
    # loop through serialized data
    # check to see if serialized data is in desired fields
    # if not, delete the field
    # if so, check that the value of desired fields matches the type of the value in serialized data
    # if not, try to cast the value to the correct type
    # else if it is correct, pass
    # if it can't be done, delete field from dictionary
    
    # for k, v in serialized_data.items():
    #      new_value = v
    #      # if the value of the iteration is a string
    #      if isinstance(v, str):
    #        print("Here is ", k)
    #        print("For key ", k, "serialized data type: ", 
    #              type(serialized_data.get(v)), " desired type: ", dict_desired_fields.get(k))
           
    #        #if the type of the value doesnt equal the type specified in desired fields
    #        if not isinstance(serialized_data.get(v), dict_desired_fields.get(k)) :
               
    #            # try to cast the values to a string
    #             try:
    #                 new_value = str(v)
                    
    #             # if you cant cast to proper type, delete from dictionary
    #             except Exception:
    #                 print("The data for ", k,
    #                           "could not be converted to a string")
    #                 del serialized_data[k]
                    
    #      elif isinstance(v, int):
    #          print("For key ", k,"serialized data type: ", 
    #                type(serialized_data.get(v)), " desired type: ", dict_desired_fields.get(k))
    #          if type(serialized_data.get(v)) != dict_desired_fields.get(k):
    #               try:
    #                   new_value = int(v)
    #               except Exception:
    #                   print("The data for ", k,
    #                             "could not be converted to an int")
    #                   del serialized_data[k]
    #      elif isinstance(v, dict):
    #          pass
    #      else:
    #          pass
    #          # del serialized_data[k]
    #      validated_data[k] = new_value
    print(validated_data)

if __name__ == "__main__":
    result = parse_jpeg_from_path(argv[1])
    print(result)
