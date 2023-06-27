import pyodbc
import pymysql

# Connect to the MSSQL database
mssql_conn_str = 'DRIVER=SQL Server Native Client 11.0;SERVER=DESKTOP-5IMR7O6;DATABASE=db_ppra;UID=sa;PWD=Pakistan@786'
mssql_conn = pyodbc.connect(mssql_conn_str)

# Connect to the target SQL database
sql_conn_str = 'DRIVER=MySQL ODBC 8.0 ANSI Driver;SERVER=127.0.0.1;DATABASE=db_ppra;UID=root;PWD='
sql_conn = pyodbc.connect(sql_conn_str)

# Fetch the list of tables from the MSSQL database
mssql_cursor = mssql_conn.cursor()
mssql_cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
tables = [table[0] for table in mssql_cursor.fetchall()]

# Iterate over each table and migrate the data
for table in tables:
    # Fetch the table data from the MSSQL database
    mssql_cursor.execute(f"SELECT * FROM {table}")
    rows = mssql_cursor.fetchall()

    # Create the table in the SQL database
    sql_cursor = sql_conn.cursor()
    # Create a new table with the same structure as an existing table
    # sql_cursor.execute(f"CREATE TABLE {table} LIKE {table}")
    # Add the constraints from the existing table to the new table
    # sql_cursor.execute(f"ALTER TABLE {table} ADD CONSTRAINTS LIKE {table}")
    print(table.lower())
    # Insert the data into the SQL table
    sql_cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

    for row in rows:
        sql_cursor.execute(f"INSERT INTO {table.lower()} VALUES ({','.join('?' * len(row))})", row)

    sql_cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    # Commit the changes for each table
    sql_conn.commit()

# Close the database connections
mssql_conn.close()
sql_conn.close()
