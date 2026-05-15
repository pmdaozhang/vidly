@echo off
D:
cd "D:\YouTube select topic"
echo Searching YouTube for: 心理学 情绪 成长
echo.
C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe cli.py 心理学 情绪 成长 --time "last week" -m 5
echo.
if %ERRORLEVEL% NEQ 0 (
    echo Error occurred. Trying alternative approach...
    C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe cli.py 心理学 --time "last week" -m 5
)
pause
