@echo off
:: BatchGotAdmin
::-------------------------------------
REM  --> Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"="
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
::--------------------------------------
echo ------- Running download script -------
tasklist /fi "ImageName eq trilium.exe" /fo csv 2>NUL | find /I "trilium.exe">NUL
if "%ERRORLEVEL%"=="0" ( echo [Warn] - A Trilium process is still running. Aborting... & pause & exit 1 )
echo [Info] - Checking for Python 3.9 at %LocalAppData%\Programs\Python\Python39
if exist %LocalAppData%\Programs\Python\Python39\python.exe (
    set python=%LocalAppData%\Programs\Python\Python39\python.exe
    echo [Info] - Found Python 3.9
    goto exec_script
) else (
    echo [Warn] - Python 3.9 wasn't found.
)
echo [Info] - Checking for Python 3.10 at %LocalAppData%\Programs\Python\Python310
if exist %LocalAppData%\Programs\Python\Python310\python.exe (
    set python=%LocalAppData%\Programs\Python\Python310\python.exe
    echo [Info] - Found Python 3.10
    goto exec_script
) else (
    echo [Error] - No Python installation was found at %LocalAppData%\Programs\Python\
    echo [Info] - Aborting...
    pause & exit /B 1
)
:exec_script
%python% "%~dp0\updater.py"
if errorlevel 2 ( echo [Error] - Script stopped with exit code %errorlevel%. & pause & exit /B %errorlevel% )
if %errorlevel% == 1 ( pause & exit /B 0 )
if %errorlevel% == -1073741510 ( echo [Warn] - Keyboard interuption detected. Aborting... & pause & exit /B %errorlevel% )
echo [Info] - Removing old files
RMDIR /S /Q "C:\Program Files\trilium-windows-x64"
echo [Info] - Moving new files
MOVE /Y "%tmp%\trilium-windows-x64" "C:\Program Files\"
echo Updated successfully.
pause
