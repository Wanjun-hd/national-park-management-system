@echo off
echo ========================================
echo 国家公园管理系统 - 后端服务
echo National Park Management System - Backend
echo ========================================
echo.

cd /d %~dp0

echo [1/3] 激活虚拟环境...
call venv\Scripts\activate.bat

echo [2/3] 检查配置...
python manage.py check
if errorlevel 1 (
    echo.
    echo 配置检查失败！请检查数据库连接和配置文件。
    pause
    exit /b 1
)

echo.
echo [3/3] 启动开发服务器...
echo.
echo 服务器地址: http://127.0.0.1:8000
echo API 文档: http://127.0.0.1:8000/api/docs/
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

python manage.py runserver

pause
