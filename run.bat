@echo off
title Chaoxing Auto Evaluator
python --version >nul 2>&1 || (echo Python not found! & pause & exit /b 1)
pip show selenium >nul 2>&1 || pip install selenium webdriver-manager >nul 2>&1
python "%~dp0auto_evaluate.py"
pause