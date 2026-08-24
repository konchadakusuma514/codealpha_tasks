@echo off
title CyberShield SOC Analytics Web Platform
echo Starting CyberShield Web Server & Launching in Chrome...
cd /d "%~dp0"
py app.py || python app.py
pause
