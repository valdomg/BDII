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

#Creating route for template cadUser
@app.route('/cadUser')
def pageUser():
    #Render_template show html and css in web browser
    return render_template('cadUser.html')

#Page cadUser with method HTTP Post
@app.route('/pageUser', methods = ['POST'])
def cadUser():
    #Taking valuees on form in cadUser.html
    idCont = request.form['idCont'] #name of value in form
    nome = request.form['nameCont']
    number = request.form['numberCont']
    email = request.form['emailCont']

    #Connection with database 
    banco = sqlite3.connect('Agenda.db')
    cursor = banco.cursor()

    #.execute is a method for execute commands of sqlite3
    cursor.execute('INSERT INTO contacts VALUES(?,?,?,?)',(idCont, nome, number, email))
    #Commit values in table 
    banco.commit()

    #redirect to function home for render template home.html
    return redirect(url_for('home'))

#Page to edit user, with parameters ID, and methods GET and POST 
@app.route('/editUser/<int:id>', methods = ['GET', 'POST'])
def editUser(id): #route with parameter id for edit unique contact in table
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


#Nova rota -------------------------------------------
@app.route('/detailsUser/<int:id>', methods = ['GET'])
def detailsUser(id):
    banco = sqlite3.connect('Agenda.db')
    cursor = banco.cursor()

    cursor.execute('SELECT * FROM contacts where id=?', (id,))
    contato = cursor.fetchone()
    cursor.close()

    return render_template('detailsUser.html', contato=contato)


if __name__ == '__main__':
    app.secret_key = 'admin123'
    app.run(debug = True)