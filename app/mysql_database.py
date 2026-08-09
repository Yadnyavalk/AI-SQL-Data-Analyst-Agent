import mysql.connector
import os

def get_connection(database_name):
    connection = mysql.connector.connect(
        host = os.getenv("MYSQL_HOST"),
        port = int(os.getenv("MYSQL_PORT")),
        user = os.getenv("MYSQL_USER"),
        password = os.getenv("MYSQL_PASSWORD"),
        database = database_name
    )

    return connection


def run_query(database_name,query):

  try:
    conn = get_connection(database_name)

    cursor = conn.cursor()

    cursor.execute(query)

    results = cursor.fetchall()

    headers = [column[0] for column in cursor.description]

    conn.close()

    return results,headers,None

  except Exception as e:
     return None,None, str(e)

if __name__ == "__main__":

    results, headers = run_query(
        "bank_data",
        "SELECT * FROM bank_churn LIMIT 5"
    )

    print(headers)

    for row in results:
        print(row)