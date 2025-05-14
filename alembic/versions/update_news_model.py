"""update news model

Revision ID: update_news_model
Revises: init_database
Create Date: 2024-03-13 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'update_news_model'
down_revision: Union[str, None] = 'init_database'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 创建新的 news_data 表
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


def downgrade() -> None:
    # 删除索引
    op.drop_index('idx_news_status', table_name='news_data')
    op.drop_index('idx_news_source', table_name='news_data')
    op.drop_index('idx_news_create_time', table_name='news_data')
    
    # 删除表
    op.drop_table('news_data') 