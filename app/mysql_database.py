import mysql.connector

def get_connection(database_name):
    connection = mysql.connector.connect(
        host = "127.0.0.1",
        port = 3306,
        user = "root",
        password = "root",
        database = "bank_data"
    )

    return connection


def run_query(database_name,query):

    conn = get_connection(database_name)

    cursor = conn.cursor()

    cursor.execute(query)

    results = cursor.fetchall()

    headers = [column[0] for column in cursor.description]

    conn.close()

    return results,headers

if __name__ == "__main__":

    results, headers = run_query(
        "bank_data",
        "SELECT * FROM bank_churn LIMIT 5"
    )

    print(headers)

    for row in results:
        print(row)