@echo off

set "containerName=cyberp/master:cpu-stable"
set imageName=master
set port=8228
set memory=200mb
set PWD=%~dp0

set foo=%*

set t=%foo%
:loop
for /f "tokens=1*" %%a in ("%t%") do (
   set t=%%b
   for /f "tokens=1,2 delims=:" %%g in ("%%a") do set %%g=%%h
)
if defined t goto :loop

@docker inspect --format='{{.Config.Image}}' %imageName%
if errorlevel 1 (
    @REM If errorlevel == 1, so container doesn't exist, creating new
    start cmd /c launch_subworkers.bat
    timeout 15
    docker run --net ml-bridge --name %imageName% -m %memory% -p %port%:80  %containerName%
) else (
    @REM Else run attached container by name
    start cmd /c docker start --attach %imageName%
    docker start --attach DET_EMOTION_MODEL
)