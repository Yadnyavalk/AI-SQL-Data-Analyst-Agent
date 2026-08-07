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


        try:

            cursor.execute(
                f"""
                SELECT DISTINCT {column[0]}
                FROM {table_name}
                WHERE {column[0]} IS NOT NULL
                LIMIT 5
                """
            )

            values = cursor.fetchall()

            if (
                len(values) > 0 and
                len(values) <= 5
            ):

                value_list = [
                    str(v[0])
                    for v in values
                ]

                schema += (
                    f"  Possible values: "
                    f"{', '.join(value_list)}\n"
                )

        except:
            pass
#above change will look like 
# Table: bank_churn | Gender: Male, Female | IsActiveMember: Yes, No 
# | Exited: Yes, No | Geography: Germany, France, Spain
 
    conn.close()

    return schema


if __name__ == "__main__":

    schema = get_database_schema("bank_data")

    print(schema)