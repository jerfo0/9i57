@echo off
chcp 65001 >nul
cd /d I:\网站备份\9i57

echo [1/3] 拉取远程最新内容...
git pull origin source
if %errorlevel% neq 0 (
    echo 错误：git pull 失败，请检查网络或手动解决冲突
    pause
    exit /b 1
)

echo [2/3] 添加新文件...
git add src/
git status

echo [3/3] 提交并推送...
git commit -m "新增博客文章 %date%"
git push origin source

if %errorlevel% equ 0 (
    echo.
    echo ✓ 推送成功！文章已发布到 GitHub。
) else (
    echo.
    echo ✗ 推送失败，请检查网络连接。
)
pause
