from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    #Creating connection with database
    banco = sqlite3.connect('Agenda.db')
    cursor = banco.cursor()

    #Command for show data on table contacts
    cursor.execute('SELECT * FROM contacts')

    #Command for take all data on table contacts
    data = cursor.fetchall()

    return render_template('home.html', data = data)


@app.route('/cadUser')
def pageUser():
    return render_template('cadUser.html')

@app.route('/pageUser', methods = ['POST'])
def cadUser():
    idCont = request.form['idCont']
    nome = request.form['nameCont']
    number = request.form['numberCont']
    email = request.form['emailCont']

    banco = sqlite3.connect('Agenda.db')
    cursor = banco.cursor()

    cursor.execute('INSERT INTO contacts VALUES(?,?,?,?)',(idCont, nome, number, email))
    banco.commit()

    return redirect(url_for('home'))


@app.route('/editUser/<int:id>', methods = ['GET', 'POST'])
def editUser(id):
    if request.method == 'GET':
        banco = sqlite3.connect('Agenda.db')
        cursor = banco.cursor()

        cursor.execute('SELECT * FROM contacts WHERE id=?', (id,))
        contato = cursor.fetchone()
        cursor.close()
        return render_template('editUser.html', contato=contato)
    
    elif request.method == 'POST':
        nome = request.form['nameCont']
        number = request.form['numberCont']
        email = request.form['emailCont']

        banco = sqlite3.connect('Agenda.db')
        cursor = banco.cursor()

        cursor.execute('UPDATE contacts set name=?, number=?, email=? where id=?', (nome, number, email, id))
        banco.commit()
        return redirect(url_for('home'))

#TAKING ID FOR DELETE USE WITH REQUEST METHOD (GET)
@app.route('/delUser/<int:id>', methods=['GET'])
def delUser(id):
    #Connection with BD
    banco = sqlite3.connect('Agenda.db')
    cursor = banco.cursor()

    cursor.execute(f'DELETE FROM contacts where id={id}')
    banco.commit()
    #flash('Dados Deletados', 'warning')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.secret_key = 'admin123'
    app.run(debug = True)