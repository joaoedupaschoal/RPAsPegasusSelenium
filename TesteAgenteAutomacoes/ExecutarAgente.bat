@echo off
setlocal

rem ====== (opcional) defina a senha só para este atalho ======
set "APP_PASS=123456"

rem ====== pasta raiz do projeto ======
set "ROOT=C:\RPASelenium\RPAsPegasusSelenium"

rem ====== script principal (sem acentos) ======
set "MAIN=%ROOT%\TesteAgenteAutomacoes\TesteAgenteAutomacoes.py"

if not exist "%MAIN%" (
  echo [ERRO] Nao encontrei o arquivo:
  echo        %MAIN%
  echo.
  pause
  exit /b 1
)

cd /d "%ROOT%"

rem tenta 'py -3', se nao houver, usa 'python'
where py >nul 2>nul && ( set "PY=py -3" ) || ( set "PY=python" )

%PY% "%MAIN%"
if errorlevel 1 (
  echo.
  echo [ERRO] Script retornou codigo %errorlevel%
)
echo.
pause
