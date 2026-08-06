from app.mysql_database import get_connection


def get_database_schema(database_name):

    conn = get_connection(database_name)

    cursor = conn.cursor()

    schema = ""

    #Get all tables from selected tables

    cursor.execute("SHOW TABLES")

    tables = cursor.fetchall()

    for table in tables:

        table_name = table[0]

        schema += f"\nTable:{table_name}\n"

        cursor.execute(f"SHOW COLUMNS FROM {table_name}")

        columns = cursor.fetchall()

        for column in columns:
            schema += f"- {column[0]}\n"

    conn.close()

    return schema


if __name__ == "__main__":

    schema = get_database_schema("bank_data")

    print(schema)