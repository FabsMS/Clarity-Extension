@echo off
echo ============================================
echo Limpando cache do Ollama
echo ============================================

echo.
echo Parando Ollama...
taskkill /F /IM ollama.exe 2>nul
timeout /t 2 >nul

echo.
echo Limpando cache...
rd /s /q "%USERPROFILE%\.ollama\cache" 2>nul
rd /s /q "%TEMP%\ollama" 2>nul

echo.
echo Reiniciando Ollama...
start "" "C:\Users\%USERNAME%\AppData\Local\Programs\Ollama\ollama.exe" serve

echo.
echo ============================================
echo Cache limpo! Aguarde 5 segundos...
echo ============================================
timeout /t 5

echo.
echo Pronto! Execute o Clarity novamente.
pause
