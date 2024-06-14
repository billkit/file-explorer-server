#!/bin/bash

# 定义应用程序文件路径
APP_PATH="app.py"

# 检查应用程序文件是否存在
if [ ! -f "$APP_PATH" ]; then
    echo "Error: $APP_PATH 文件不存在"
    exit 1
fi

# 后台运行应用程序，并将输出重定向到日志文件
nohup python3 "$APP_PATH" > app.log 2>&1 &

# 输出提示信息
echo "应用程序在后台运行中，日志文件位于 $(pwd)/app.log"