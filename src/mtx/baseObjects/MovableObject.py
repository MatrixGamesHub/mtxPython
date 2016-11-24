
from .. import BaseObject


class MovableObject(BaseObject):
    """
    A movable object can be moved to a neighboring cell if possible, but it can not be removed or
    collected.
    It can be moved directly or through another, neighboring object.
    """

    def IsMovable(self):
        """
        Returns:
            True if the object is movable, False otherwise.
        """
        return True

    def IsMovableByObject(self):
        """
        Returns:
            True if the object can be moved by another object, False otherwise.
        """
        return True
