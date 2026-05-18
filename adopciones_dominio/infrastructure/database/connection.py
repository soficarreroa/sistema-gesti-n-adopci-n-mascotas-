import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    connection = psycopg2.connect(
        DATABASE_URL,
        sslmode="require"
    )

    print("✅ Conexión exitosa a Supabase")

    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    print("📊 Test query:", cursor.fetchone())

    cursor.close()
    connection.close()

except Exception as e:
    print("❌ Error de conexión:")
    print(e)