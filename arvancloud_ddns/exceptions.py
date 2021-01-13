class ArvanCloudError(Exception):
    """
    Base exception for ArvanCloud module
    """
    pass

class ZoneNotFound(ArvanCloudError):
    """
    Raised when a specified zone is not found from ArvanCloud
    """
    pass

class RecordNotFound(ArvanCloudError):
    """
    Raised when a specified record is not found for a zone from ArvanCloud
    """
    pass
