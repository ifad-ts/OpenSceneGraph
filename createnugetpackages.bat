rem Build native OpenSceneGraphIFAD NuGet package(s).
rem Requires nuget.exe, cmake.exe in the path and the Visual Studio x64 setup (vcvarsall.bat x86_amd64)
rem Also requires a Nuget feed containing the dependent packages (most easily setup from within Visual Studio
rem as that setup is picked up by the command-line nuget.exe)

rem get dependencies
set OSGVISUALVER=10.0.2
nuget install -OutputDirectory packages -Version %OSGVISUALVER% osgvisual-3rdparty-full

rem re-construct osgvisual-3rdparty structure so that the OpenSceneGraph 3rdparty location scripts can detect the files
set OSGVISUALTEMP=packages\osgvisual-3rdparty-temp\x64
rem rmdir /s /q %OSGVISUALTEMP%
rem mkdir %OSGVISUALTEMP%
robocopy /s /NFL /NDL packages\osgvisual-3rdparty-full.%OSGVISUALVER%\build\native\include %OSGVISUALTEMP%\include
rem mkdir %OSGVISUALTEMP%\lib
robocopy /NFL packages\osgvisual-3rdparty-full.%OSGVISUALVER%\build\native\lib\x64\v120\Debug\Desktop %OSGVISUALTEMP%\lib\
robocopy /NFL packages\osgvisual-3rdparty-full.%OSGVISUALVER%\build\native\lib\x64\v120\Release\Desktop %OSGVISUALTEMP%\lib\

rem build OpenSceneGraph debug and release
call nugetbuild.bat debug
call nugetbuild.bat release

rem build the nuget packages
PowerShell -Command "& {Write-NugetPackage OpenSceneGraphIFAD.autopkg}"
