ECHO OFF
schtasks.exe > NUL
IF %ERRORLEVEL% EQU 0 (
    ECHO you are Administrator
    ECHO continue....
) ELSE (
    ECHO you are NOT Administrator. Exiting...
    PING 127.0.0.1 > NUL 2>&1
    EXIT /B 1
)

REM download/install python
REM unzip your code package
REM unzip quizbot.zip
SET ZZ=BOT

IF EXIST "C:\Program Files\7-Zip\7z.exe" (
   SET ZZ=C:\Program Files\7-Zip\7z.exe
   REM ECHO 7z has already been installed
)

IF "%ZZ%" == "BOT" (
   echo installing 7z ...
   echo run 7z1900-x64.msi
   SET ZZ=C:\Program Files\7-Zip\7z.exe
)


REM ECHO %USERPROFILE%\Desktop
ECHO %ZZ% x quizbot.zip -o%USERPROFILE%\Desktop\quizbot
ECHO quizbot is installed on your desktop %USERPROFILE%\Desktop\quizbot
ECHO execute the quizbot shortcut from %USERPROFILE%\Desktop\quizbot
ECHO 
wmic bios get serialnumber | findstr /V SerialNumber
echo Send the above serial number to quizbot@gmail.com
echo
echo You may try running this program once you complete the installation
echo However, you need to acquire a new installation package in order to use the bot
echo Thanks...
echo


