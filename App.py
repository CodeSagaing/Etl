from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'etl'
mysql = MySQL(app)

# Session
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM etiqueta")
    data = cur.fetchall()
    return render_template('index.html', etiquetas = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        id = request.form['id']
        etiqueta = request.form['etiqueta']
        print(id)
        print(etiqueta)

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO etiqueta (id_etiqueta, etiqueta) VALUES (%s, %s)', (id, etiqueta))
        mysql.connection.commit()
        flash("Etiqueta registrada corrrectamente")
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_etiqueta(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM etiqueta WHERE id_etiqueta = {}".format(id))
    data = cur.fetchall()
    return render_template("edit_etiqueta.html", etiqueta = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_etiqueta(id):
    if request.method == 'POST':
        id_etiqueta = request.form['id']
        etiqueta = request.form['etiqueta']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE etiqueta SET id_etiqueta = %s, etiqueta = %s  WHERE id_etiqueta = %s", (id_etiqueta, etiqueta, id))
        mysql.connection.commit()
        flash("Etiqueta actualizada correctamente")
        return redirect(url_for("Index"))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM etiqueta WHERE id_etiqueta = {0}".format(id))
    mysql.connection.commit()
    flash("Etiqueta removida correctamente")
    return redirect(url_for("Index"))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)

