@echo off
cd /d "D:\YouTube select topic"
set HTTP_PROXY=http://127.0.0.1:7897
set HTTPS_PROXY=http://127.0.0.1:7897
start http://localhost:5000
C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe app.py
pause
