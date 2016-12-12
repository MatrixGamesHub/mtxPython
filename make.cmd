@ECHO OFF

PUSHD %~dp0
SET BUILD_DIR=build
SET DIST_DIR=dist
SET DOC_DIST_DIR=%DIST_DIR%\doc
SET SERVICE_DIST_DIR=%DIST_DIR%\service
SET SERVICE_DIST_DIR_PYTHON=%SERVICE_DIST_DIR%\Python
SET SERVICE_DIST_DIR_CSHARP=%SERVICE_DIST_DIR%\CSharp
SET SERVICE_DIR=res\service

SET PYTHON=C:\PythonVirtualEnv\MatrixGames\Scripts\python.EXE
SET SPHINX_BUILD=C:\PythonVirtualEnv\MatrixGames\Scripts\sphinx-build.exe
SET THRIFT=%SERVICE_DIR%\bin\thrift-0.10.0-rc0.exe

SET SERVICE_RENDERER=%SERVICE_DIR%\RendererService.thrift
SET SERVICE_CONTROLLER=%SERVICE_DIR%\ControllerService.thrift
SET SERVICE_DEST_DIR=src\mtxNet
SET SPHINX_OPTS=-d %BUILD_DIR%\doctrees doc\source

IF NOT EXIST %PYTHON% CALL :ERROR_ENV
IF NOT EXIST %SPHINX_BUILD% CALL :ERROR_ENV

IF ERRORLEVEL 1 GOTO DONE

IF "%1" == "" CALL :HELP
IF "%1" == "all" CALL :ALL
IF "%1" == "lib" CALL :LIB
IF "%1" == "service" CALL :SERVICE
IF "%1" == "services" CALL :SERVICE
IF "%1" == "doc" CALL :DOC
IF "%1" == "clean" CALL :CLEAN


:DONE
    IF ERRORLEVEL 1 (
        ECHO build faulty
    ) ELSE (
        ECHO build successful
    )
    POPD
    EXIT /B %ERRORLEVEL%

::--------------------------------------------------------------------------------------

:ERROR_ENV
    ECHO.
    ECHO You need the python virtual environment. Please visit http://www.matrixgames.rocks/developers.php
    EXIT /B 1


:ERROR_CLEAN
    ECHO.
    ECHO Could not clean up the environment. Make sure that the build and dist directories are not in use.
    EXIT /B 1


:HELP
    ECHO.Please use `Make ^<target^>` where ^<target^> is one of
    ECHO.  all        clean up environment and build all targets
    ECHO.  lib        builds the documentation
    ECHO.  service    builds the thrift services
    ECHO.  doc        builds the documentation
    ECHO.  clean      clean up environment
    ECHO.
    EXIT /B 0


:ALL
    CALL :CLEAN
    CALL :CREATE_ENV_BASE
    CALL :CREATE_ENV_DOC
    CALL :CREATE_ENV_SERVICE
    CALL :BUILD_SERVICE
    CALL :BUILD_LIB
    CALL :BUILD_DOC
    CALL :CLEAN_BUILD
    EXIT /B %ERRORLEVEL%


:LIB
    CALL :CLEAN
    CALL :CREATE_ENV_BASE
    CALL :BUILD_LIB
    CALL :CLEAN_BUILD
    EXIT /B %ERRORLEVEL%


:SERVICE
    CALL :CLEAN
    CALL :CREATE_ENV_BASE
    CALL :CREATE_ENV_SERVICE
    CALL :BUILD_SERVICE
    CALL :CLEAN_BUILD
    EXIT /B %ERRORLEVEL%


:DOC
    CALL :CLEAN
    CALL :CREATE_ENV_BASE
    CALL :CREATE_ENV_DOC
    CALL :BUILD_DOC
    CALL :CLEAN_BUILD
    EXIT /B %ERRORLEVEL%


:CLEAN
    IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%
    ECHO [ clean up ... ]
    FOR /D %%f in ("src\*.egg-info", %DIST_DIR%, %BUILD_DIR%) DO IF EXIST %%f RD /s /q "%%f"
    FOR /D /R . %%f in (__pycache__) DO IF EXIST %%f RD /s /q "%%f"

    IF EXIST %BUILD_DIR% CALL :ERROR_CLEAN
    IF EXIST %DIST_DIR% CALL :ERROR_CLEAN

    IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%

    ECHO [ clean up done ]
    ECHO.
    EXIT /B %ERRORLEVEL%


:CLEAN_BUILD
    IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%
    ECHO [ clean build directory ... ]
    FOR /D %%f in (%BUILD_DIR%) DO IF EXIST %%f RD /s /q "%%f"
    ECHO [ clean build directory done ]
    ECHO.
    EXIT /B %ERRORLEVEL%


:CREATE_ENV_BASE
    IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%
    ECHO [ create build environment ... ]
    IF NOT EXIST %BUILD_DIR% MKDIR %BUILD_DIR%
    IF NOT EXIST %DIST_DIR% MKDIR %DIST_DIR%
    EXIT /B %ERRORLEVEL%


:CREATE_ENV_DOC
    IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%
    IF NOT EXIST %DOC_DIST_DIR% MKDIR %DOC_DIST_DIR%
    EXIT /B %ERRORLEVEL%


:CREATE_ENV_SERVICE
    IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%
    IF NOT EXIST %SERVICE_DIST_DIR% MKDIR %SERVICE_DIST_DIR%
    IF NOT EXIST %SERVICE_DIST_DIR_PYTHON% MKDIR %SERVICE_DIST_DIR_PYTHON%
    IF NOT EXIST %SERVICE_DIST_DIR_CSHARP% MKDIR %SERVICE_DIST_DIR_CSHARP%
    EXIT /B %ERRORLEVEL%


:BUILD_LIB
    IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%
    ECHO [ build lib ... ]
    CALL %PYTHON% setup.py sdist --formats=gztar,zip bdist_wheel egg_info
    COPY src\mtxPython.egg-info\PKG-INFO %DIST_DIR%\PKG-INFO
    ECHO [ build lib done ]
    ECHO.
    EXIT /B %ERRORLEVEL%


:BUILD_SERVICE
    IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%
    ECHO [ build thrift services ... ]
    CALL %THRIFT% -out %SERVICE_DIST_DIR_PYTHON% --gen py %SERVICE_RENDERER%
    CALL %THRIFT% -out %SERVICE_DIST_DIR_PYTHON% --gen py %SERVICE_CONTROLLER%
    CALL %THRIFT% -out %SERVICE_DIST_DIR_CSHARP% --gen csharp:union %SERVICE_RENDERER%
    CALL %THRIFT% -out %SERVICE_DIST_DIR_CSHARP% --gen csharp:union %SERVICE_CONTROLLER%

    ECHO [ copy thrift services to mtxNet... ]
    IF EXIST %SERVICE_DEST_DIR%\controllerService RD /s /q %SERVICE_DEST_DIR%\controllerService
    IF EXIST %SERVICE_DEST_DIR%\rendererService RD /s /q %SERVICE_DEST_DIR%\rendererService

    XCOPY /S /I /Y %SERVICE_DIST_DIR_PYTHON%\ControllerService %SERVICE_DEST_DIR%\controllerService
    XCOPY /S /I /Y %SERVICE_DIST_DIR_PYTHON%\RendererService %SERVICE_DEST_DIR%\rendererService

    ECHO [ build thrift services done ]
    ECHO.
    EXIT /B %ERRORLEVEL%


:BUILD_DOC
    IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%

    ECHO [ build doc ... ]
    CALL %SPHINX_BUILD% -b html %SPHINX_OPTS% %BUILD_DIR%\html
    IF ERRORLEVEL 1 GOTO BUILD_DOC_DONE

    MOVE /Y %BUILD_DIR%\html %DIST_DIR%\doc\html

    ECHO [ build doc done ]
    ECHO.
    :BUILD_DOC_DONE
    EXIT /B %ERRORLEVEL%
