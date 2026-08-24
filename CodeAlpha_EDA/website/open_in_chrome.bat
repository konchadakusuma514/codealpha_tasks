@echo off
title Launching CyberShield in Chrome
echo =======================================================
echo   Opening CyberShield SOC Analytics Dashboard in Chrome
echo =======================================================
start chrome "%~dp0index.html" || start "" "%~dp0index.html"
exit
