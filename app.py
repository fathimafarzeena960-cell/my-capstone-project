from flask import Flask, request, render_template, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'secretkey'
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ---------------- MODELS ----------------

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    role = db.Column(db.String(20), default='user')


class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# ---------------- DECORATORS ----------------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = User.query.get(session['user_id'])
        print(f"DEBUG - User: {user.username}, Role: {user.role}")
        if not user or user.role != 'admin':
            flash('Admins only!', 'danger')
            return redirect('/dashboard')
        return f(*args, **kwargs)
    return decorated

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect('/dashboard')
        return "Invalid credentials"
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        content = request.form['content']
        new_note = Note(content=content, user_id=session['user_id'])
        db.session.add(new_note)
        db.session.commit()
    notes = Note.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', notes=notes)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    note = Note.query.get(id)
    if note and note.user_id == session['user_id']:
        db.session.delete(note)
        db.session.commit()
        flash("Note deleted successfully!")
    return redirect('/dashboard')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    note = Note.query.get(id)
    if request.method == 'POST':
        note.content = request.form['content']
        db.session.commit()
        return redirect('/dashboard')
    return render_template('edit.html', note=note)


# ---------------- ADMIN ROUTES ----------------

@app.route('/admin')
@login_required
@admin_required
def admin():
    users = User.query.all()
    notes = Note.query.all()
    total_users = len(users)
    total_notes = len(notes)
    return render_template('admin.html',
                           users=users,
                           notes=notes,
                           total_users=total_users,
                           total_notes=total_notes)


@app.route('/admin/delete_user/<int:id>')
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    Note.query.filter_by(user_id=id).delete()
    db.session.delete(user)
    db.session.commit()
    flash('User deleted.', 'success')
    return redirect('/admin')


# ---------------- RUN APP ----------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)