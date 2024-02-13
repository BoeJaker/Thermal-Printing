@echo off

REM Use PowerShell to retrieve the clipboard text and encode it for URL
for /f "delims=" %%A in ('powershell -command "$clip = Get-Clipboard; [uri]::EscapeDataString($clip)"') do set "encoded_clipboard=%%A"

REM Use curl to send the encoded content to the server
curl -X GET "http://192.168.3.201:12345/print/%encoded_clipboard%"

pause
