from flask import Flask, render_template, redirect, request, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ---------------- Models ----------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    notes = db.relationship('Note', backref='user', lazy=True)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- Routes ----------------

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('notepad'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for('notepad'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        existing = User.query.filter_by(username=request.form['username']).first()
        if existing:
            flash('Username already exists!')
        else:
            new_user = User(username=request.form['username'], password=request.form['password'])
            db.session.add(new_user)
            db.session.commit()
            flash('Registered! Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/notepad')
@login_required
def notepad():
    return render_template('notepad.html')  # Use your original Pixel Notepad HTML here

# ---------------- Notes API ----------------

@app.route('/api/notes', methods=['GET'])
@login_required
def get_notes():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        {
            'id': note.id,
            'text': note.text,
            'timestamp': note.timestamp
        } for note in notes
    ])

@app.route('/api/notes', methods=['POST'])
@login_required
def add_note():
    data = request.get_json()
    if not data.get('text'):
        return jsonify({'error': 'Note text is required'}), 400
    new_note = Note(
        text=data['text'],
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        user_id=current_user.id
    )
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(note)
    db.session.commit()
    return jsonify({'success': True})

# ---------------- Run ----------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
