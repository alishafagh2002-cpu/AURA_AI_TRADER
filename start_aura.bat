@echo off

cd /d C:\Users\Pars Pardazesh\Desktop\AURA_AI_TRADER\backend

call venv\Scripts\activate

start "AURA BOT" python telegram_bot.py

start "AURA SCHEDULER" python scheduler.py

exit