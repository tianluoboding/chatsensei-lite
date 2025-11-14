@echo off
REM ChatSensei Lite 启动脚本 (Windows)

echo ======================================
echo   ChatSensei Lite 启动中...
echo ======================================
echo.

REM 检查虚拟环境
if not exist "venv\" (
    echo 警告：虚拟环境不存在，正在创建...
    python -m venv venv
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 检查依赖
echo 检查依赖...
pip list | findstr /C:"fastapi" >nul
if errorlevel 1 (
    echo 警告：依赖缺失，正在安装...
    pip install -r requirements.txt
)

REM 显示配置信息
echo.
echo 配置信息:
if "%OPENAI_API_KEY%"=="" (
    echo   • OpenAI API: 未设置 (将使用启发式方法^)
) else (
    echo   • OpenAI API: 已配置
)

echo.
echo ======================================
echo   服务器启动于: http://127.0.0.1:8000
echo   按 Ctrl+C 停止服务器
echo ======================================
echo.

REM 启动服务器
uvicorn app:app --host 127.0.0.1 --port 8000 --reload

pause

