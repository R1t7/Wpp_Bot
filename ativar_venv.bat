@echo off
REM Script para ativar o ambiente virtual
cd /d "%~dp0"
call venv\Scripts\activate.bat
echo.
echo ========================================
echo Ambiente virtual ativado!
echo ========================================
echo.
echo Comandos disponiveis:
echo   python main.py --setup      - Configurar bot
echo   python main.py --first-run  - Login WhatsApp
echo   python main.py --test       - Testar envio
echo   python main.py              - Enviar mensagem
echo.
cmd /k
