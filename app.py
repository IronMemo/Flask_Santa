import random
from flask import Flask, render_template, request, redirect, url_for
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_request
def create_tables():
    if not hasattr(app, 'tables_created'):
        db.create_all()
        app.tables_created = True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return redirect(url_for('names'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Verifică dacă există deja un utilizator cu același email
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('register.html', error="Email already in use")

        # Verifică dacă parolele coincid
        if password == confirm_password:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))  # Redirecționează la pagina de login
        else:
            return render_template('register.html', error="Passwords do not match")
    return render_template('register.html')


@app.route('/names', methods=['GET', 'POST'])
def names():
    if request.method == 'POST':
        names = []
        for i in range(1, 31):
            name = request.form.get(f'name{i}')
            if name:
                names.append(name)
        if len(names) < 2:
            return "Please enter at least 2 names."
        
        # Generare perechi aleatorii
        random.shuffle(names)
        givers = names[:]
        receivers = names[:]
        random.shuffle(receivers)

        # Asigură-te că nimeni nu este propriul Secret Santa
        while any(giver == receiver for giver, receiver in zip(givers, receivers)):
            random.shuffle(receivers)

        pairs = list(zip(givers, receivers))

        return render_template('pairs.html', pairs=pairs)
    return render_template('names.html')

if __name__ == '__main__':
    app.run(debug=True)
