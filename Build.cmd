@PUSHD %~dp0
@SET PYTHON=C:\PythonVirtualEnv\MatrixGames\Scripts\python.EXE
@IF NOT EXIST %PYTHON% GOTO ERROR


:RUN
@CALL Clean.cmd
%PYTHON% Setup.py sdist --formats=gztar,zip bdist_wheel egg_info
@GOTO DONE


:ERROR
@ECHO ON
@ECHO.
@ECHO You need the python virtual environment. Please visit http://www.matrixgames.rocks/developers.php
@ECHO OFF
@GOTO DONE


:DONE
@POPD
