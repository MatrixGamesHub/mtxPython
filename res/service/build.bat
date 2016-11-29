cls
set thriftExe=.\bin\thrift-0.10.0-rc0.exe
set rendererServiceDefinition=RendererService.thrift
set controllerServiceDefinition=ControllerService.thrift
set distDir=.\dist

:: --------------------------

if exist %distDir% rd /q /s %distDir%

mkdir %distDir%
mkdir %distDir%\Python
mkdir %distDir%\C#

call %thriftExe% -out %distDir%\Python --gen py %rendererServiceDefinition%
call %thriftExe% -out %distDir%\Python --gen py %controllerServiceDefinition%
call %thriftExe% -out %distDir%\C# --gen csharp:union %rendererServiceDefinition%
call %thriftExe% -out %distDir%\C# --gen csharp:union %controllerServiceDefinition%
