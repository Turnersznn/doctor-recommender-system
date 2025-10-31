@echo off
echo Starting Doctor Recommender System...
echo.

echo 1. Starting ML Service (Port 8000)...
start "ML Service" cmd /k "cd ml-doctor-recommender && python simple_api.py"
timeout /t 3

echo 2. Starting Backend Server (Port 5000)...
start "Backend" cmd /k "cd doctor-recommender-backend && node server.js"
timeout /t 3

echo 3. Starting Frontend (Port 3000)...
start "Frontend" cmd /k "cd doctor-recommender-frontend && npm start"

echo.
echo All services are starting...
echo.
echo Services:
echo - ML API: http://127.0.0.1:8000
echo - Backend: http://localhost:5000  
echo - Frontend: http://localhost:3000
echo.
echo Wait a few seconds for all services to start, then open http://localhost:3000
pause
