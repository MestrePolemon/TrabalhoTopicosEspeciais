from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectMultipleField, widgets, SelectField
from wtforms.validators import DataRequired, Length

class FormularioCriarConta(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=25)])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class FormularioLogin(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')



class FormularioCriarTarefa(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    data = DateField('Data', validators=[DataRequired()])
    descricao = StringField('Descrição', validators=[DataRequired()])
    usuarios = SelectMultipleField('Usuarios', option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    submit = SubmitField('Criar Tarefa')

class FormularioEditarTarefa(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    data = DateField('Data', validators=[DataRequired()])
    descricao = StringField('Descrição', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pendente', 'Pendente'),('Ta indo ( EM ANDAMENTO)', 'Ta indo (EM ANDAMENTO)'), ('Concluida', 'Concluida')], validators=[DataRequired()])
    usuarios = SelectMultipleField('Usuarios', option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    submit = SubmitField('Editar Tarefa')