
from .. import BaseObject


class SolidObject(BaseObject):
    """
    A solid object can not be moved, removed or collected.
    No other object can be moved to a cell where a solid object is placed.
    """

    def IsSolid(self):
        """
        Returns:
            True if the object is solid, False otherwise.
        """
        return True
