from sqlalchemy import create_engine, text
from database.config import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ CONEXION EXITOSA:", result.fetchone())

    except Exception as e:
        print("❌ ERROR:", e)


def test_db_info():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT current_database(), current_user
            """))
            print("📊 INFO DB:", result.fetchone())

    except Exception as e:
        print("❌ ERROR INFO DB:", e)


if __name__ == "__main__":
    test_connection()
    test_db_info()