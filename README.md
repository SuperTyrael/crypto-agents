# 加密货币分析服务

基于 Python 的加密货币市场分析服务，集成了实时数据采集、技术指标计算和 LLM 分析功能。

## 功能特点

- 实时市场数据采集（Binance API）
- 技术指标计算（pandas-ta）
- LLM 市场分析（OpenAI API）
- 数据持久化（PostgreSQL + TimescaleDB）
- RESTful API 接口（FastAPI）
- 异步任务调度（APScheduler）

## 技术栈

- Python 3.12+
- FastAPI
- SQLAlchemy
- APScheduler
- LangChain
- PostgreSQL + TimescaleDB
- Docker

## 快速开始

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/crypto-agents.git
cd crypto-agents
```

2. 创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置信息
```

5. 启动服务：
```bash
# 开发模式
python -m app.scheduler

# 或使用 Docker
docker-compose up -d
```

## 项目结构

```
app/
├── core/           # 核心功能模块
├── jobs/           # 异步任务
├── api/            # API 接口
├── models/         # 数据模型
└── scheduler.py    # 任务调度器
```

## 开发指南

1. 代码风格
- 使用 Black 进行代码格式化
- 使用 isort 进行导入排序
- 使用 flake8 进行代码检查

2. 测试
```bash
pytest
```

3. 数据库迁移
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## 许可证

MIT 