@echo off

REM Use PowerShell to retrieve the clipboard text and encode it for URL
for /f "delims=" %%A in ('powershell -command "$clip = Get-Clipboard; $clip"') do set "clipboard=%%A"

REM Use curl to send the encoded content to the server
python3 C:\Users\User\MEGA\send_message.py -t %clipboard%

pause
