class GroundStationException(Exception):
    """
    Generic Ground Station Exception. This class and its subclasses indicate
    conditions that an application might want to catch.
    All functionality of this class is the inherited of `Exception
    <https://docs.python.org/2/library/exceptions.html?highlight=exceptions.exception#exceptions.Exception>`_.
    """
    pass


class RadioException(GroundStationException):
    """
    This exception will be thrown when there is a problem encountered with the XBee-radio.
    All functionality of this class is the inherited of `Exception
    <https://docs.python.org/2/library/exceptions.html?highlight=exceptions.exception#exceptions.Exception>`_.
    """
    pass


class RadioSerialConnectionException(RadioException):
    """
    This exception will be thrown if there is a problem with the physical USB connection with the Ground Station.
    All functionality of this class is the inherited of `Exception
    <https://docs.python.org/2/library/exceptions.html?highlight=exceptions.exception#exceptions.Exception>`_.
    """
    __DEFAULT_MESSAGE = "Error with the serial connection to the radio. Check the USB connections."

    def __init__(self, message=__DEFAULT_MESSAGE):
        super().__init__(message)


class RadioObjectException(RadioException):
    """
    This exception will be thrown if there is an issue with calling the radio object.
    All functionality of this class is the inherited of `Exception
    <https://docs.python.org/2/library/exceptions.html?highlight=exceptions.exception#exceptions.Exception>`_.
    """
    __DEFAULT_MESSAGE = "The radio object being called is of type None."
    print(__DEFAULT_MESSAGE)
    pass

    # def __init__(self, message=__DEFAULT_MESSAGE):
    #     super().__init__(message)


class QueueException(GroundStationException):
    """
    This exception will be thrown if there is a problem with the data queue for the display and logging of all data.
    All functionality of this class is the inherited of `Exception
    <https://docs.python.org/2/library/exceptions.html?highlight=exceptions.exception#exceptions.Exception>`_.
    """
    __DEFAULT_MESSAGE = "There is a problem with the data queue."

    def __init__(self, message=__DEFAULT_MESSAGE):
        super().__init__(message)
