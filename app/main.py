import asyncio
import uvicorn
from fastapi import FastAPI
from app.scheduler import JobScheduler
from app.core.config import settings

app = FastAPI(title="Crypto Agents API")

async def start_services():
    # 启动调度器
    scheduler = JobScheduler()
    await scheduler.start()
    
    # 启动API服务器
    config = uvicorn.Config(
        app=app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(start_services()) 