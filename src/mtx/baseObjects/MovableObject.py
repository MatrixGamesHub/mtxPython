"""
    mtxPython - A framework to create matrix games.
    Copyright (C) 2016  Tobias Stampfl <info@matrixgames.rocks>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation in version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

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
