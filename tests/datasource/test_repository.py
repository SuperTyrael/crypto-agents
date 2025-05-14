import pytest
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.datasource.repositories.datasource import DataSourceRepository
from app.datasource.models.datasource import DataSource
from app.datasource.models.market import News

# 创建测试数据库引擎
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

@pytest.fixture
async def session():
    """创建测试会话"""
    async with engine.begin() as conn:
        # 创建所有表
        await conn.run_sync(DataSource.metadata.create_all)
        await conn.run_sync(News.metadata.create_all)
    
    async with async_session() as session:
        yield session
    
    async with engine.begin() as conn:
        # 清理所有表
        await conn.run_sync(News.metadata.drop_all)
        await conn.run_sync(DataSource.metadata.drop_all)

@pytest.fixture
async def repository(session):
    """创建仓储实例"""
    return DataSourceRepository(session)

@pytest.fixture
async def test_source(session):
    """创建测试数据源"""
    source = DataSource(
        name="test_source",
        type="news",
        is_active=True,
        last_fetch_at=datetime.utcnow()
    )
    session.add(source)
    await session.commit()
    return source

@pytest.mark.asyncio
async def test_get_by_name(repository, test_source):
    """测试根据名称获取数据源"""
    # 测试获取存在的源
    source = await repository.get_by_name("test_source")
    assert source is not None
    assert source.name == "test_source"
    assert source.is_active is True

    # 测试获取不存在的源
    source = await repository.get_by_name("non_existent")
    assert source is None

@pytest.mark.asyncio
async def test_get_active_sources(repository, test_source):
    """测试获取活跃数据源"""
    sources = await repository.get_active_sources()
    assert len(sources) == 1
    assert sources[0].name == "test_source"

@pytest.mark.asyncio
async def test_save_news(repository, test_source):
    """测试保存新闻数据"""
    # 准备测试数据
    news_list = [
        {
            "title": "测试新闻1",
            "content": "内容1",
            "link": "http://test1.com",
            "publishTime": datetime.utcnow(),
            "type": "push",
            "source": "test_source",
            "status": "pending"
        },
        {
            "title": "测试新闻2",
            "content": "内容2",
            "link": "http://test2.com",
            "publishTime": datetime.utcnow(),
            "type": "push",
            "source": "test_source",
            "status": "pending"
        }
    ]

    # 保存新闻
    await repository.save_news(news_list, "test_source")

    # 验证保存结果
    async with repository.session as session:
        saved_news = await session.execute(select(News))
        news = saved_news.scalars().all()
        assert len(news) == 2
        assert news[0].title == "测试新闻1"
        assert news[1].title == "测试新闻2"

@pytest.mark.asyncio
async def test_save_news_duplicate(repository, test_source):
    """测试保存重复新闻"""
    # 准备测试数据
    news_list = [
        {
            "title": "测试新闻",
            "content": "内容",
            "link": "http://test.com",
            "publishTime": datetime.utcnow(),
            "type": "push",
            "source": "test_source",
            "status": "pending"
        }
    ]

    # 第一次保存
    await repository.save_news(news_list, "test_source")
    
    # 第二次保存相同新闻
    await repository.save_news(news_list, "test_source")

    # 验证结果
    async with repository.session as session:
        saved_news = await session.execute(select(News))
        news = saved_news.scalars().all()
        assert len(news) == 1  # 应该只有一条记录

@pytest.mark.asyncio
async def test_update_source_status(repository, test_source):
    """测试更新数据源状态"""
    old_time = test_source.last_fetch_at
    await repository.update_source_status("test_source")
    
    # 验证更新时间
    async with repository.session as session:
        source = await session.get(DataSource, test_source.id)
        assert source.last_fetch_at > old_time

@pytest.mark.asyncio
async def test_save_news_without_link(repository, test_source):
    """测试保存没有链接的新闻"""
    news_list = [
        {
            "title": "测试新闻",
            "content": "内容",
            "publishTime": datetime.utcnow(),
            "type": "push",
            "source": "test_source",
            "status": "pending"
        }
    ]

    await repository.save_news(news_list, "test_source")

    # 验证保存结果
    async with repository.session as session:
        saved_news = await session.execute(select(News))
        news = saved_news.scalars().all()
        assert len(news) == 1
        assert news[0].title == "测试新闻"
        assert news[0].link == ""  # 链接应该为空字符串