
from .. import BaseObject


class RemovableObject(BaseObject):

    def IsRemovable(self):
        """
        Returns:
            True if the object is removable, False otherwise.
        """
        return True

    def RemoveOnEnter(self):
        return True
