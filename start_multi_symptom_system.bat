@echo off
echo Starting Doctor Recommender System...
echo.

echo Starting Multi-Symptom API on port 8005...
start "Multi-Symptom API" cmd /k "cd ml-doctor-recommender && python ml_multi_symptom_api.py"

timeout /t 3 /nobreak > nul

echo Starting Backend Server on port 5000...
start "Backend Server" cmd /k "cd doctor-recommender-backend && npm start"

timeout /t 3 /nobreak > nul

echo Starting Frontend Server on port 3000...
start "Frontend Server" cmd /k "cd doctor-recommender-frontend && npm start"

echo.
echo All services are starting...
echo.
echo Multi-Symptom API: http://localhost:8005
echo Backend Server: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo CHANGES MADE:
echo - Removed Multi-Symptom section from navigation
echo - Fixed dashboard loading and error handling
echo - Added sample data for empty dashboards
echo - Enhanced ML predictions display
echo.
echo Press any key to exit...
pause > nul
