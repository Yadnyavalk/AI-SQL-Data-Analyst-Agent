from app.database import get_connection


def get_database_schema():

    # Connect to the database
    conn = get_connection()
    cursor = conn.cursor()

    schema = ""

    # Get all user-created tables
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
    """)

    tables = cursor.fetchall()

    # Loop through every table
    for table in tables:

        table_name = table[0]

        schema += f"\nTable: {table_name}\n"

        # Get all columns of that table
        cursor.execute(f"PRAGMA table_info({table_name})")

        columns = cursor.fetchall()

        # Add every column to schema string
        for column in columns:
            schema += f"- {column[1]}\n"

    conn.close()

    return schema