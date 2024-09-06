from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from config import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String, nullable=False)
    tarefas = db.relationship('Tarefa', backref='owner', lazy=True)

TarefaUsuario = db.Table('TarefaUsuario',
    db.Column('tarefa_id', db.Integer, db.ForeignKey('tarefa.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    data = db.Column(db.Date, nullable=False)
    descricao = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default='Pendente', nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    usuarios = db.relationship('User', secondary=TarefaUsuario, lazy='subquery', backref=db.backref('tarefasUsuarios', lazy=True))