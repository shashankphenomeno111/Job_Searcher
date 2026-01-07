@echo off
echo ========================================
echo  Job Searcher - Development Mode
echo ========================================
echo.
echo Starting Flask Backend Server...
echo.

start "Flask Backend" python app.py

timeout /t 3 /nobreak >nul

echo Starting React Frontend (Vite)...
echo.

start "React Frontend" npm run dev

echo.
echo ========================================
echo  Both servers are starting...
echo ========================================
echo.
echo Flask Backend: http://localhost:5000
echo React Frontend: http://localhost:5173
echo.
echo Open http://localhost:5173 in your browser
echo.
echo Press any key to stop all servers...
pause >nul

taskkill /FI "WINDOWTITLE eq Flask Backend*" /T /F
taskkill /FI "WINDOWTITLE eq React Frontend*" /T /F

echo.
echo Servers stopped.
pause
