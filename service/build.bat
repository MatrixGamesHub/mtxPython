cls
set thriftExe=.\bin\thrift-0.10.0-rc0.exe
set mtxRendererServiceDefinition=MtxRendererService.thrift
set mtxControllerServiceDefinition=MtxControllerService.thrift
set distDir=.\dist

:: --------------------------

if exist %distDir% rd /q /s %distDir%

mkdir %distDir%
mkdir %distDir%\Python
mkdir %distDir%\C#

call %thriftExe% -out %distDir%\Python --gen py %mtxRendererServiceDefinition%
call %thriftExe% -out %distDir%\Python --gen py %mtxControllerServiceDefinition%
call %thriftExe% -out %distDir%\C# --gen csharp:union %mtxRendererServiceDefinition%
call %thriftExe% -out %distDir%\C# --gen csharp:union %mtxControllerServiceDefinition%
