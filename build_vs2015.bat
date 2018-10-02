rem rmdir /s /q build
rem rmdir /s /q install


CALL :RESOLVE "." CMAKE_DIR
CALL :RESOLVE "install" INSTALLDIR
CALL :RESOLVE "..\osg-3rdparty-cmake\download\install\msvc140\3rdParty.x64" THIRDPARTY

CALL :MKANDPUSHD build

..\..\cmake-3.5.1-win32-x86\bin\cmake.exe -G "Visual Studio 14 2015 Win64" ^
-D ACTUAL_3RDPARTY_DIR=%THIRDPARTY% ^
-D TIFF_LIBRARY=%THIRDPARTY%/lib/libtiff.lib ^
-D TIFF_LIBRARY_DEBUG=%THIRDPARTY%/lib/libtiffd.lib ^
-D GIFLIB_LIBRARY=%THIRDPARTY%/lib/libgif.lib ^
-D GIFLIB_LIBRARY_DEBUG=%THIRDPARTY%/lib/libgifd.lib ^
-D CURL_IS_STATIC=OFF ^
-D CMAKE_INSTALL_PREFIX=%INSTALLDIR% ^
-D WIN32_USE_MP=ON ^
-D CMAKE_CXX_FLAGS_RELEASE:STRING="/MD /O2 /Ob2 /D NDEBUG /Zi /Oy-" ^
-D CMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="/DEBUG /OPT:REF /OPT:ICF /INCREMENTAL:NO" ^
-D CMAKE_EXE_LINKER_FLAGS_RELEASE:STRING="/DEBUG /OPT:REF /OPT:ICF /INCREMENTAL:NO" ^
-D CMAKE_MODULE_LINKER_FLAGS_RELEASE:STRING="/DEBUG /OPT:REF /OPT:ICF /INCREMENTAL:NO" ^
%CMAKE_DIR%

call "%VS140COMNTOOLS%\..\..\VC\vcvarsall.bat" x86_amd64
devenv.com OpenSceneGraph.sln /build Release /Project INSTALL
devenv.com OpenSceneGraph.sln /build Debug /Project INSTALL

pause
GOTO :EOF


:RESOLVE
SET TEMPRESOLVE=%~f1
SET "%2=%TEMPRESOLVE:\=/%"
GOTO :EOF

:MKANDPUSHD
IF NOT EXIST %1 ( mkdir %1 )
pushd %1 || exit 
GOTO :EOF
