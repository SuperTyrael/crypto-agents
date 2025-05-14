"""init database

Revision ID: init_database
Revises: 
Create Date: 2024-05-13 15:30:00

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'init_database'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # 创建数据源表
    op.create_table(
        'data_sources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('type', sa.String(20), nullable=False),
        sa.Column('api_url', sa.String(200), nullable=False),
        sa.Column('api_key', sa.String(), nullable=True),
        sa.Column('api_secret', sa.String(), nullable=True),
        sa.Column('config', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('fetch_interval', sa.Integer(), nullable=False, server_default='300'),
        sa.Column('last_fetch_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # 创建新闻数据表
    op.create_table(
        'news_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False, comment='新闻标题'),
        sa.Column('content', sa.Text(), nullable=False, comment='新闻内容'),
        sa.Column('link', sa.String(length=500), nullable=False, comment='新闻链接'),
        sa.Column('create_time', sa.DateTime(), nullable=False, comment='新闻创建时间'),
        sa.Column('type', sa.String(length=50), nullable=False, comment='新闻类型'),
        sa.Column('source', sa.String(length=50), nullable=False, comment='数据来源'),
        sa.Column('summary', sa.Text(), nullable=True, comment='新闻摘要'),
        sa.Column('sentiment', sa.String(length=20), nullable=True, comment='情感分析结果'),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='pending', comment='处理状态'),
        sa.Column('processed_at', sa.DateTime(), nullable=True, comment='处理时间'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), comment='记录创建时间'),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP'), comment='记录更新时间'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建索引
    op.create_index('idx_news_create_time', 'news_data', ['create_time'])
    op.create_index('idx_news_source', 'news_data', ['source'])
    op.create_index('idx_news_status', 'news_data', ['status'])

def downgrade():
    op.drop_table('news_data')
    op.drop_table('data_sources') 