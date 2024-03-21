import sqlite3

banco = sqlite3.connect('Agenda.db')

cursor = banco.cursor()

#cursor.execute('create table if not exists contacts(id INTEGER PRIMARY KEY, name TEXT, number TEXT, email TEXT)')

#cursor.execute("DROP TABLE IF EXISTS contacts")

def insertValues(id,name, number, email):
    cursor.execute(f"INSERT INTO contacts VALUES({id},'{name}','{number}','{email}')")
    banco.commit()
    showTable()

def showTable():
    cursor.execute("SELECT * from contacts")
    print(cursor.fetchall())

def deleteValue(id):
    cursor.execute(f'DELETE FROM contacts where id = {id}')
    showTable()

insertValues(2,'vaom','45', 'vaom@gmail.com')

print('Código executado!')