import aiosqlite
import logging
import uuid
from typing import Optional
from config import DB_PATH

logger = logging.getLogger(__name__)

# Global database connection
db: Optional[aiosqlite.Connection] = None


async def init_db():
    """Initialize database connection and create tables"""
    global db
    try:
        db = await aiosqlite.connect(DB_PATH)
        db.row_factory = aiosqlite.Row  # Enable column access by name
        
        # Create tables
        await create_tables()
        logger.info(f"Database initialized: {DB_PATH}")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


async def create_tables():
    """Create database tables"""
    if db is None:
        raise RuntimeError("Database not initialized")
    
    # Example: Users table
    await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            session_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Example: Messages table
    await db.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)
    
    # Example: Sessions table (for LangFlow sessions)
    await db.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_id TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)
    
    await db.commit()
    logger.info("Database tables created successfully")


async def close_db():
    """Close database connection"""
    global db
    if db:
        await db.close()
        db = None
        logger.info("Database connection closed")


async def get_user(user_id: int) -> Optional[dict]:
    """Get user by user_id"""
    if db is None:
        raise RuntimeError("Database not initialized")
    
    async with db.execute(
        "SELECT * FROM users WHERE user_id = ?", (user_id,)
    ) as cursor:
        row = await cursor.fetchone()
        return dict(row) if row else None


async def create_or_update_user(user_id: int, username: Optional[str] = None,
                                first_name: Optional[str] = None,
                                last_name: Optional[str] = None,
                                session_id: Optional[str] = None):
    """Create or update user"""
    if db is None:
        raise RuntimeError("Database not initialized")
    
    await db.execute("""
        INSERT INTO users (user_id, username, first_name, last_name, session_id, updated_at)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id) DO UPDATE SET
            username = excluded.username,
            first_name = excluded.first_name,
            last_name = excluded.last_name,
            session_id = COALESCE(excluded.session_id, users.session_id),
            updated_at = CURRENT_TIMESTAMP
    """, (user_id, username, first_name, last_name, session_id))
    await db.commit()


async def save_message(user_id: int, message_text: str):
    """Save message to database"""
    if db is None:
        raise RuntimeError("Database not initialized")
    
    await db.execute(
        "INSERT INTO messages (user_id, message_text) VALUES (?, ?)",
        (user_id, message_text)
    )
    await db.commit()


async def get_user_session(user_id: int) -> Optional[str]:
    """Get user's session_id from users table"""
    if db is None:
        raise RuntimeError("Database not initialized")
    
    async with db.execute(
        "SELECT session_id FROM users WHERE user_id = ?",
        (user_id,)
    ) as cursor:
        row = await cursor.fetchone()
        return row[0] if row and row[0] else None


async def get_user_messages(user_id: int, limit: int = 10) -> list:
    """Get user's recent messages"""
    if db is None:
        raise RuntimeError("Database not initialized")
    
    async with db.execute(
        "SELECT * FROM messages WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
        (user_id, limit)
    ) as cursor:
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

