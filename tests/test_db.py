import pytest
import asyncio
from src.core.database import db

@pytest.mark.asyncio
async def test_db_connection():
    await db.create_pool()
    assert db.pool is not None
    await db.close_pool()