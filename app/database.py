import sqlite3


def get_connection():
    return sqlite3.connect("data/company.db")


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    

    # Create Employees Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        employee_id INTEGER PRIMARY KEY,
        name TEXT,
        department_id INTEGER,
        salary INTEGER,
        city TEXT
    )
    """)

    # Create Departments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments(
        department_id INTEGER PRIMARY KEY,
        department_name TEXT
    )
    """)

    # Remove old data
    cursor.execute("DELETE FROM employees")
    cursor.execute("DELETE FROM departments")

    # Employee Data
    employees = [
        (1, "Rahul", 1, 85000, "Pune"),
        (2, "Priya", 2, 60000, "Mumbai"),
        (3, "Amit", 3, 95000, "Delhi"),
        (4, "Sneha", 1, 78000, "Bangalore"),
        (5, "Rohan", 4, 72000, "Pune"),
        (6, "Neha", 5, 68000, "Hyderabad"),
        (7, "Arjun", 1, 99000, "Chennai"),
        (8, "Kiran", 3, 88000, "Mumbai"),
        (9, "Meera", 2, 65000, "Pune"),
        (10, "Vikram", 4, 81000, "Delhi")
    ]

    cursor.executemany("""
    INSERT INTO employees
    VALUES (?, ?, ?, ?, ?)
    """, employees)

    # Department Data
    departments = [
        (1, "IT"),
        (2, "HR"),
        (3, "Finance"),
        (4, "Sales"),
        (5, "Marketing")
    ]

    cursor.executemany("""
    INSERT INTO departments
    VALUES (?, ?)
    """, departments)

    conn.commit()

        # Check the structure of the employees table
    cursor.execute("PRAGMA table_info(employees)")
    print(cursor.fetchall())

    conn.close()

    print("Database Created Successfully")
    print("10 Employee Records Inserted!")


def show_employees():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    conn.close()

    print("\nEmployee Records")
    print("=" * 60)

    for employee in employees:
        print(employee)


def show_it_employees():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM employees
    WHERE department_id = 1
    """)

    employees = cursor.fetchall()

    conn.close()

    print("\nEmployees from IT Department")
    print("-" * 60)

    for employee in employees:
        print(employee)


def run_query(query):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query)

        results = cursor.fetchall()

        # Get column names dynamically
        headers = [description[0] for description in cursor.description]

        conn.close()

        return results, headers

    except Exception as e:
        print("\nDatabase Error:")
        print(e)
        return None


if __name__ == "__main__":
    create_database()
    show_employees()
    show_it_employees()