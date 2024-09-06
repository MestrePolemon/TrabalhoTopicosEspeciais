from config import app, db
from models import User, Tarefa, TarefaUsuario

with app.app_context():
    db.create_all()