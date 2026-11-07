#使用官方Python3.14 slim镜像作为基础
FROM python:3.14-slim

#设置工作目录
WORKDIR /app

#先复制依赖清单，利用Docker层缓存
COPY requirements.txt .

#安装依赖，使用国内源
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

#复制项目代码
COPY app/ ./app/

#创建非root用户运行应用
RUN useradd --create-home --shell /bin/bash appuser
RUN mkdir -p /app/data && chown -R appuser:appuser /app
USER appuser

#声明对外暴露端口
EXPOSE 8000

#启动命令
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


