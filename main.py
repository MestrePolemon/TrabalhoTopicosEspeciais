from datetime import date
from flask import Flask, render_template, redirect, url_for, flash, request
from config import app, db
from models import User, load_user, Tarefa
from flask_login import login_user, login_required, logout_user, current_user
from formulario import FormularioCriarConta, FormularioLogin, FormularioCriarTarefa
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    formulario = FormularioCriarConta()
    if formulario.validate_on_submit():
        usu = formulario.usuario.data
        usuBanco = User.query.filter_by(usuario=usu).first()
        if usuBanco:
            flash('Usuario já existe', 'danger')
        else:
            sen = generate_password_hash(formulario.senha.data)
            novoUsuario = User(usuario=usu, senha=sen)
            db.session.add(novoUsuario)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html', form=formulario)

@app.route('/login', methods=['GET', 'POST'])
def login():
    formulario = FormularioLogin()
    if formulario.validate_on_submit():
        usu = formulario.usuario.data
        usuBanco = User.query.filter_by(usuario=usu).first()
        if usuBanco:
            sen = formulario.senha.data
            senhaHash = usuBanco.senha
            if check_password_hash(senhaHash, sen):
                login_user(usuBanco)
                return redirect(url_for('gerenciador'))
            else:
                flash('Usuario ou senha incorretos', 'danger')
        else:
            flash('Usuario ou senha incorretos', 'danger')
    return render_template('login.html', form=formulario)

@app.route('/gerenciador')
@login_required
def gerenciador():
    tarefas = Tarefa.query.filter((Tarefa.user_id == current_user.id) | (Tarefa.usuarios.any(id=current_user.id))).all()
    return render_template('gerenciador.html', tarefas=tarefas)

@app.route('/criartarefas', methods=['GET', 'POST'])
@login_required
def criartarefas():
    formulario = FormularioCriarTarefa()
    formulario.usuarios.choices = [(user.id, user.usuario) for user in User.query.all()]

    if formulario.validate_on_submit():
        nome = formulario.nome.data
        data = formulario.data.data
        descricao = formulario.descricao.data
        usuarios_ids = formulario.usuarios.data

        if data < date.today():
            flash('Data inválida', 'danger')
            return redirect(url_for('criartarefas'))

        tarefa = Tarefa(nome=nome, data=data, descricao=descricao, user_id=current_user.id)
        db.session.add(tarefa)
        db.session.commit()

        for user_id in usuarios_ids:
            user = User.query.get(user_id)
            tarefa.usuarios.append(user)

        db.session.commit()
        return redirect(url_for('gerenciador'))

    return render_template('criartarefas.html', form=formulario)

@app.route('/visualizar_tarefas/<int:id>')
@login_required
def visualizar_tarefas(id):
    tarefa = Tarefa.query.get(id)
    return render_template('visualizar_tarefas.html', tarefa=tarefa)

@app.route('/editar_tarefas/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_tarefas(id):
    tarefa = Tarefa.query.get(id)
    formulario = FormularioCriarTarefa(obj=tarefa)
    formulario.usuarios.choices = [(user.id, user.usuario) for user in User.query.all()]

    if formulario.validate_on_submit():
        tarefa.nome = formulario.nome.data
        tarefa.data = formulario.data.data
        tarefa.descricao = formulario.descricao.data
        tarefa.status = formulario.status.data
        tarefa.usuarios.clear()

        usuarios_ids = formulario.usuarios.data
        for user_id in usuarios_ids:
            user = User.query.get(user_id)
            tarefa.usuarios.append(user)

        db.session.commit()
        return redirect(url_for('gerenciador'))

    return render_template('editar_tarefas.html', form=formulario, tarefa=tarefa)

@app.route('/deletar_tarefas/<int:id>', methods=['GET', 'POST'])
@login_required
def deletar_tarefas(id):
    tarefa = Tarefa.query.get(id)
    if tarefa.user_id != current_user.id:
        flash('Você não tem permissão para deletar esta tarefa', 'danger')
        return redirect(url_for('gerenciador'))

    if request.method == 'POST':
        nomeConfirmacao = request.form.get('nome_confirmacao')
        if nomeConfirmacao == tarefa.nome:
            db.session.delete(tarefa)
            db.session.commit()
            flash('Tarefa deletada com sucesso', 'success')
            return redirect(url_for('gerenciador'))
        else:
            flash('Nome da tarefa incorreto', 'danger')

    return render_template('deletar_tarefas.html', tarefa=tarefa)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)