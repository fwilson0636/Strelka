class Error(Exception):
    """Base class for other exceptions"""
    pass


class PathError(Error):
    """Exception error for invalid file path"""
    print("Invalid file path")
