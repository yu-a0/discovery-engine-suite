@echo off
title Discovery Engine Launcher
:menu
cls
echo ===========================================
echo       SELECT YOUR DISCOVERY ENGINE
echo ===========================================
echo.
echo  [1] Movie Discovery Engine (TMDB)
echo  [2] Anime Discovery Engine (AniList)
echo  [3] Exit
echo.
echo ===========================================
set /p choice="Enter your choice (1, 2, or 3): "

if "%choice%"=="1" goto movies
if "%choice%"=="2" goto anime
if "%choice%"=="3" exit

:movies
echo Launching Movie Engine...
call venv\Scripts\activate
python gui_app.py
goto menu

:anime
echo Launching Anime Engine...
call venv\Scripts\activate
python anime_app.py
goto menu