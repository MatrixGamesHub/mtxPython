
from . import Constants, Cell, GameConsole


class Field():
    """
    Class to manage a two-dimensional game field. The field consists of rows and columns, and each
    intersection is represented by a :class:`cell<mtx.Cell>`.
    """

    def __init__(self, width, height):
        """
        Parameters:
            width (:obj:`int`): The width of the field.
            height (:obj:`int`): The height of the field.
        """
        self._width = width
        self._height = height
        self._cells = None

        self._CreateCells()

    def __repr__(self):
        return 'mtx.Field(%r, %r)' % (self._width, self._height)

    def __iter__(self):
        for row in self._cells:
            for cell in row:
                yield cell

    def _CreateCells(self):
        self._cells = []

        for y in range(self._height):
            row = []
            for x in range(self._width):
                row.append(Cell(self, x, y))

            self._cells.append(row)

    def Clear(self):
        """
        Removes all objects from all cells.
        """
        self._CreateCells()

    def GetSize(self):
        """
        Returns:
            :obj:`tuple`: The size of the field.
        """
        return (self._width, self._height)

    def GetWidth(self):
        """
        Returns:
            :obj:`int`: The width of the field.
        """
        return self._width

    def GetHeight(self):
        """
        Returns:
            :obj:`int`: The height of the field.
        """
        return self._height

    def GetCell(self, x, y):
        """
        Parameters:
            x (:obj:`int`): The x-coordinate in the field.
            y (:obj:`int`): The y-coordinate in the field.

        Returns:
            :class:`mtx.Cell` or :obj:`None`: The cell at the given position or None if none
            exists.
        """

        if x < 0 or x >= self._width or\
           y < 0 or y >= self._height:
           return None

        return self._cells[y][x]
