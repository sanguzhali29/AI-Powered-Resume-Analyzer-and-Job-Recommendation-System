@echo off
title Create Desktop Shortcut
echo Creating desktop shortcut for AI Resume Analyzer...

set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
set TARGET=%~dp0START_PROJECT.bat
set SHORTCUT=%USERPROFILE%\Desktop\AI_Resume_Analyzer.lnk

echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%SHORTCUT%" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%TARGET%" >> %SCRIPT%
echo oLink.WorkingDirectory = "%~dp0" >> %SCRIPT%
echo oLink.Description = "Launch AI Resume Analyzer Application" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript /nologo %SCRIPT%
del %SCRIPT%

echo.
echo ======================================================================
echo  [SUCCESS] Desktop Shortcut created successfully on your Desktop!
echo  Icon Name: AI_Resume_Analyzer
echo ======================================================================
echo.
pause
