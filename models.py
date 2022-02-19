from sys import argv


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
    return dict()


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
    return dict()



if __name__ == "__main__":
    print(argv)
    result = parse_jpeg_from_path(argv[1])
    print(result)
