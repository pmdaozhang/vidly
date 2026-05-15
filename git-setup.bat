@echo off
cd /d D:\YouTube select topic
git init
git add -A
git commit -m "init: Vidly - YouTube topic research tool"
echo.
echo --- Now create GitHub repo and run: ---
echo git remote add origin git@github.com:pmdaozhang/vidly.git
echo git push -u origin main
pause
