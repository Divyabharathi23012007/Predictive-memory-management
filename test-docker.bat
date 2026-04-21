@echo off
echo 🐳 Testing Docker Setup for MemOS...
echo ==================================

echo 🚀 Starting Docker services...
docker-compose up -d

echo.
echo ⏱️ Waiting for services to start...
timeout /t 10 /nobreak >nul

echo.
echo 🔍 Checking Backend health...
curl -f -s http://localhost:8000/ >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend is healthy!
    echo 📊 Backend API Response:
    curl -s http://localhost:8000/
    echo.
) else (
    echo ❌ Backend failed to become healthy
)

echo 🔍 Checking Frontend health...
curl -f -s http://localhost:3000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Frontend is healthy!
    echo 🌐 Frontend Health Response:
    curl -s http://localhost:3000/health
    echo.
) else (
    echo ❌ Frontend failed to become healthy
)

echo.
echo 🎉 Docker setup test completed!
echo.
echo 📱 Access your application:
echo    Frontend: http://localhost:3000
echo    Backend:  http://localhost:8000
echo.
echo 🛠️ Useful commands:
echo    View logs: docker-compose logs -f
echo    Stop:      docker-compose down
echo    Restart:   docker-compose restart
pause
