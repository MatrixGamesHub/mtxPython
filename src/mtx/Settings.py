

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
