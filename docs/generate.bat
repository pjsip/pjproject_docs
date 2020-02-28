@echo off

echo Checking doxygen availability..
doxygen -h >NUL 2>NUL
if errorlevel 1 (
    echo Error: doxygen is not found. Please follow required s/w installation in the doc.
    exit /b 1
)


echo Checking breathe-apidoc availability..
breathe-apidoc -h >NUL 2>NUL
if errorlevel 1 (
    echo Error: breathe-apidoc is not found. Please follow required s/w installation in the doc.
    exit /b 1
)


PUSHD source\pjproject\pjlib
doxygen docs\doxygen.cfg
if errorlevel 1 goto error
POPD

PUSHD source\pjproject\pjlib-util
doxygen docs\doxygen.cfg
if errorlevel 1 goto error
POPD

PUSHD source\pjproject\pjnath
doxygen docs\doxygen.cfg
if errorlevel 1 goto error
POPD

PUSHD source\pjproject\pjmedia
doxygen docs\doxygen.cfg
if errorlevel 1 goto error
POPD

PUSHD source\pjproject\pjsip
doxygen docs\doxygen.cfg
if errorlevel 1 goto error
POPD

MKDIR source\api
ECHO breathe-apidoc pjlib..
breathe-apidoc -f -p pjlib -o source\api\generated\pjlib source\pjproject\pjlib\docs\xml
if errorlevel 1 goto error

ECHO breathe-apidoc pilib_util..
breathe-apidoc -f -p pilib_util -o source\api\generated\pilib_util source\pjproject\pjlib-util\docs\xml
if errorlevel 1 goto error

ECHO breathe-apidoc pjnath..
breathe-apidoc -f -p pjnath -o source\api\generated\pjnath source\pjproject\pjnath\docs\xml
if errorlevel 1 goto error

ECHO breathe-apidoc pjmedia..
breathe-apidoc -f -p pjmedia -o source\api\generated\pjmedia source\pjproject\pjmedia\docs\xml
if errorlevel 1 goto error

ECHO breathe-apidoc pjsip..
breathe-apidoc -f -p pjsip -o source\api\generated\pjsip source\pjproject\pjsip\docs\xml
if errorlevel 1 goto error


echo Success
goto quit

:error
echo Aborting..
goto quit

:quit
