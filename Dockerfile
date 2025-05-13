FROM python:3.12-slim

WORKDIR /opt/app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 创建数据目录
RUN mkdir -p /opt/app/data

# 设置环境变量
ENV PYTHONPATH=/opt/app
ENV PYTHONUNBUFFERED=1

# 运行应用
CMD ["python", "-m", "app.scheduler"] 