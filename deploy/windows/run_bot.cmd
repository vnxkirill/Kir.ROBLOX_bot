@echo off
rem GameCore AI — запуск бота с автоперезапуском при падении.
rem Используется задачей планировщика Windows (см. deploy/windows/README.md).

cd /d "%~dp0..\.."

:loop
echo [%date% %time%] Запуск GameCore AI... >> logs\runner.log
uv run python -m app.main >> logs\runner.log 2>&1
echo [%date% %time%] Бот остановился (код %errorlevel%), перезапуск через 5 сек... >> logs\runner.log
timeout /t 5 /nobreak > nul
goto loop
