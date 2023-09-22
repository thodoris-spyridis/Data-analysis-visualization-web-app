from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileAllowed


class UploadFileForm(FlaskForm):  # upload file form
    file = FileField("File", validators=[InputRequired(), FileAllowed(["xlsx"], "wrong format!")])
    submit = SubmitField("Upload File")


class RegistrationForm(FlaskForm):  # user registration form
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm_password", validators=[DataRequired(), EqualTo("password")])
    sign_up = SubmitField("Sign up")


class LoginForm(FlaskForm):  # user registration form
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    remember = BooleanField("Remember me")
    log_in = SubmitField("Log in")



