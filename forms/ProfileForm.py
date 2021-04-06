from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class ProfileForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    sename = StringField('Фамилия', validators=[DataRequired()])
    nickname = StringField('Никнейм', validators=[DataRequired()])
    phone = IntegerField('телефон', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    img = FileField("Аватарка", validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    birthday = DateField('День рождения', format='%d.%m.%Y')
    submit = SubmitField('Загрузить')