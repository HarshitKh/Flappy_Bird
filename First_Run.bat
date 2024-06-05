@echo off
echo.
color A
echo Installing Required modules ....
pip install -r r.txt
echo.
echo The modules have been installed
timeout /t 1
cls
echo.
echo Converting to EXE ....
pyinstaller --onefile --icon=icon.ico "Flappy Bird.py"
echo.
echo Converted to EXE
timeout /t 1
echo Type Y if you want to open your game, else, press N to exit
set /p input=Enter your choice:
if "%input%"=="Y" (
    echo Playing your game ....
    cd dist
    start "" "Flappy Bird.exe"
) else if "%input%"=="N" (
    exit
) else if "%input%"=="y" (
    echo Playing your game ....
    cd dist
    start "" "Flappy Bird.exe"
) else if "%input%"=="n" (
    echo Exiting....
    exit
) else (
    echo Invalid choice
)
