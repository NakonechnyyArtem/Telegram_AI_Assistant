from src.core.database import db

async def create_user(user_id: int, username: str, first_name: str):
    await db.add_user(user_id, username, first_name)

async def get_user(user_id: int):
    return await db.get_user(user_id)

async def update_user_name(user_id: int, new_name: str):
    async with db.pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE users 
            SET first_name = $1, last_activity = CURRENT_TIMESTAMP
            WHERE user_id = $2
            """,
            new_name, user_id
        )

async def get_user_stats(user_id: int):
    async with db.pool.acquire() as conn:
        stats = await conn.fetchrow(
            """
            SELECT 
                COUNT(*) as total_messages,
                MIN(created_at) as first_seen,
                MAX(last_activity) as last_activity
            FROM users
            WHERE user_id = $1
            """,
            user_id
        )
        return stats