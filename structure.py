import pyodbc
import mysql.connector

# Connect to MSSQL
mssql_conn = pyodbc.connect(
    'DRIVER=SQL Server Native Client 11.0;SERVER=DESKTOP-5IMR7O6;DATABASE=db_ppra;UID=sa;PWD=Pakistan@786'
)

# Retrieve table structure from MSSQL
table_name = '<mssql_table_name>'
mssql_cursor = mssql_conn.cursor()
mssql_cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
columns = mssql_cursor.fetchall()

# Connect to MySQL
mysql_conn = mysql.connector.connect(
    host='127.0.0.1',
    database='db_ppra',
    user='root',
    password=''
)

# Create the table in MySQL with lowercase column names
mysql_cursor = mysql_conn.cursor()
mysql_table_name = '<mysql_table_name>'
mysql_create_table_sql = f"CREATE TABLE {mysql_table_name} ("
for column in columns:
    column_name, data_type, max_length = column
    lowercase_column_name = column_name.lower()  # Convert column name to lowercase
    mysql_create_table_sql += f"{lowercase_column_name} {data_type}"
    if max_length is not None:
        mysql_create_table_sql += f"({max_length})"
    mysql_create_table_sql += ", "
mysql_create_table_sql = mysql_create_table_sql.rstrip(", ")
mysql_create_table_sql += ")"

mysql_cursor.execute(mysql_create_table_sql)

# Close connections
mssql_cursor.close()
mssql_conn.close()
mysql_cursor.close()
mysql_conn.close()
