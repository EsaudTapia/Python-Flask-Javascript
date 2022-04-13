from datetime import date
from wtforms import Form
from wtforms import RadioField, IntegerField, StringField, SelectField, DecimalField, DateField,PasswordField,DecimalField
from wtforms.validators import DataRequired
from wtforms import validators


class Personaform(Form):
    fname=StringField("Nombre", [DataRequired("Campo vacio *")])
    lname=StringField("Apellido", [DataRequired("Campo vacio *")])