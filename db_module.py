import sqlite3


# Function to create a table in the database
# Arguments:
# - database: a dictionary containing database name ('dbname') and table name ('tblname')
# - fields: a list of dictionaries, each representing a field with 'name', 'dtype' (data type), and 'modify' (field modifier)
def create_table(database, fields):
    # Connect to the database
    conn = sqlite3.connect(database['dbname'])
    cursor = conn.cursor()

    # Start building the SQL query to create a tab
    sql = "CREATE TABLE " + database['tblname'] + "("

    # Iterate over the fields list to define the table structure
    for f in fields:
        sql += f['name'] + " " + f['dtype'] + " " + f['modify'] + ","

    # Remove the last comma and close the table creation query
    sql = sql[:-1]
    sql += ")"

    # Drop the table if it already exists to ensure a clean slate
    cursor.execute("DROP TABLE IF EXISTS " + database['tblname'])

    # Execute the final SQL query to create the table
    cursor.execute(sql)

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()


# Function to insert a row into the table
# Arguments:
# - database: a dictionary containing database name ('dbname') and table name ('tblname')
# - _fields: a list of field names to insert data into
# - _fieldata: a list of data values corresponding to the fields
def insertRow(database, _fields, _fieldata):
    # Ensure the number of fields matches the number of data values
    if len(_fields) != len(_fieldata):
        print("Field list does not equal data provided");
        return

    # Connect to the database
    conn = sqlite3.connect(database['dbname'])
    cursor = conn.cursor()

    # Start building the SQL query to insert data
    sql = "INSERT INTO " + database['tblname'] + "("

    # Add field names to the query
    for f in _fields:
        sql += f + ","

    # Remove the last comma and add the placeholders for the values
    sql = sql[:-1] + ")"
    sql += " VALUES("

    # Add placeholders for each value
    for f in range(len(_fieldata)):
        sql += "?" + ","

    # Remove the last comma and close the query
    sql = sql[:-1] + ")"

    # Execute the query with the provided data
    cursor.execute(sql, _fieldata)

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()


# Function to retrieve and display records from the table
# Arguments:
# - database: a dictionary containing database name ('dbname') and table name ('tblname')
# - wclause: a SQL WHERE clause to filter the records (optional)
def getRecords(database, wclause):
    # Display a title for the records being fetched
    title = "All records from the table " + database['tblname'] + ":"

    # If a WHERE clause is provided, append it to the title
    if len(wclause) > 0:
        title = title[:-1] + " " + wclause

    # Connect to the database
    conn = sqlite3.connect(database['dbname'])
    cursor = conn.cursor()

    # Build and execute the SQL query to retrieve records
    sql = "SELECT * FROM " + database['tblname'] + " " + wclause
    cursor.execute(sql)

    # Fetch all the rows from the query result
    rows = cursor.fetchall()

    # Print the title and each row of data
    print(title)
    for row in rows:
        print(row)

    # Close the database connection
    conn.close()


# Function to delete records from the table based on a condition
# Arguments:
# - database: a dictionary containing database name ('dbname') and table name ('tblname')
# - whereclause: a SQL WHERE clause to specify which records to delete
def delRecord(database, whereclause):
    """Deletes a record(s) from the table based on the given whereclause."""
    # TO DO: Add code to delete records based on the whereclause
    pass


# Function to update a record in the table based on the provided information
# Arguments:
# - database: a dictionary containing database name ('dbname'), table name ('tblname'),
#             primary key field ('primarykeyfield'), primary key value ('primarykeyvalue'),
#             field to update ('updatenamefield'), and new value ('newname')
def updateRec(database):
    """Updates a record based on the information from the database dictionary."""
    # TO DO: Add code to update a record based on the database dictionary
    pass

    # After updating, get the updated record. This is an extra step to show the updated record.
    getRecords(database, "WHERE " + database["primarykeyfield"] + " = " + str(database["primarykeyvalue"]))


def main():
    database = {'dbname': 'info.db', 'tblname': 'contacts',
                'primarykeyfield': 'contactid', 'primarykeyvalue': '1',
                'updatenamefield': 'last', 'newname': 'Yuto'}

    fieldlist = [
        {'name': 'contactid', 'dtype': 'int', 'modify': 'primary key'},
        {'name': 'last', 'dtype': 'varchar(30)', 'modify': ''},
        {'name': 'first', 'dtype': 'varchar(20)', 'modify': ''},
        {'name': 'address', 'dtype': 'varchar(50)', 'modify': ''},
        {'name': 'city', 'dtype': 'varchar(20)', 'modify': ''},
        {'name': 'state', 'dtype': 'char(2)', 'modify': ''},
        {'name': 'postalcode', 'dtype': 'varchar(15)', 'modify': ''}
    ]

    create_table(database, fieldlist)

    fields = ['contactid', 'last', 'first', 'address', 'city', 'state', 'postalcode']

    # Insert sample data
    fieldata = [1, 'Washington', 'George', '3200 Mount Vernon Memorial Highway', 'Mt. Vernon', 'VA', '22121']
    insertRow(database, fields, fieldata)
    fieldata = [2, 'Lincoln', 'Abraham', '123 Main ST', 'Springfield', 'MO', '65803']
    insertRow(database, fields, fieldata)
    fieldata = [3, 'Monroe', 'James', '2050 James Monroe Pkwy', 'Charlottesville', 'VA', '22902']
    insertRow(database, fields, fieldata)

    whereclause = ""
    getRecords(database, whereclause)

    print("-" * 25)

    whereclause = "WHERE state = 'MO'"
    getRecords(database, whereclause)

    print("-" * 25)

    # Delete a record using a whereclause
    whereclause = "WHERE contactid = 2"
    delRecord(database, whereclause)

    print("-" * 25)

    # Display all records after deletion
    getRecords(database, "")

    print("-" * 25)

    # Update a record based on database dictionary
    updateRec(database)

    print("-" * 25)

    # Display all records after update
    getRecords(database, "")


main()
