import sqlite3

def get_connection():
    return sqlite3.connect("data/company.db")

def create_database():
    conn = get_connection()

    cursor = conn.cursor()
#Think of the cursor as your SQL executor.Without it...Python can't execute SQL.


    cursor.execute("""
     CREATE TABLE IF NOT EXISTS employees(
        employee_id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        salary INTEGER,
        city TEXT
    )
    """)
     # Remove old data (so we don't get duplicates when running again)
    cursor.execute("DELETE FROM employees")

 # Sample data
    employees = [
        (1, "Rahul", "IT", 85000, "Pune"),
        (2, "Priya", "HR", 60000, "Mumbai"),
        (3, "Amit", "Finance", 95000, "Delhi"),
        (4, "Sneha", "IT", 78000, "Bangalore"),
        (5, "Rohan", "Sales", 72000, "Pune"),
        (6, "Neha", "Marketing", 68000, "Hyderabad"),
        (7, "Arjun", "IT", 99000, "Chennai"),
        (8, "Kiran", "Finance", 88000, "Mumbai"),
        (9, "Meera", "HR", 65000, "Pune"),
        (10, "Vikram", "Sales", 81000, "Delhi")
    ]

###Instead of writing:cursor.execute(...)cursor.execute(...)cursor.execute(...)100 times...We write:cursor.executemany(...)###

    cursor.executemany("""
    INSERT INTO employees
    VALUES (?, ?, ?, ?, ?)
    """, employees)


    conn.commit()   #Save changes.Without commit...Nothing gets saved.
    conn.close()

    print("Database Created Sucessfully")
    print("10 Employee Records Inserted!")



if __name__ ==  "__main__":
    create_database()

def show_employees():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("Select * From employees")

    employees = cursor.fetchall()

    conn.close()

    print("\nEmployee Records")
    print("="*60)

    for employee in employees:
        print(employee)



def show_it_employees():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""Select * from employees where department = 'IT'""")
    employees = cursor.fetchall()

    conn.close()

    print("\nEmployees from IT DEPT")
    print("-"*60)

    for employee in employees :
        print(employee)

if __name__ == "__main__":
     create_database()
     show_employees()
     show_it_employees()


def run_query(query):

  try :
    
    conn = get_connection()

    cursor = conn.cursor()

   
    cursor.execute(query)

    results = cursor.fetchall()

    # Get column names returned by SQLite
    headers = [description[0] for description in cursor.description]


    conn.close()

    return results,headers

  except Exception as e:

      print("\nDatabase Error:")
      print(e)

      return None

