
from .. import BaseObject


class CollectableObject(BaseObject):

    def IsCollectable(self):
        """
        Returns:
            True if the object is collectable, False otherwise.
        """
        return True
