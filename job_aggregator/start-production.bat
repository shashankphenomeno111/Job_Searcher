@echo off
echo ========================================
echo  Job Searcher - Production Build
echo ========================================
echo.
echo Building React application...
echo.

call npm run build

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Build failed! Please check the errors above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Build completed successfully!
echo ========================================
echo.
echo Starting production server...
echo.

python app.py

pause
