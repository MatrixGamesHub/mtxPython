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

class Settings():
    def __init__(self):
        self.preferedSize = None
        """
        The prefered size of the playing field.
        A program that renders the surface will always try to keep this size. If no size is
        specified, then the client will specify a size.
        """

        self.centerSmalerLevels = True
        """
        If the renderer has a fixed size, but a level is smaller, then this setting determines
        whether the level should be centered or drawn in the upper left corner.
        """

        self.cellAccessWhitelist = None
        """
        List of object symbols of which at least one must be present in a cell to grant access.
        If the value is None (default), there is no whitelist check.
        """

        self.cellAccessBlacklist = None
        """
        List of object symbols, none of which may be present in the cell to grant access.
        If the value is None (default), there is no blacklist check.
        """
