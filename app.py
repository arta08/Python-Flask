from flask import Flask, render_template, redirect, request, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'python_web'
app.secret_key = 'my_precious'

mysql = MySQL(app)

@app.route('/')
def index():
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM students")
  data = cur.fetchall()
  return render_template('index.html', students = data)

@app.route('/insert', methods = ['POST'])
def insert():
  if request.method == "POST":
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    try:
      cur = mysql.connection.cursor()
      cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
      mysql.connection.commit()
      flash("Data Inserted Successfully")
      return redirect(url_for('index'))
    except Exception as e:
      print(f"Error occurred during INSERT operation: {e}")
      flash(e)
      return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
  if request.method == 'POST':
    id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    cur = mysql.connection.cursor()
    cur.execute("""UPDATE students 
                SET name = %s, email = %s, phone = %s 
                WHERE id = %s""", (name, email, phone, id))
    mysql.connection.commit()
    flash("Data Updated Successfully")
    return redirect(url_for('index'))

@app.route('/delete/<string:id_data>', methods=['GET', 'POST'])
def delete(id_data):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM students WHERE id = %s", (id_data,))
        mysql.connection.commit()
        flash("Data Deleted Successfully")
    except Exception as e:
        flash({e})
    finally:
        cur.close() 
    return redirect(url_for('index'))

if __name__ == "__main__":
  app.run(debug=True)