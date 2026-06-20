from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key='secret'
DB_NAME='database.db'

def get_connection():
    conn=sqlite3.connect(DB_NAME)
    conn.row_factory=sqlite3.Row
    return conn

def init_db():
    conn=get_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS reservations(uid TEXT PRIMARY KEY,start_date TEXT NOT NULL,status TEXT NOT NULL)')
    conn.commit(); conn.close()

@app.route('/')
def index():
    uid=request.args.get('uid')
    status=request.args.get('status')
    conn=get_connection()
    if uid:
      rows=conn.execute('SELECT * FROM reservations WHERE uid=?',(uid,)).fetchall()
    elif status:
      rows=conn.execute('SELECT * FROM reservations WHERE status=?',(status,)).fetchall()
    else:
      rows=conn.execute('SELECT * FROM reservations ORDER BY start_date').fetchall()
    conn.close(); return render_template('index.html',reservations=rows)

@app.route('/create',methods=['GET','POST'])
def create():
    if request.method=='POST':
      conn=get_connection(); conn.execute('INSERT INTO reservations VALUES(?,?,?)',(request.form['uid'],request.form['start_date'],request.form['status'])); conn.commit(); conn.close(); return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/edit/<uid>',methods=['GET','POST'])
def edit(uid):
    conn=get_connection()
    if request.method=='POST':
      conn.execute('UPDATE reservations SET start_date=?,status=? WHERE uid=?',(request.form['start_date'],request.form['status'],uid)); conn.commit(); conn.close(); return redirect(url_for('index'))
    r=conn.execute('SELECT * FROM reservations WHERE uid=?',(uid,)).fetchone(); conn.close(); return render_template('edit.html',reservation=r)

@app.route('/delete/<uid>')
def delete(uid):
    conn=get_connection(); conn.execute('DELETE FROM reservations WHERE uid=?',(uid,)); conn.commit(); conn.close(); return redirect(url_for('index'))

if __name__=='__main__': init_db(); app.run(debug=True)