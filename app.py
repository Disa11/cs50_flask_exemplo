from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from cs50 import SQL
import os
from helpers import login_required

app = Flask(__name__)

# Configuración de Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.secret_key = os.urandom(24)
Session(app)

db = SQL("sqlite:///database.db")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('pass')
        
        if not username:
            return render_template('login.html', message="Username is required")
        elif not password:
            return render_template('login.html', message="Password is required")
        
        user = db.execute("SELECT * FROM users WHERE name = :name", name=username)
        
        if len(user) == 0:
            return render_template('login.html', message="User not found")
        
        if user[0]["password"] != password:
            return render_template('login.html', message="Invalid password")
        
        session['user_id'] = user[0]['id']	
        
        return render_template('users.html')
    else:
        return render_template('login.html')   
    
@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('pass')
        confirm = request.form.get('cpass')
        sport = request.form.get('sport')
        
        if not username or not password or not confirm or not sport:
            return render_template('register.html', message="All fields are required")
        elif password != confirm:
            return render_template('register.html', message="Passwords do not match")
        
        user_confirm = db.execute("SELECT * FROM users WHERE name = :name", name=username)
        
        if len(user_confirm) != 0:
            return render_template('register.html', message="User already exists")
        
        try:
            db.execute("INSERT INTO users(name, password, sport) VALUES (:name, :passw, :sport)", name=username, passw=password, sport=sport)
            print("NUEVO usuario agregado")
        except Exception as e:
            print(e)
            print("Error al agregar usuario")
            return render_template('register.html', message="Error al agregar usuario")
        
        return redirect('/login')
        
    else:
        return render_template('register.html') 
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    
@app.route('/users')
@login_required
def users():
    users = db.execute("SELECT * FROM users")
    return render_template('users.html', users=users)
    
    

if __name__ == '__main__':
    app.run(debug=True)
 