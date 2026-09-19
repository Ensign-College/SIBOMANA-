import sqlite3
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_module import create_table, insertRow, getRecords, delRecord, updateRec

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

def setup():
    create_table(database, fieldlist)
    fields = ['contactid', 'last', 'first', 'address', 'city', 'state', 'postalcode']
    # Insert sample data
    fieldata = [1, 'Washington', 'George', '3200 Mount Vernon Memorial Highway', 'Mt. Vernon', 'VA', '22121']
    insertRow(database, fields, fieldata)
    fieldata = [2, 'Lincoln', 'Abraham', '123 Main ST', 'Springfield', 'MO', '65803']
    insertRow(database, fields, fieldata)
    fieldata = [3, 'Monroe', 'James', '2050 James Monroe Pkwy', 'Charlottesville', 'VA', '22902']
    insertRow(database, fields, fieldata)

def test_del_record():
    setup()
    whereclause = "WHERE contactid = 2"
    delRecord(database, whereclause)
    conn = sqlite3.connect(database['dbname'])
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE contactid = 2")
    result = cursor.fetchall()
    assert len(result) == 0, "Record not deleted"
    conn.close()

def test_update_rec():
    setup()
    updateRec(database)
    conn = sqlite3.connect(database['dbname'])
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE contactid = 1")
    result = cursor.fetchall()
    assert result[0][1] != 'Washington', "Record not updated"
    conn.close()
