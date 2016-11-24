Create your own game
====================

Creating your own game is very easy. Each game simply needs to inherit from :class:`mtx.Game` and
must override a few required methods. Furthermore, there are many event methods that can optionally
be overridden to implement the game logic.

The following section shows all methods that can or should be overridden.


Methods and Events
------------------

Overwriting required:
    * :ref:`GetNextLevel<GetNextLevel>`

Overwriting recommended:
    * :ref:`GetDescription<GetDescription>`
    * :ref:`OnInit<OnInit>`

Overwriting optional (game dependent):
    * :ref:`GetMaxPlayers<GetMaxPlayers>`
    * :ref:`GetName<GetName>`
    * :ref:`OnCollect<OnCollect>`
    * :ref:`OnIdle<OnIdle>`
    * :ref:`OnLevelStart<OnLevelStart>`
    * :ref:`OnPlayerJumpRequest<OnPlayerJumpRequest>`
    * :ref:`OnPlayerMoveRequest<OnPlayerMoveRequest>`
    * :ref:`OnRemove<OnRemove>`
    * :ref:`OnShutdown<OnShutdown>`
    * :ref:`OnTriggerEnter<OnTriggerEnter>`
    * :ref:`OnTriggerLeave<OnTriggerLeave>`


Game related
~~~~~~~~~~~~

.. _GetName:
.. automethod:: mtx.Game.GetName
    :noindex:

.. _GetDescription:
.. automethod:: mtx.Game.GetDescription
    :noindex:

.. _GetMaxPlayers:
.. automethod:: mtx.Game.GetMaxPlayers
    :noindex:

.. _OnInit:
.. automethod:: mtx.Game.OnInit
    :noindex:

.. _OnShutdown:
.. automethod:: mtx.Game.OnShutdown
    :noindex:

.. _OnIdle:
.. automethod:: mtx.Game.OnIdle
    :noindex:


Level related
~~~~~~~~~~~~~

.. _GetNextLevel:
.. automethod:: mtx.Game.GetNextLevel
    :noindex:

.. _OnLevelStart:
.. automethod:: mtx.Game.OnLevelStart
    :noindex:


Movement related
~~~~~~~~~~~~~~~~

.. _OnPlayerMoveRequest:
.. automethod:: mtx.Game.OnPlayerMoveRequest
    :noindex:

.. _OnPlayerJumpRequest:
.. automethod:: mtx.Game.OnPlayerJumpRequest
    :noindex:


Event related
~~~~~~~~~~~~~

.. _OnTriggerEnter:
.. automethod:: mtx.Game.OnTriggerEnter
    :noindex:

.. _OnTriggerLeave:
.. automethod:: mtx.Game.OnTriggerLeave
    :noindex:

.. _OnCollect:
.. automethod:: mtx.Game.OnCollect
    :noindex:

.. _OnRemove:
.. automethod:: mtx.Game.OnRemove
    :noindex:

