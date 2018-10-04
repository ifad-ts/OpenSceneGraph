set NAME=OpenSceneGraph

CALL :RESOLVE "packages\osgvisual-3rdparty-temp" OSG_3RDPARTY_DIR

set CURRENT_DIR=%CD%
CALL :RESOLVE "target\nugetinstall\%1" INSTALLDIR
CALL :MKANDPUSHD target\nugetbuild

cmake -G "Visual Studio 12 Win64" ^
-D OSG_USE_QT=OFF ^
-D COLLADA_INCLUDE_DIR= ^
-D CMAKE_INSTALL_PREFIX=%INSTALLDIR% ^
-D WIN32_USE_MP=ON ^
-D CMAKE_CXX_FLAGS_RELEASE:STRING="/MD /O2 /Ob2 /D NDEBUG /Zi /Oy-" ^
-D CMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="/DEBUG /OPT:REF /OPT:ICF /INCREMENTAL:NO" ^
-D CMAKE_EXE_LINKER_FLAGS_RELEASE:STRING="/DEBUG /OPT:REF /OPT:ICF /INCREMENTAL:NO" ^
-D CMAKE_MODULE_LINKER_FLAGS_RELEASE:STRING="/DEBUG /OPT:REF /OPT:ICF /INCREMENTAL:NO" ^
%CURRENT_DIR% || GOTO :EOF 

devenv.com %NAME%.sln /build %1 /Project INSTALL || GOTO :EOF
popd
for /r %INSTALLDIR% %%p in (*.dll) do (
	for /f "delims=" %%i in ('dir target\nugetbuild\bin\%%~np.pdb /b /s') do ( xcopy /y %%~dpnxi  %%~dpp )
)

GOTO :EOF


:RESOLVE
SET TEMPRESOLVE=%~f1
SET "%2=%TEMPRESOLVE:\=/%"
GOTO :EOF

:MKANDPUSHD
IF NOT EXIST %1 ( mkdir %1 )
pushd %1 || exit 
GOTO :EOF
