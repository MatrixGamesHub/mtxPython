.. mtxPython documentation master file, created by
   sphinx-quickstart on Thu Oct 13 09:37:17 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to mtxPython documentation
==================================

What is mtxPython?
   This framework provides the ability to quickly and easily create games based on a
   two-dimensional matrix like Sokoban_, Bomberman_ or maze puzzles in general. The playing
   field consists of rows and columns, and each intersection is defined by a cell. Each cell can
   contain objects (walls, items, players, opponents, etc.) that represent the structure of the
   game.
   
Why it is written in Python?
   mtxPython is written in Python 3 so it can be used with MicroPython_ on a pyboard_.

.. _Sokoban: https://en.wikipedia.org/wiki/Sokoban
.. _Bomberman: https://en.wikipedia.org/wiki/Bomberman
.. _MicroPython: http://micropython.org/
.. _pyboard: http://docs.micropython.org/en/latest/pyboard/pyboard/quickref.html

   
.. toctree::
   :maxdepth: 1
   :caption: Contents

   game.rst
   objects.rst
   api/apiReference.rst


* :ref:`genindex`

