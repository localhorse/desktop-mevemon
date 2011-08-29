""" This module contains all our input validation functions """
from constants import MIN_VCODE_SIZE, MAX_VCODE_SIZE

class ValidationError(StandardError):
    """ Exception that is raised if input validation fails
    """
    def __init__(self, message):
        StandardError.__init__(self)
        self.message = message

    def __str__(self):
        return repr(self.message)



def validate_kid(kid):
    """ Validates an EVE key ID. throws ValidationError exception if
        the format is invalid.
    """
    # I don't know enough about the keyID yet. seems to be only numeric.
    # The 2 I made were 705 and 706 respectively. I think they are
    # just incrementing numbers. But I won't assume that yet...
    
    pass


def validate_vcode(vcode):
    """ Validates an EVE Online verification code, throws
        ValidationError exception if the format is invalid.
    """
    # What we DO know about the vcode is that it has to be
    # at least 20 digits and at most 64. Seems to be
    # alphanumeric only.

    if len(vcode) < MIN_VCODE_SIZE or len(vcode) > MAX_VCODE_SIZE:
        raise ValidationError("Verification code must be from 20 to 64 "
                              "characters.")
    # too much? --danny
    ##elif not vcode.isalnum():
    ##    raise ValidationError("Verification code must contain only "
    ##                          "alphanumeric characters.")

