@echo off
echo 正在清理 Python 缺存...
for /d /r . %%d in (__pycache__) do @rmdir /s /q "%%d" 2>nul
del /s /q *.pyc 2>nul
echo 清理完成！
echo.
echo 正在启动程序...
python main.py
pause
