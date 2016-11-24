Objects
=======

Objects are things that can be placed on a :class:`cell<mtx.Cell>`.

Base Objects
------------

There are 4 different base objects every object must inherit from. Each of these base objects has
different characteristics and must follow certain rules.

:class:`Solid Object<mtx.baseObjects.SolidObject>`
    An object that **can not be moved, removed or collected** by any other object and no other 
    object can be placed on a :class:`cell<mtx.Cell>`, on which a solid object is located.

:class:`Movable Object<mtx.baseObjects.MovableObject>`
    An object that **can be moved but not be removed or collected** by any other object.
    A :class:`cell<mtx.Cell>` can only contain one
    :class:`movable object<mtx.baseObjects.MovableObject>`. The only objects that can be placed on
    a :class:`cell<mtx.Cell>` with a :class:`movable object<mtx.baseObjects.MovableObject>` at the
    same time are :class:`collectable objects<mtx.baseObjects.CollectableObject>` and/or
    :class:`removable objects<mtx.baseObjects.RemovableObject>`.

:class:`Collectable Object<mtx.baseObjects.CollectableObject>`
    An object that can be collected by an :class:`movable object<mtx.baseObjects.MovableObject>`
    if it is accepted. When an :class:`movable object<mtx.baseObjects.MovableObject>` steps on a
    :class:`cell<mtx.Cell>` with a :class:`collectable object<mtx.baseObjects.CollectableObject>`,
    the :class:`OnCollect<mtx.Game.OnCollect>` method of the :class:`game<mtx.Game>` object is
    called. If it returns True, the :class:`collectable object<mtx.baseObjects.CollectableObject>`
    is accepted and will be removed, otherwise it remains on the :class:`cell<mtx.Cell>`. There can
    be more than one :class:`collectable object<mtx.baseObjects.CollectableObject>` on the same
    :class:`cell<mtx.Cell>`. In this case **all of them will be collected** if they are accepted.

:class:`Removable Object<mtx.baseObjects.RemovableObject>`
    An object that will be removed by an :class:`movable object<mtx.baseObjects.MovableObject>` if
    it is accepted. The :class:`RemoveOnEnter<mtx.baseObjects.RemovableObject.RemoveOnEnter>`
    method of the :class:`removable object<mtx.baseObjects.RemovableObject>` decides, whether it
    will be removed by entering or leaving. The :class:`OnRemove<mtx.game.OnRemove>` method of the
    :class:`game<mtx.Game>` object is called. If it returns True, the
    :class:`removable object<mtx.baseObjects.RemovableObject>` is accepted and will be removed,
    otherwise it remains on the :class:`cell<mtx.Cell>`. There can be more than one
    :class:`collectable object<mtx.baseObjects.CollectableObject>` on the same
    :class:`cell<mtx.Cell>` In this case **only the top most will be removed** if it is accepted.
    
:class:`Trigger Object<mtx.baseObjects.TriggerObject>`
    An object that triggers an event when another object enters or leaves the
    :class:`cell<mtx.Cell>` with the :class:`trigger object<mtx.baseObjects.TriggerObject>`. On
    :class:`cell<mtx.Cell>` entering, the :class:`OnTriggerEnter<mtx.Game.OnTriggerEnter>` method
    is called, on :class:`cell<mtx.Cell>` leaving, the 
    :class:`OnTriggerLeave<mtx.Game.OnTriggerLeave>` method.


Available Objects
-----------------

+--------+-------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Symbol | Name                                      | Description                                                                                                                                                             |
+========+===========================================+=========================================================================================================================================================================+
| 1-8    | :class:`Player<mtx.objects.Player>`       | A :class:`movable object<mtx.baseObjects.MovableObject>` that represents a player in the game. There must be at least one player and there may be up to 8 players,      |
|        |                                           | but each number may only occur once.                                                                                                                                    |
+--------+-------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| #      | :class:`Wall<mtx.objects.Wall>`           | A :class:`solid object<mtx.baseObjects.SolidObject>` that can be used to build the structure of a game level.                                                           |
+--------+-------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| \-     | :class:`Empty<mtx.objects.Empty>`         | A :class:`solid object<mtx.baseObjects.SolidObject>` that marks the cell as empty. No ground is drawn in this cell.                                                     |
+--------+-------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| b      | :class:`Box<mtx.objects.Box>`             | A :class:`movable object<mtx.baseObjects.MovableObject>` that represents a wooden box.                                                                                  |
+--------+-------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t      | :class:`Target<mtx.objects.Target>`       | A :class:`trigger object<mtx.baseObjects.TriggerObject>` that represents a destination for another object.                                                              |
+--------+-------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| \+     | :class:`Tile<mtx.objects.Tile>`           | A :class:`removable object<mtx.baseObjects.RemovableObject>` a player can walk on and that is removed as soon as the player leaves it.                                  |
+--------+-------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| .      | :class:`Dot<mtx.objects.Dot>`             | A :class:`collectable object<mtx.baseObjects.CollectableObject>` that represents a PacDot that can be collected by a player.                                            |
+--------+-------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
                                                                                                                                                                                                                               
                                                                                                                                                                                                                               
Available Multi Objects                                                                                                                                                                                                        
-----------------------                                                                                                                                                                                                        
                                                                                                                                                                                                                               
+--------+-------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Symbol | Replacement                               | Description                                                                                                                                                             |
+========+===========================================+=========================================================================================================================================================================+
| B      | tb                                        | A :class:`Box<mtx.objects.Box>` on a :class:`Target<mtx.objects.Target>`.                                                                                               |
+--------+-------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| \*     | \+\+                                      | Two :class:`Tiles<mtx.objects.Tile>`.                                                                                                                                   |
+--------+-------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| %      | \+\+\+                                    | Three :class:`Tiles<mtx.objects.Tile>`.                                                                                                                                 |
+--------+-------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| @      | \+1                                       | :class:`Player 1<mtx.objects.Player>` on a :class:`Tile<mtx.objects.Tile>`.                                                                                             |
+--------+-------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
