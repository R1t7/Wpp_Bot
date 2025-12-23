@echo off
REM ====================================================================
REM Script de execução do Bot de WhatsApp para Windows
REM ====================================================================

REM Mudar para o diretório do script
cd /d "%~dp0"

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

REM Executar o bot
python main.py

REM Desativar ambiente virtual
deactivate

REM Sair
exit
